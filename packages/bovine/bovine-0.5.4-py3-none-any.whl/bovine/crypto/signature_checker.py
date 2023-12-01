import logging
import json
import warnings

from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Callable, Awaitable, Tuple
import bovine.utils.date
from bovine.utils.date import parse_gmt

from .helper import content_digest_sha256
from .http_signature import HttpSignature
from .signature import parse_signature_header
from .types import CryptographicIdentifier

logger = logging.getLogger(__name__)


@dataclass
class SignatureChecker:
    key_retriever: Callable[
        [str], Awaitable[Tuple[str | None, str | None] | CryptographicIdentifier | None]
    ]

    async def validate_signature(self, method, url, headers, body) -> str | None:
        if "signature" not in headers:
            logger.debug("Signature not present on request for %s", url)
            logger.debug(json.dumps(dict(headers)))
            return None

        if method.lower() == "post":
            digest = content_digest_sha256(await body())
        else:
            digest = None

        if digest is not None:
            request_digest = headers["digest"]
            request_digest = request_digest[:4].lower() + request_digest[4:]
            if request_digest != digest:
                logger.warning("Different digest")
                return None

        try:
            http_signature = HttpSignature()
            parsed_signature = parse_signature_header(headers["signature"])
            signature_fields = parsed_signature.fields

            if (
                "(request-target)" not in signature_fields
                or "date" not in signature_fields
            ):
                logger.warning("Required field not present in signature")
                return None

            if digest is not None and "digest" not in signature_fields:
                logger.warning("Digest not present, but computable")
                return None

            http_date = parse_gmt(headers["date"])
            if not bovine.utils.date.check_max_offset_now(http_date):
                logger.warning(f"Encountered invalid http date {headers['date']}")
                return None

            for field in signature_fields:
                if field == "(request-target)":
                    method = method.lower()
                    parsed_url = urlparse(url)
                    path = parsed_url.path
                    http_signature.with_field(field, f"{method} {path}")
                else:
                    http_signature.with_field(field, headers[field])

            key_result = await self.key_retriever(parsed_signature.key_id)

            if isinstance(key_result, tuple):
                warnings.warn(
                    "Returning a tuple from key_retriever is deprecated, return a CryptographicIdentifier instead, will be remove in bovine 0.6.0",
                    DeprecationWarning,
                )
                key_result = CryptographicIdentifier.from_pem(*key_result)

            if key_result is None:
                logger.debug(f"Could not retrieve key from {parsed_signature.key_id}")
                return None

            return http_signature.verify_with_identity(
                key_result, parsed_signature.signature
            )

        except Exception as e:
            logger.exception(str(e))
            logger.error(headers)
            return None

        return None

    async def validate_signature_request(self, request) -> str | None:
        return await self.validate_signature(
            request.method, request.url, request.headers, request.get_data
        )

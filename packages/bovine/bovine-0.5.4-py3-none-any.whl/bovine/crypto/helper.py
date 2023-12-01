import base64
import hashlib
import logging
import warnings
import jcs

from typing import Tuple
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
import based58

logger = logging.getLogger(__name__)

multicodec_ed25519_public_bytes = b"\xed\x01"
multicodec_ed25519_private_bytes = b"\x80\x26"
multicodec_rsa_public_bytes = b"\x85$"


def content_digest_sha256(content: str | bytes) -> str:
    """Computes the SHA256 digest of given content"""
    if isinstance(content, str):
        content = content.encode("utf-8")

    digest = base64.standard_b64encode(hashlib.sha256(content).digest()).decode("utf-8")
    return "sha-256=" + digest


def sign_message(private_key, message):
    warnings.warn("Deprecated will be removed with bovine 0.6.0", DeprecationWarning)
    try:
        key = load_pem_private_key(private_key.encode("utf-8"), password=None)
        assert isinstance(key, rsa.RSAPrivateKey)
    except Exception as e:
        logger.error(e)
        logger.error(private_key)
        raise (e)

    return base64.standard_b64encode(
        key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    ).decode("utf-8")


def verify_signature(public_key, message, signature):
    public_key_loaded = load_pem_public_key(public_key.encode("utf-8"))

    assert isinstance(public_key_loaded, rsa.RSAPublicKey)

    try:
        public_key_loaded.verify(
            base64.standard_b64decode(signature),
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature:
        logger.warning("invalid signature")
        return False

    return True


def public_key_to_did_key(public_key: ed25519.Ed25519PublicKey) -> str:
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    encoded = based58.b58encode(multicodec_ed25519_public_bytes + public_bytes)

    return "did:key:z" + encoded.decode("utf-8")


def private_key_to_base58(private_key: ed25519.Ed25519PrivateKey) -> str:
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    encoded = based58.b58encode(multicodec_ed25519_private_bytes + private_bytes)
    return "z" + encoded.decode("ascii")


def did_key_to_public_key(did: str) -> ed25519.Ed25519PublicKey:
    if not did.startswith("did:key:z"):
        raise ValueError(f"Should start with 'did:key:z' got {str}")
    decoded = based58.b58decode(did[9:].encode("ascii"))
    if decoded[:2] != multicodec_ed25519_public_bytes:
        raise ValueError(f"Improper start for ed25519 public key. Got {str}")
    return ed25519.Ed25519PublicKey.from_public_bytes(decoded[2:])


def private_key_to_ed25519(private_key_str: str) -> ed25519.Ed25519PrivateKey:
    decoded = based58.b58decode(private_key_str[1:].encode("utf-8"))
    if decoded[:2] != multicodec_ed25519_private_bytes:
        raise ValueError(f"Improper start for ed25519 private key. Got {str}")

    return ed25519.Ed25519PrivateKey.from_private_bytes(decoded[2:])


def multibase_58btc_encode(data: bytes) -> str:
    """Encodes `data` in base 58 using the bitcoin alphabet
    and adds the prefix `z`"""
    return "z" + based58.b58encode(data).decode("utf-8")


def multibase_decode(data: str) -> bytes:
    """Decodes the string data using the multibase algorithm"""
    if data[0] == "z":
        return based58.b58decode(data[1:].encode("utf-8"))

    raise ValueError(f"{data} encoded in unknown format")


def jcs_sha356(doc: dict) -> str:
    """Returns the sha256 digest of the representation
    of dict according to JCS. This assumes that `doc`
    is JSON serializable.

    JCS is defined in [RFC8785](https://www.rfc-editor.org/rfc/rfc8785).
    """
    return hashlib.sha256(jcs.canonicalize(doc)).digest()


def split_according_to_fep8b32(doc: dict) -> Tuple[dict, dict, bytes]:
    pure_doc = {key: value for key, value in doc.items() if key != "proof"}
    pure_proof = {
        key: value for key, value in doc["proof"].items() if key != "proofValue"
    }
    signature = multibase_decode(doc["proof"]["proofValue"])

    return pure_doc, pure_proof, signature

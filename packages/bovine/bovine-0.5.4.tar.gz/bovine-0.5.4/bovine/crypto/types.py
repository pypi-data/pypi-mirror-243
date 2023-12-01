import base64
import logging

from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import (
    load_der_public_key,
    load_pem_public_key,
    load_pem_private_key,
)


from typing import Union, Tuple

from .helper import (
    private_key_to_ed25519,
    multibase_58btc_encode,
    multibase_decode,
    split_according_to_fep8b32,
    jcs_sha356,
    multicodec_ed25519_public_bytes,
    multicodec_rsa_public_bytes,
)

logger = logging.getLogger(__name__)


@dataclass
class CryptographicSecret:
    """Represents a cryptographic secret. Such a secret is composed
    of the private key and the URI that resolves to the material, one
    can construct the appropriate cryptographic identifier from.

    :param key_id: The URI, where the corresponding public key and controller
        can be retrieved
    :param private_key: The signing material
    """

    key_id: str
    private_key: Union[ed25519.Ed25519PrivateKey, rsa.RSAPrivateKey]

    def sign(self, message: str):
        """Signs the message.

        Currently only implemented for RSA: Uses PKCS1v15 padding and SHA256
        hashes. Returns the signature as base64 encoded.

        **Warning**: Interface might change, to enable specifying encoding
        of the signature.

        :param message: The message to sign as UTF-8 encoded string."""

        if isinstance(message, str):
            message = message.encode("utf-8")

        if isinstance(self.private_key, rsa.RSAPrivateKey):
            return base64.standard_b64encode(
                self.private_key.sign(
                    message,
                    padding.PKCS1v15(),
                    hashes.SHA256(),
                )
            ).decode("utf-8")
        if isinstance(self.private_key, ed25519.Ed25519PrivateKey):
            return multibase_58btc_encode(self.private_key.sign(message))

        raise ValueError("Unknown key type in private key")

    def fep_8b32_sign(self, document: dict, created: str | None = None) -> dict:
        proof = {
            "created": created,
            "cryptosuite": "eddsa-jcs-2022",
            "proofPurpose": "assertionMethod",
            "type": "DataIntegrityProof",
            "verificationMethod": self.key_id,
        }
        digest = jcs_sha356(proof) + jcs_sha356(document)
        proof["proofValue"] = self.sign(digest)

        return {**document, "proof": proof}

    @staticmethod
    def from_pem(key_id: str, pem: str):
        """Creates a CryptographicSecret from a PEM encoded private key"""
        return CryptographicSecret(
            key_id, load_pem_private_key(pem.encode("utf-8"), password=None)
        )

    @staticmethod
    def from_multibase(key_id: str, multibase: str):
        """Creates a CryptographicSecret from multibase encoded
        Ed25519 private key and key_id"""
        return CryptographicSecret(key_id, private_key_to_ed25519(multibase))


@dataclass
class CryptographicIdentifier:
    """Represents a cryptographic identifier. The usage is: If an object is
    signed by `public_key`, then it is authored by `controller`. In order
    to discover which `CryptographicIdentifier` to use, one resolves another
    identifier `key_id`, which yields either a Multikey or a publicKey object, which
    can then be resolved into a CryptographicIdentifier.

    One should never need to directly access the properties of this class, instead
    verify returns the controller, if and only if the signature is valid.

    :param controller: The URI of the actor that controls the public key
    :param public_key: Public key used to verify signatures
    """

    controller: str
    public_key: Union[ed25519.Ed25519PublicKey, rsa.RSAPublicKey]

    def verify(self, message: str | bytes, signature: str | bytes) -> str | None:
        """Verifies that `signature` is a correct signature for the given message.

        **Warning**: Interface might change, to enable specifying encoding
        of the signature.

        :param message: The message string.
        :param signature: The signature

        :return: If the signature is valid the corresponding controller,
            otherwise null.
        """
        # Doing the encoding here is probably wrong ...
        # All these things are awkward

        if isinstance(signature, str):
            signature = base64.standard_b64decode(signature)

        if isinstance(message, str):
            message = message.encode("utf-8")

        if isinstance(self.public_key, rsa.RSAPublicKey):
            try:
                self.public_key.verify(
                    signature,
                    message,
                    padding.PKCS1v15(),
                    hashes.SHA256(),
                )
                return self.controller
            except InvalidSignature:
                return None

        if isinstance(self.public_key, ed25519.Ed25519PublicKey):
            try:
                self.public_key.verify(signature, message)
                return self.controller
            except InvalidSignature:
                return None

        raise ValueError("Unknown key type in public_key")

    def fep_8b32_verify(self, document: dict):
        pure_doc, pure_proof, signature = split_according_to_fep8b32(document)
        digest = jcs_sha356(pure_proof) + jcs_sha356(pure_doc)

        return self.verify(digest, signature)

    def as_tuple(self) -> Tuple[str, str]:
        """Transforms the CryptographicIdentifier into a tuple

        :return: controller, multibase/multicodec encoded public key"""
        if isinstance(self.public_key, rsa.RSAPublicKey):
            public_bytes = multicodec_rsa_public_bytes + self.public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            public_key = multibase_58btc_encode(public_bytes)
        else:
            public_key = multibase_58btc_encode(
                multicodec_ed25519_public_bytes
                + self.public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw,
                )
            )
        return (self.controller, public_key)

    @staticmethod
    def from_pem(public_key: str, owner: str):
        """Creates a CryptographicIdentifier from a pem encoded public key and the controller"""
        if public_key is None:
            return None
        return CryptographicIdentifier(
            controller=owner, public_key=load_pem_public_key(public_key.encode("utf-8"))
        )

    @staticmethod
    def from_multikey(multikey: dict):
        """Creates a CryptographicIdentifier from a Multikey, see

        * [FEP-521a: Representing actor's public keys](https://codeberg.org/fediverse/fep/src/branch/main/fep/521a/fep-521a.md)

        Example:

        ```json
        {
            "id": "https://server.example/users/alice#ed25519-key",
            "type": "Multikey",
            "controller": "https://server.example/users/alice",
            "publicKeyMultibase": "z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2"
        }
        ```
        """
        if multikey.get("type") != "Multikey":
            raise ValueError("Multikeys must have type 'Multikey'")

        controller = multikey.get("controller")
        public_key = multikey.get("publicKeyMultibase")

        if controller is None or public_key is None:
            raise ValueError(
                "Expected parameters controller and publicKeyMultibase to be present when parsing MultiKey"
            )

        return CryptographicIdentifier.from_tuple(controller, public_key)

    @staticmethod
    def from_tuple(controller: str, multibase_public_key: str):
        """Creates a CryptographicIdentifier from a tuple

        :param controller: The controller URI
        :parma multibase_public_key: The public key encoded using multibase/multicodex
        """
        public_key = multibase_decode(multibase_public_key)

        if public_key[:2] == multicodec_ed25519_public_bytes:
            return CryptographicIdentifier(
                controller=controller,
                public_key=ed25519.Ed25519PublicKey.from_public_bytes(public_key[2:]),
            )
        if public_key[:2] == multicodec_rsa_public_bytes:
            return CryptographicIdentifier(
                controller=controller,
                public_key=load_der_public_key(public_key[2:]),
            )

        raise ValueError("Unsupported public key format")

    @staticmethod
    def from_public_key(data: dict):
        """Creates a Cryptographic identifier from a publicKey object, example:

        ```json
        {
            "id": "https://com.example/issuer/123#main-key",
            "owner": "https://com.example/issuer/123",
            "publicKeyPem": "-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----"
        }
        ```
        """
        controller = data.get("owner")
        public_key = data.get("publicKeyPem")

        if controller is None or public_key is None:
            raise ValueError(
                "Expected parameters owner and publicKeyPem to be present when parsing publicKey"
            )

        return CryptographicIdentifier(
            controller=controller,
            public_key=load_pem_public_key(public_key.encode("utf-8")),
        )

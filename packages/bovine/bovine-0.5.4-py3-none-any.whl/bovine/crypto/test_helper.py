from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

from .helper import (
    content_digest_sha256,
    did_key_to_public_key,
    verify_signature,
    multibase_58btc_encode,
    multibase_decode,
    split_according_to_fep8b32,
)
from .test import private_key, public_key
from .types import CryptographicSecret


def test_content_digest_sha256():
    digest = content_digest_sha256("content")

    assert digest == "sha-256=7XACtDnprIRfIjV9giusFERzD722AW0+yUMil7nsn3M="


def test_did_to_public_key():
    did_example = "did:key:z6MkiTBz1ymuepAQ4HEHYSF1H8quG5GLVVQR3djdX3mDooWp"

    public_key = did_key_to_public_key(did_example)

    assert isinstance(public_key, ed25519.Ed25519PublicKey)
    assert (
        public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        == b";j'\xbc\xce\xb6\xa4-b\xa3\xa8\xd0*o\rse2\x15w\x1d\xe2C\xa6:\xc0H\xa1\x8bY\xda)"
    )


def test_crypto_sign_verify():
    message = "secret"

    secret = CryptographicSecret.from_pem("key", private_key)
    signature = secret.sign(message)

    assert verify_signature(public_key, message, signature)


def test_crypto_sign_verify_failure():
    message = "secret"

    assert not verify_signature(public_key, message, "")


def test_multibase_58btc_encode():
    message = "secret".encode("utf-8")
    result = multibase_58btc_encode(message)

    assert result == "zzTuS2beK"


def test_split_according_to_fep8b32():
    doc_base = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/data-integrity/v1",
        ],
        "type": "Create",
        "actor": "https://server.example/users/alice",
        "object": {"type": "Note", "content": "Hello world"},
    }
    pure_proof = {
        "type": "DataIntegrityProof",
        "cryptosuite": "eddsa-jcs-2022",
        "verificationMethod": "https://server.example/users/alice#ed25519-key",
        "proofPurpose": "assertionMethod",
        "created": "2023-02-24T23:36:38Z",
    }
    signature = "z3sXaxjKs4M3BRicwWA9peyNPJvJqxtGsDmpt1jjoHCjgeUf71TRFz56osPSfDErszyLp5Ks1EhYSgpDaNM977Rg2"

    input_doc = {**doc_base, "proof": {**pure_proof, "proofValue": signature}}

    doc, proof, sig = split_according_to_fep8b32(input_doc)

    assert doc == doc_base
    assert proof == pure_proof
    assert sig == multibase_decode(signature)

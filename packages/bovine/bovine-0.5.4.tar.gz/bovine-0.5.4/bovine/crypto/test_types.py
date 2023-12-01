import pytest

from .types import CryptographicIdentifier
from .test import public_key, did_key


@pytest.mark.parametrize(
    "example",
    [
        {},
        {"type": "Key"},
        {"type": "Multikey"},
        {"type": "Multikey", "controller": "controller"},
        {"type": "Multikey", "publicKeyMultibase": "zxxx"},
        {"type": "Multikey", "controller": "controller", "publicKeyMultibase": "zxxx"},
    ],
)
def test_remote_identity_from_multikey_error(example):
    with pytest.raises(ValueError):
        CryptographicIdentifier.from_multikey(example)


def test_remote_identity_from_multikey():
    public_key_ed25519 = did_key.removeprefix("did:key:")
    controller = "https://com.example/issuer/123"
    multikey = {
        "id": f"{controller}#key-0",
        "type": "Multikey",
        "controller": controller,
        "publicKeyMultibase": public_key_ed25519,
    }

    identity = CryptographicIdentifier.from_multikey(multikey)

    assert identity.controller == controller

    signature = "0gHDz8Qn4+8gWC/byjTk7yvJxL0p4kiUSdxt6VZQvWQ9MBlRThMBDSrgJsNPHZWNMXtPSoL9+r0k\n3cUwYmIWDA=="

    assert identity.verify("moo", signature)
    assert identity.as_tuple() == (controller, public_key_ed25519)


def test_remote_identity_from_multikey_rsa():
    controller = "https://com.example/issuer/123"
    public_key_rsa = "z4MXj1wBzi9jUstyQ1t9N9BHZpoQb4FQpaUfcc61XQigH9ua5R9aEN7YMK81PTKgWLGZXMqvy9eP4X42KgEsmNnZrwQbeT5R8oKhMHVQ5qcwTFwdX2gQeZLLDkUDJL3aJqmqSLK7mrgZ1CskMyD4p8eqFEUW1oufy9cE6Wyz7TQZFKpSCd1oY8HNue9cNRthZzXCdoX6DGVyewBFdivkohE1mhU1EpbKSYH66rx1cZpa6PJKzg4LbKSUqhHaftmsD1jWzFrKNUFzRmCGsihAjLVgsfjPaPmBUXNjYTFg1nCHWCGVGD3g9NhBwGiuu4vQR5PQfD6BCPZpGTaUZjWgZTHveef1pUDPvsCRuGDoGvrTnG8k7SeQp"
    multikey = {
        "id": f"{controller}#key-0",
        "type": "Multikey",
        "controller": controller,
        "publicKeyMultibase": public_key_rsa,
    }

    identity = CryptographicIdentifier.from_multikey(multikey)

    assert identity.controller == controller
    assert identity.as_tuple()[0] == controller

    identity_too = CryptographicIdentifier.from_tuple(*identity.as_tuple())

    assert identity.public_key == identity_too.public_key


@pytest.mark.parametrize(
    "example",
    [
        {},
        {"owner": "owner"},
        {"publicKeyPem": "xxxx"},
        {"owner": "owner", "publicKeyPem": "xxxx"},
    ],
)
def test_remote_identity_from_public_key_error(example):
    with pytest.raises(ValueError):
        CryptographicIdentifier.from_public_key(example)


def test_remote_identity_from_public_key():
    controller = "https://com.example/issuer/123"

    public_key_dict = {
        "id": f"{controller}/main-key",
        "owner": controller,
        "publicKeyPem": public_key,
    }

    identity = CryptographicIdentifier.from_public_key(public_key_dict)

    assert identity.controller == controller

    signature = "vaSYmwpEhGhB/o5QNC8MxYbJeBKDDiaZG0J4EsN0V/5+bFRgPbFK1oUgrdkiTT+farWXdVagPvIg44M/IYjPY8oExBS3mCt9oXDDWiDfBED8n2yrGHV6X/GWNxWUarmo4RcOBU2xWy9982/ZH+UyiPVEpanPi4REf9UYiF0dciZK1Yx3Nkqadnm9XTJJISHX4v88jkUGYaNnWcJ+SJMXuqklYJU/j8j4FVvf3vbFvuwGX1W5o7Zmk89xdJeRiGPYCM2zUgfzGoDHdVHuX8ksR+/xjzwLxMn/SerHuKSCzYivCpaxUqmX0VMTEwvPZ2H+hvXsqyLgR+zFnL7WdX6p7Q=="

    assert identity.verify("secret", signature)
    assert not identity.verify("secret", "")

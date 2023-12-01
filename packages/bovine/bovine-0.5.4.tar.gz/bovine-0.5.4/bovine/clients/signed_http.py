import aiohttp
import bovine.clients.signed_http_methods

from bovine.crypto.types import CryptographicSecret


class SignedHttpClient:
    """Client for using HTTP Signatures"""

    def __init__(self, session, public_key_url, private_key, account_url=None):
        self.session = session
        self.account_url = account_url
        self.secret = CryptographicSecret.from_pem(public_key_url, private_key)

    def set_session(self, session):
        self.session = session

        return self

    async def get(self, url, headers={}) -> aiohttp.ClientResponse:
        """Retrieves url using a signed get request"""
        return await bovine.clients.signed_http_methods.signed_get(
            self.session, self.secret, url, headers
        )

    async def post(self, url, body, headers={}, content_type=None):
        """Posts to url using a signed post request"""
        return await bovine.clients.signed_http_methods.signed_post(
            self.session,
            self.secret,
            url,
            body,
            headers,
            content_type=content_type,
        )

    def event_source(self, url):
        return bovine.clients.signed_http_methods.signed_event_source(
            self.session, self.secret, url
        )

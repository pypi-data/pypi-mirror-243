"""avoid SSLError due to UNSAFE_LEGACY_RENEGOTIATION_DISABLED

from https://stackoverflow.com/a/71646353/21997874
"""

import ssl
import urllib3
import requests.adapters


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """Transport adapter that allows us to use custom ssl_context."""
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ctx.options |= 0x4
adapter = CustomHttpAdapter(ctx)


def make_session_sslerror_free(session: requests.Session, prefix: str = 'https://') -> None:
    session.mount(prefix, adapter)

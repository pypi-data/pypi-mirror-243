from __future__ import annotations

from requests.models import Response

from .souptoolsclass import SoupTools


class ResponseProxy(Response, SoupTools):
    def __init__(self, response):
        state = response.__reduce__()[2]
        self.__setstate__(state)  # type: ignore
        self.response = response

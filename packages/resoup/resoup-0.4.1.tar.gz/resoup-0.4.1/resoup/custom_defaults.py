import functools

from . import api_with_tools


class CustomDefaults:
    def __init__(
        self,
        **kwargs
    ) -> None:
        self.defaults = kwargs

    def __getattr__(self, name):
        return functools.partial(getattr(api_with_tools, name), **self.defaults)

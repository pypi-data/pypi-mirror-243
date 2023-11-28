from typing import Text, Union, Dict

from .Response import Response


def get(
        url: str | bytes,
        params: Dict | None = ...,
        headers: Dict | None = ...,
        cookies: None | Dict = ...,
        files=...,
        auth=...,
        timeout: int | None = ...,
        allow_redirects: bool = ...,
        proxies: Dict | None = ...,
        hooks=...,
        stream: bool | None = ...,
        verify: bool | None = ...,
        cert=...,
        json: Dict | None = ...,
) -> Response: ...


def post(url: Text,
         data=Union[Dict, Text],
         headers=Union[Dict, Text],
         **kwargs) -> Response: ...


def session_get(url: Text,
                params=Union[Dict, Text],
                headers=Union[Dict, Text],
                **kwargs) -> Response: ...


def session_post(url: Text,
                 data=Union[Dict, Text],
                 headers=Union[Dict, Text],
                 **kwargs) -> Response: ...

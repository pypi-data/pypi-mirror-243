from types import TracebackType
from typing import Optional, Type
import httpx

from ...base.http import Request, Response
from .base import SyncHttp



class SyncHttpxSession(SyncHttp):
    def __init__(self) -> None:
        self.__client = httpx.Client()

    def __enter__(self) -> SyncHttp:
        self.__client.__enter__()
        return self

    def __exit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        self.__client.__exit__(__exc_type, __exc_value, __traceback)

    def fetch(self, request: Request) -> Response:
        resp = self.__client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            content=request.content
        )
        return Response(
            status=resp.status_code,
            content=resp.content,
        )

    def close(self) -> None:
        self.__client.close()

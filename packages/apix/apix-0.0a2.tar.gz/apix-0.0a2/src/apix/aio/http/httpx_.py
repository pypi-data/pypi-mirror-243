from types import TracebackType
from typing import Optional, Type
import httpx

from ...base import Request, Response
from .base import AsyncHttp


class AsyncHttpxSession(AsyncHttp):
    def __init__(self) -> None:
        self.__client = httpx.AsyncClient()

    async def __aenter__(self) -> AsyncHttp:
        await self.__client.__aenter__()
        return self

    async def __aexit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        await self.__client.__aexit__(__exc_type, __exc_value, __traceback)

    async def fetch(self, request: Request) -> Response:
        resp = await self.__client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            content=request.content,
        )
        return Response(
            status=resp.status_code,
            content=resp.content,
        )

    async def close(self) -> None:
        await self.__client.aclose()

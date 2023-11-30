from types import TracebackType
from typing import Optional, Type, overload
from ..base import Async, ProtoHttp, ProtoPath, T, BaseClient
from .http.base import AsyncHttp


class AsyncClient(BaseClient[Async]):
    http: AsyncHttp
    
    async def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = self._build_request(path, **kwargs)
        response = await self.http.fetch(request)
        self._check_response(response)
        return self._build_result(response, path)

    async def __aenter__(self) -> "AsyncClient":
        await self.http.__aenter__()
        return self

    async def __aexit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        await self.http.__aexit__(__exc_type, __exc_value, __traceback)


    @staticmethod
    def default_http() -> ProtoHttp[Async]:
        from .http.httpx_ import AsyncHttpxSession

        return AsyncHttpxSession()

from types import TracebackType
from typing import Optional, Type
from ..base import Sync, ProtoHttp, ProtoPath, T, BaseClient
from .http.base import SyncHttp


class SyncClient(BaseClient[Sync]):
    http: SyncHttp
    
    def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = self._build_request(path, **kwargs)
        response = self.http.fetch(request)
        self._check_response(response)
        return self._build_result(response, path)

    def __enter__(self) -> "SyncClient":
        self.http.__enter__()
        return self

    def __exit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        self.http.__exit__(__exc_type, __exc_value, __traceback)

    @staticmethod
    def default_http() -> ProtoHttp[Sync]:
        from .http.httpx_ import SyncHttpxSession

        return SyncHttpxSession()

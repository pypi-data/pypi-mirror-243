import abc
from ...base.proto import ProtoHttp, Async
from contextlib import AbstractAsyncContextManager


class AsyncHttp(ProtoHttp[Async], AbstractAsyncContextManager):
    @abc.abstractmethod
    async def close(self) -> None: ...

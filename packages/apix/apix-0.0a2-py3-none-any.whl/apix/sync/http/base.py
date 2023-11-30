import abc
from ...base.proto import ProtoHttp, Sync
from contextlib import AbstractContextManager


class SyncHttp(ProtoHttp[Sync], AbstractContextManager):
    @abc.abstractmethod
    def close(self) -> None: ...

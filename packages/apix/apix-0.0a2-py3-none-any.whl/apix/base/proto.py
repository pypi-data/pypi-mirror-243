from __future__ import annotations

import typing

from .http import PathInfo, Request, Response


class Operation: ...
class Sync(Operation): ...
class Async(Operation): ...

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
OP = typing.TypeVar("OP")
OP_co = typing.TypeVar("OP_co", covariant=True)


class ProtoSerializer(typing.Protocol):
    def to_json(self, obj: typing.Any) -> bytes: ...
    def from_json(self, data: bytes, type: typing.Type[T]) -> T: ...
    def to_builtins(self, obj: typing.Any) -> typing.Dict[str, typing.Any]: ...
    def to_type(self, obj: typing.Any, type: typing.Type[T]) -> T: ...


class ProtoSchema(typing.Protocol): ...


class ProtoPath(typing.Protocol[T_co]):
    __info__: typing.ClassVar[PathInfo]
    
    def build_request(self, client: ProtoClient) -> Request: ...
    def build_result(self, response: Response, client: ProtoClient) -> T_co: ...
    def check_response(self, response: Response) -> Response: ...


class ProtoHttp(typing.Protocol[OP_co]):
    @typing.overload
    def fetch(self: ProtoHttp[Sync], request: Request) -> Response: ...

    @typing.overload
    async def fetch(self: ProtoHttp[Async], request: Request) -> Response: ...

    @typing.overload
    def close(self: ProtoHttp[Sync]) -> None: ...

    @typing.overload
    async def close(self: ProtoHttp[Async]) -> None: ...


class ProtoConfig(typing.Protocol[OP]):
    base_url: str
    serializer: ProtoSerializer
    http: typing.Optional[ProtoHttp[OP]]


class ProtoClient(typing.Protocol[OP]):
    @typing.overload
    def __call__(self: ProtoClient[Sync], path: ProtoPath[T], **kwargs) -> T: ...

    @typing.overload
    async def __call__(self: ProtoClient[Async], path: ProtoPath[T], **kwargs) -> T: ...

    @property
    def config(self) -> ProtoConfig[OP]: ...

    @property
    def http(self) -> ProtoHttp: ...

    @staticmethod
    def default_http() -> ProtoHttp[OP]: ...

    def build_url(self, path: ProtoPath[T]) -> str: ...

import typing
import msgspec

from ..base import T, ProtoSerializer, ProtoClient, PathInfo, Request, Response
from .base import build_request, build_result, check_response


class MsgspecSchema(msgspec.Struct):
    ...


class MsgspecPath(msgspec.Struct, typing.Generic[T]):
    __info__: typing.ClassVar[PathInfo] = PathInfo()

    def build_request(self, client: ProtoClient) -> Request:
        return build_request(self, client)

    def build_result(self, response: Response, client: ProtoClient) -> T:
        return build_result(self, response, client)

    def check_response(self, response: Response) -> Response:
        return check_response(response)


class MsgspecSerializer(ProtoSerializer):
    def __init__(self) -> None:
        self.__encoder = msgspec.json.Encoder()

    def to_json(self, obj) -> bytes:
        return self.__encoder.encode(obj)

    def from_json(self, data, type: typing.Type[T]) -> T:
        return msgspec.json.decode(data, type=type)

    def to_builtins(self, obj) -> typing.Dict[str, typing.Any]:
        return msgspec.to_builtins(obj)

    def to_type(self, obj: typing.Any, type: typing.Type[T]) -> T:
        return msgspec.convert(obj, type=type)

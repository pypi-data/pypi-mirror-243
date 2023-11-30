import typing
import dataclasses

from .proto import OP, ProtoHttp, ProtoSerializer, ProtoConfig


def default_serializer() -> ProtoSerializer:
    from ..serializer.default import Serializer

    return Serializer()


@dataclasses.dataclass
class ClientConfig(ProtoConfig[OP]):
    base_url: str = "https://api.example.com"
    serializer: ProtoSerializer = dataclasses.field(
        default_factory=default_serializer)
    http: typing.Optional[ProtoHttp[OP]] = None

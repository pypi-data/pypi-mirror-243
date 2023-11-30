import typing
import dataclasses


@dataclasses.dataclass
class Request:
    method: str
    url: str
    content: typing.Optional[bytes] = None
    params: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Response:
    status: int
    content: bytes
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class PathInfo:
    method: str = "GET"
    path: str = "/"
    type: typing.Type = bool
    path_params: typing.List[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.path_params = [
            param[1:-1]
            for param in self.path.split("/") 
            if param.startswith("{") and param.endswith("}")
        ]

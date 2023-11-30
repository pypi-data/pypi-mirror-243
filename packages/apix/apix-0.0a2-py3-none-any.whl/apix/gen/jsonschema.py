import typing
import msgspec


JSON2PY = {
    "integer": int,
    "number": float,
    "string": str,
    "boolean": bool,
    "object": dict,
    "array": list,
    "null": None
}


class JsonSchema(msgspec.Struct):
    type: typing.Optional[str]

import os

APIX_SERIALIZER = os.getenv("APIX_SERIALIZER", "msgspec")


if APIX_SERIALIZER == "msgspec":
    from .msgspec_ import (
        MsgspecSchema as Schema,
        MsgspecSerializer as Serializer,
        MsgspecPath as Path,
    )
    from msgspec import field

else:
    from .msgspec_ import (
        MsgspecSchema as Schema,
        MsgspecSerializer as Serializer,
        MsgspecPath as Path,
    )
    from msgspec import field


__all__ = [
    "Schema",
    "Serializer",
    "Path",
    "field",
]

# apix

## Example

```python
# models.py
from apix import Schema, Path, PathInfo

class Data(Schema):
    key: str
    value: str

class GetData(Path[Data]):
    __info__ = PathInfo("GET", "/data", Data)
    key: str

# sync.py
from apix.sync import SyncClient

class MySyncClient(SyncClient):
    def get_data(self, key: str) -> Data:
        return self(GetData(key=key))


# main.py
from apix import Config

with MySyncClient(Config(base_url="https://my.api")) as client:
    print(client.get_data("Key")) # "Value"

```


## Serializers

- [msgspec](https://jcristharif.com/msgspec/index.html)

## Http Clients

- [httpx](https://www.python-httpx.org/)

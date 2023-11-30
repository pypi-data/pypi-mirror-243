import logging
import typing

from .proto import ProtoClient, OP, ProtoConfig, ProtoHttp, ProtoPath, T
from .http import Response, Request
from .config import ClientConfig

log = logging.getLogger(__name__)


class BaseClient(ProtoClient[OP]):
    def __init__(
            self, 
            config: typing.Optional[ProtoConfig] = None
    ) -> None:
        self._http: typing.Optional[ProtoHttp[OP]]
        self._config = config or ClientConfig()
        if self._config.http is None:
            self._http = self.default_http()
        else:
            self._http = None

    @property
    def config(self) -> ProtoConfig:
        return self._config
    
    @property
    def http(self) -> ProtoHttp[OP]:
        if _http := self._http or self.config.http:
            return _http
        raise RuntimeError("Client is not initialized http")

    def build_url(self, path: ProtoPath[T]) -> str:
        return self.config.base_url + path.__info__.path
    
    def _build_request(self, path: ProtoPath[T], **kwargs) -> Request:
        return path.build_request(self)
    
    def _check_response(self, response: Response):
        pass

    def _build_result(self, response: Response, path: ProtoPath[T]) -> T:
        log.debug(f"Response: {response}")
        return path.build_result(response, self)

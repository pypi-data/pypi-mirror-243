from abc import ABCMeta
from typing import Dict, Union, Any

from project_utils.exception import ConfigException


class BaseConfig(metaclass=ABCMeta):
    __instance__: Any = None
    host: str
    port: int

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, port: str, host: str = "0.0.0.0"):
        assert port.isdigit(), ConfigException("params port type required integer!")
        self.host = host
        self.port = int(port)

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "host": self.host,
            "port": self.port
        }

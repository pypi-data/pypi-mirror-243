from typing import Dict, Union

from project_utils.exception import ConfigException
from .base_config import BaseConfig


class RedisConfig(BaseConfig):
    password: str
    db: int

    def __init__(self, host: str, password: str, db: str, port: str = "6379"):
        assert db.isdigit(), ConfigException("params db type required integer!")
        super().__init__(host=host, port=port)
        self.password = password
        self.db = int(db)

    def to_dict(self) -> Dict[str, Union[str, int]]:
        result: Dict[str, Union[str, int]] = super().to_dict()
        result.update({
            "password": self.password,
            "db": self.db
        })
        return result

    def to_url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"

from .path_config import Path
from .addr_config import Mysql, Redis, Kafka, Hbase

from typing import Any


class BaseConfig:
    __instance__: Any
    base_config: Path = Path()
    mysql_config: Mysql
    redis_config: Redis
    kafka_config: Kafka
    hbase_config: Hbase

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    @classmethod
    def load_path(cls, *args, **kwargs):
        cls.base_config.load(*args, **kwargs)

    @classmethod
    def load_mysql(cls, *args, **kwargs):
        cls.mysql_config = Mysql(*args, **kwargs)

    @classmethod
    def load_redis(cls, *args, **kwargs):
        cls.redis_config = Redis(*args, **kwargs)

    @classmethod
    def load_kafka(cls, *args, **kwargs):
        cls.kafka_config = Kafka(*args, **kwargs)

    @classmethod
    def load_hbase(cls, *args, **kwargs):
        cls.hbase_config = Hbase(*args, **kwargs)

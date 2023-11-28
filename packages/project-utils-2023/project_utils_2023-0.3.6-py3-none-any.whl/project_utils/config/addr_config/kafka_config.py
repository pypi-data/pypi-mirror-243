from typing import List, Optional, Dict, Union

from .base_config import BaseConfig


class KafkaConfig(BaseConfig):
    bootstrap_servers: List[str]
    topic: str
    group: Optional[str]

    def __init__(self, bootstrap_servers: str, topic: str, group: Optional[str] = None):
        super().__init__(port="0")
        self.bootstrap_servers = bootstrap_servers.split(";")
        self.topic = topic
        if group: self.group = group

    def to_dict(self) -> Dict[str, Union[str, int, List[str]]]:
        result: Dict[str, Union[str, int, List[str]]] = {
            "bootstrap_servers": self.bootstrap_servers,
            "topic": self.topic,
        }
        if self.group:
            result['group'] = self.group
        return result

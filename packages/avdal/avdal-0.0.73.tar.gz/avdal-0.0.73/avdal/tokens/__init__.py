from typing import Dict
from datetime import datetime


class Token():
    def __init__(self,
                 kind: str = None,
                 key: str = None,
                 lifetime: int = None,
                 counter: int = None,
                 props: Dict = None,
                 metadata: Dict = None,
                 timestamp: int = None):

        self.kind = kind
        self.key = key
        self.lifetime = lifetime
        self.counter = counter
        self.props = props
        self.metadata = metadata
        self.timestamp = timestamp or int(datetime.utcnow().timestamp() * 1e9)

        self._created = datetime.utcfromtimestamp(self.timestamp / 1e9)

    def seconds_left(self):
        if self.lifetime is None:
            return None

        offset = int((self._created - datetime.utcnow()).total_seconds())

        return offset + self.lifetime

    def auto_fields(self):
        metadata = {}
        for k, v in self.metadata.items():
            if not k.startswith("_"):
                metadata[k] = v

        return {
            "kind": self.kind,
            "key": self.key,
            "created": str(self._created),
            "seconds_left": self.seconds_left(),
            "lifetime": self.lifetime,
            "counter": self.counter,
            "props": self.props,
            "metadata": metadata
        }

    def dict(self):
        return {
            "kind": self.kind,
            "key": self.key,
            "timestamp": self.timestamp,
            "lifetime": self.lifetime,
            "counter": self.counter,
            "props": self.props,
            "metadata": self.metadata
        }

    def __str__(self):
        return f"{self.kind}:{self.key}"

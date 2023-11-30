from .. import Token
from abc import ABC, abstractmethod

class TokenStore(ABC):
    @abstractmethod
    def get_token(self, kind: str, key: str) -> Token:
        raise NotImplementedError()

    @abstractmethod
    def add_token(self, token: Token) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_token(self, kind: str, key: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def decrement(self, token: Token) -> None:
        raise NotImplementedError()

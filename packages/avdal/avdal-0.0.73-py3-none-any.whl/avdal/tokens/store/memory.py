from ..token import Token
from . import TokenStore
from util.error import NotFound, Gone

# TODO: check expiration time and counter 

class MemTokenStore(TokenStore):
    def __init__(self):
        self.tokens: Dict[str, Dict[str, Token]] = {}

    def get_token(self, kind: str, key: str) -> Token:
        if kind not in self.tokens:
            raise NotFound(f"kind: {kind}")

        if key not in self.tokens[kind]:
            raise NotFound(f"key: {key}")

        return self.tokens[kind][key]

    def add_token(self, token: Token) -> None:
        if token.kind not in self.tokens:
            self.tokens[token.kind] = {}

        self.tokens[token.kind][token.key] = token

    def delete_token(self, kind: str, key: str) -> None:
        if kind not in self.tokens:
            raise NotFound(f"kind: {kind}")

        if key not in self.tokens[kind]:
            raise NotFound(f"key: {key}")

        del self.tokens[kind][key]

    def decrement(self, token: Token) -> None:
        if token.kind not in self.tokens:
            raise NotFound(f"kind: {token.kind}")

        if token.key not in self.tokens[token.kind]:
            raise NotFound(f"key: {token.key}")

        self.tokens[token.kind][token.key].counter -= 1


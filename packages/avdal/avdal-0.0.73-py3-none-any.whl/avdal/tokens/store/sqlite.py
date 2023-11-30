from token import Token
from store import TokenStore
import sqlite3
from peewee import *

class SQLiteTokenStore:
    def __init__(self, logger, db_path: str):
        self.logger = logger
        self.tokens = {}

        db = SqliteDatabase(db_path)
        db.bind([Token])
        db.create_tables([Token])

        for token in Token.select().execute():
            self._cache_add(token)

    def _cache_add(self, token):
        self.tokens[(token.kind, token.key)] = token

    def _cache_remove(self, kind: str, key: str):
        id = (kind, key)
        if id not in self.tokens:
            raise NotFound(id)

        del self.tokens[id]

    def _cache_get(self, kind: str, key: str):
        id = (kind, key)
        if id not in self.tokens:
            raise NotFound(id)

        return self.tokens[id]

    def get_token(self, kind: str, key: str) -> Token:
        token = self._cache_get(kind, key)

        if (token.seconds_left() or 1) < 0:
            self.logger.info(f"deleting expired token [{token}]")
            self.delete_token(token.kind, token.key)
            raise Gone(token)

        self._decrement(token)

        return token

    def add_token(self, token: Token) -> None:
        token.upsert()
        self._cache_add(token)

        return None

    def _decrement(self, token: Token) -> None:
        if token.counter is None:
            return

        token.counter -= 1
        self.logger.info(f"decremented counter of token [{token}] to [{token.counter}]")

        if token.counter == 0:
            self.logger.info(f"deleting token [{token}] with zero counter")
            self.delete_token(token.kind, token.key)
            return

        token.save()
        self.logger.info(f"updated counter of token [{token}] in database")

    def delete_token(self, kind: str, key: str) -> None:
        Token.delete().where(Token.kind == kind, Token.key == key).execute()
        self._cache_remove(kind, key)

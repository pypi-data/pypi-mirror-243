import boto3
from ..token import Token
from . import TokenStore
from util.error import NotFound, Gone

class DynamoDbStore(TokenStore):
    def __init__(self, logger, kid: str, secret: str, region_name: str, table_name: str):
        self.logger = logger

        self.client = boto3.resource("dynamodb",
                                     region_name=region_name,
                                     aws_access_key_id=kid,
                                     aws_secret_access_key=secret)

        self.table = self.client.Table(table_name)

    def get_token(self, kind: str, key: str) -> Token:
        response = self.table.get_item(Key={"kind": kind, "key": key})
        if "Item" not in response:
            raise NotFound(f"kind: {kind}, key: {key}")

        for field in ["counter", "lifetime", "timestamp"]:
            val = response["Item"].get(field)
            if val is not None:
                response["Item"][field] = int(val)

        token = Token(**response["Item"])

        if (token.seconds_left() or 1) < 0:
            self.logger.info(f"deleting expired token [{token}]")
            self.delete_token(token.kind, token.key)

            raise Gone(token)

        self.decrement(token)

        return token

    def add_token(self, token: Token) -> None:
        self.table.put_item(Item=token.dict())

    def delete_token(self, kind: str, key: str) -> None:
        self.table.delete_item(Key={"kind": kind, "key": key})
        self.logger.info(f"deleted token [{kind}, {key}]")

    def decrement(self, token: Token) -> None:
        if token.counter is None:
            return

        token.counter -= 1
        self.logger.info(f"decremented counter of token [{token}] to [{token.counter}]")

        if token.counter == 0:
            self.logger.info(f"deleting token [{token}] with zero counter")
            self.delete_token(token.kind, token.key)
            return

        self.table.update_item(Key={"kind": token.kind, "key": token.key},
                               UpdateExpression="SET #counter = :c",
                               ExpressionAttributeValues={":c": token.counter},
                               ExpressionAttributeNames={"#counter": "counter"})

        self.logger.info(f"updated counter of token [{token}] in database")

import logging
from decimal import Decimal
from functools import cached_property

import boto3

logger = logging.getLogger(__name__)

MESSAGE_ATTRIBUTES_TYPE = {
    str: "String",
    int: "Number",
    Decimal: "Number",
    float: "Number",
    bytes: "Binary",
    list: "String.Array",
    tuple: "String.Array",
}

FALLBACK_MESSAGE_ATTRIBUTES_TYPE = "String"


# noinspection PyMethodMayBeStatic
class BaseDynamoDBClient:
    def __init__(
        self,
        topic_name=None,
        log_level="debug",
        region_name="us-east-1",
        profile_name=None,
    ):
        self.topic_name = topic_name
        self.log_level = log_level
        self.region_name = region_name
        self.profile_name = profile_name

    @property
    def log(self):
        return getattr(logger, self.log_level)


class DynamoDBClient(BaseDynamoDBClient):
    @cached_property
    def client(self):
        session = boto3.Session(
            region_name=self.region_name, profile_name=self.profile_name
        )
        return session.client("dynamodb")

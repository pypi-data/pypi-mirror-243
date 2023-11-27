"""pyaslengine.aws.services.ecs"""

from typing import Callable

from attrs import define, field

from pyaslengine.aws.services import AWSService
from pyaslengine.data import JSON
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class AWSSNSPublish(AWSService):
    @staticmethod
    def arn_match(arn: str):
        if arn.startswith("arn:aws:states:::sns:publish"):
            return True
        return False

    def get_registered_resource(self) -> Callable | None:
        raise NotImplementedError()

    def call_registered_resource(self) -> JSON:
        raise NotImplementedError()

    @staticmethod
    def call_aws_service(parameters, context) -> JSON:
        logger.warning("SNS not yet supported, but not raising, returning {}")
        return {}

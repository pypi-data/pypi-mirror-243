"""pyaslengine.aws.services.base"""

from abc import ABC, abstractmethod
from typing import Callable

from attrs import define, field

from pyaslengine.data import JSON
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class AWSService:
    resource: str = field(default=None)
    parameters: JSON = field(default=None)
    context: JSON | None = field(default=None)
    registered_resources: dict = field(default=None)

    @staticmethod
    @abstractmethod
    def arn_match(arn: str) -> bool:
        pass

    @staticmethod
    def get_service(arn: str) -> type["AWSService"]:
        for service_cls in AWSService.__subclasses__():
            if service_cls.arn_match(arn):
                return service_cls
        raise NotImplementedError(
            f"Some AWS services not yet supported, cannot invoke: {arn}"
        )

    @abstractmethod
    def get_registered_resource(self) -> Callable | None:
        pass

    @abstractmethod
    def call_registered_resource(self) -> JSON:
        pass

    @staticmethod
    @abstractmethod
    def call_aws_service(parameters, context) -> JSON:
        pass

    def run(self) -> JSON:
        if self.get_registered_resource():
            return self.call_registered_resource()
        return self.call_aws_service(self.parameters, self.context)

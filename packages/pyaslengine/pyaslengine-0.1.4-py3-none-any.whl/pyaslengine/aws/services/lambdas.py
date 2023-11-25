"""pyaslengine.aws.services.lambdas"""

import json
from typing import Callable

from attrs import define, field
import boto3

from pyaslengine.aws.services import AWSService
from pyaslengine.data import JSON
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class AWSLambda(AWSService):
    @staticmethod
    def arn_match(arn: str):
        if arn.startswith("arn:aws:states:::lambda:invoke"):
            return True
        return False

    def get_registered_resource(self) -> Callable | None:
        function_name = self.parameters["FunctionName"]
        if registered_function := self.registered_resources.get(function_name):
            return registered_function

    def call_registered_resource(self):
        registered_resource = self.get_registered_resource()
        payload = self.parameters["Payload"]
        return registered_resource(payload, json.dumps(self.context))

    @staticmethod
    def call_aws_service(parameters, context) -> JSON:
        lambda_client = boto3.client("lambda")
        function_name = parameters["FunctionName"]
        payload = parameters["Payload"]
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),  # NOTE: automatically parsed by lambda in AWS
            # ClientContext=json.dumps(context),  # TODO: uncomment and enable
        )
        payload_response = json.loads(response["Payload"].read().decode("utf-8"))
        return {"Payload": payload_response}

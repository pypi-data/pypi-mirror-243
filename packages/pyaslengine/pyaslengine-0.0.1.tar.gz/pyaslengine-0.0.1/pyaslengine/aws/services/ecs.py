"""pyaslengine.aws.services.ecs"""

from typing import Callable

from attrs import define, field

from pyaslengine.aws.services import AWSService
from pyaslengine.data import JSON
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class AWSECSTask(AWSService):
    @staticmethod
    def arn_match(arn: str):
        if arn.startswith("arn:aws:states:::ecs:runTask"):
            return True
        return False

    def get_registered_resource(self) -> Callable | None:
        task_definition = self.parameters["TaskDefinition"]
        if registered_function := self.registered_resources.get(task_definition):
            return registered_function

    def call_registered_resource(self) -> JSON:
        raise NotImplementedError()

    @staticmethod
    def call_aws_service(parameters, context) -> JSON:
        import boto3
        import time

        ecs_client = boto3.client("ecs")
        cluster = parameters["Cluster"]
        task_definition = parameters["TaskDefinition"]
        subnets = parameters["NetworkConfiguration"]["AwsvpcConfiguration"]["Subnets"]
        security_groups = parameters["NetworkConfiguration"]["AwsvpcConfiguration"][
            "SecurityGroups"
        ]

        # NOTE: this is only problematic for serialization purposes...
        #   with a proper marshmallow schema, this and above could be removed
        if len(parameters["Overrides"]["ContainerOverrides"]) > 1:
            raise NotImplementedError(
                "Currently only one container per ECS task is supported"
            )
        container_name = parameters["Overrides"]["ContainerOverrides"][0]["Name"]
        container_command = parameters["Overrides"]["ContainerOverrides"][0]["Command"]

        response = ecs_client.run_task(
            cluster=cluster,
            launchType="FARGATE",
            taskDefinition=task_definition,
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": subnets,
                    "securityGroups": security_groups,
                    "assignPublicIp": "ENABLED",
                }
            },
            overrides={
                "containerOverrides": [
                    {
                        "name": container_name,
                        "command": container_command,
                    },
                ],
            },
        )

        if response.get("tasks"):
            task_arn = response["tasks"][0]["taskArn"]
            while True:
                describe_response = ecs_client.describe_tasks(
                    cluster=cluster, tasks=[task_arn]
                )
                task_status = describe_response["tasks"][0]["lastStatus"]
                logger.info(f"ECS TASK STATUS: {task_status}")
                if task_status == "STOPPED":
                    break
                time.sleep(10)
            logger.debug(f"Task {task_arn} has completed.")
        else:
            logger.debug("Failed to start task.")

        if response.get("failures"):
            logger.error(f"Failures: {response['failures']}")
            raise RuntimeError("ECS task failed with errors")

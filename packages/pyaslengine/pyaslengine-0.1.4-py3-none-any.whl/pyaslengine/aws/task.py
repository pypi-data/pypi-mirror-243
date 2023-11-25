"""pyaslengine.aws.task"""

from pyaslengine.data import JSON
from pyaslengine.log import get_logger

from pyaslengine.aws.services import AWSService

logger = get_logger(__name__)


class AWSTaskInvoker:
    @classmethod
    def invoke(
        cls,
        resource: str,
        parameters: JSON,
        context: JSON,
        registered_resources: dict,
    ) -> JSON:
        service = AWSService.get_service(resource)(
            resource=resource,
            parameters=parameters,
            context=context,
            registered_resources=registered_resources,
        )
        return service.run()

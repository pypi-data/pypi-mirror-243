"""pyaslengine.workflows"""

import json
import re
from typing import TYPE_CHECKING

from attrs import define, field
import boto3

from pyaslengine.log import get_logger
from pyaslengine.data import (
    Context,
    WorkflowInput,
    WorkflowOutput,
    StateInput,
    StateOutput,
    JSON,
)
from pyaslengine.patch.states import StatePatch
from pyaslengine.states import (
    State,
    Choice,
    Task,
    Map,
    Fail,
    Succeed,
    Pass,
    Wait,
    Parallel,
)

if TYPE_CHECKING:
    from pyaslengine.schemas import StateMachineSchema

logger = get_logger(__name__)


@define
class Workflow:
    comment: str = field(default=None)
    start_at: str = field(default=None)
    states: dict[str, State] = field(default=None)

    @classmethod
    @property
    def schema(self) -> type["StateMachineSchema"]:
        """Provide schema via property"""
        from pyaslengine.schemas import StateMachineSchema

        return StateMachineSchema

    @classmethod
    def load_definition_file(cls, definition_filepath) -> "StateMachine":
        with open(definition_filepath) as f:
            return cls.schema().load(json.load(f))

    @classmethod
    def load_aws_arn(cls, step_function_arn) -> "StateMachine":
        client = boto3.client("stepfunctions")
        response = client.describe_state_machine(stateMachineArn=step_function_arn)
        state_machine_definition = response["definition"]
        return cls.schema().load(json.loads(state_machine_definition))

    def to_dict(self):
        return self.schema().dump(self)

    def to_json(self, indent: int = None):
        return json.dumps(self.to_dict(), indent=indent)

    def get_state(self, state_id):
        state = self.states.get(state_id)
        if not state:
            raise AttributeError(f"Could not find State for state id: '{state_id}'")
        state.state_id = state_id
        return state

    def process_input_payload(
        self,
        state_input: StateInput,
        current_state: State,
    ) -> tuple[StateInput, JSON]:
        """Process input payload for State work.

        Order of application:
            - InputPath
            - Parameters
        """

        # StatePatch hook: pre_input_process_hook()
        if current_state.state_patch and current_state.state_patch.hook_defined(
            "pre_input_process_hook"
        ):
            state_input, current_state = current_state.state_patch.pre_input_process_hook(
                state_input, current_state
            )

        # apply InputPath
        state_input.data = state_input.apply_input_path(current_state.input_path)
        original_data = state_input.data

        # apply Parameters
        if isinstance(current_state, (Task, Parallel, Map, Pass)):
            state_input.data = state_input.apply_parameters(current_state.parameters)

        # StatePatch hook: post_input_process_hook()
        if current_state.state_patch and current_state.state_patch.hook_defined(
            "post_input_process_hook"
        ):
            (
                state_input,
                original_data,
            ) = current_state.state_patch.post_input_process_hook(
                state_input, current_state, original_data
            )

        return state_input, original_data

    def process_output_payload(
        self,
        state_output: StateOutput,
        current_state: State,
        original_data: JSON,
    ) -> StateOutput:
        """Process output payload for State return.

        Order of application:
            - ResultSelector
            - ResultPath
            - OutputPath
        """

        # StatePatch hook: pre_output_process_hook()
        if current_state.state_patch and current_state.state_patch.hook_defined(
            "pre_output_process_hook"
        ):
            (
                state_output,
                current_state,
                original_data,
            ) = current_state.state_patch.pre_output_process_hook(
                state_output, current_state, original_data
            )

        # apply ResultSelector
        state_output.data = state_output.apply_result_selector(
            current_state.result_selector
        )

        # apply ResultPath
        state_output.data = state_output.apply_result_path(
            current_state.result_path,
            state_output.data,
            original_data,
        )

        # apply OutputPath
        state_output.data = state_output.apply_output_path(current_state.output_path)

        # StatePatch hook: post_output_process_hook()
        if current_state.state_patch and current_state.state_patch.hook_defined(
            "post_output_process_hook"
        ):
            state_output = current_state.state_patch.post_output_process_hook(
                state_output, current_state, original_data
            )

        return state_output

    def run(
        self,
        workflow_input: WorkflowInput,
        registered_resources: dict | None = None,
        context: Context = None,
        state_patches: dict[str, "StatePatch"] = None,
    ) -> WorkflowOutput:
        """Run Workflow"""

        # initialize new Context if not provided
        context = context or Context.create(self, workflow_input)

        # initialize first state and input for Workflow
        state_input = StateInput(data=workflow_input.data, context=context)
        current_state_id = self.start_at
        logger.info(f"Workflow Start At: '{current_state_id}'")
        logger.debug(f"Workflow Input: '{state_input}'")

        # main Workflow loop to process States
        while True:
            # update context
            context.set_current_state(current_state_id)
            state_input.context = context

            # handle no next state
            if current_state_id is None:
                logger.warning(
                    "Next step undefined, exiting.  Consider explicit Succeed or Fail "
                    "state."
                )
                return WorkflowOutput(data=state_input.data)

            # initialize State
            current_state = self.get_state(current_state_id)
            logger.info(f"Current State: '{current_state.state_id}'")
            logger.debug(f"State Input: {state_input}")

            # apply StatePatch if present
            current_state.set_state_patch(state_patches)

            # process Input Payload
            state_input, original_data = self.process_input_payload(
                state_input, current_state
            )

            logger.debug(f"Running State logic: '{current_state_id}'")

            # STATEPATCH
            if current_state.state_patch and current_state.state_patch.hook_defined(
                "run_override"
            ):
                (
                    next_state_id,
                    state_output,
                ) = current_state.state_patch.run_override(
                    current_state, state_input, registered_resources
                )

            # CHOICE, PASS, WAIT
            elif isinstance(current_state, (Choice, Pass, Wait)):
                next_state_id, state_output = current_state.run(state_input)

            # TASK, MAP, PARALLEL
            elif isinstance(current_state, (Task, Map, Parallel)):
                next_state_id, state_output = current_state.run(
                    state_input,
                    context,
                    registered_resources=registered_resources or {},
                )

            # FAIL, SUCCEED
            elif isinstance(current_state, (Fail, Succeed)):
                return WorkflowOutput(data=state_input.data)

            else:
                raise Exception(f"State type: {current_state.type} not recognized")

            # process Output Payload
            state_output = self.process_output_payload(
                state_output, current_state, original_data
            )

            # handle end state
            if current_state.end:
                return WorkflowOutput(data=state_output.data)

            # continue workflow state loop
            logger.debug(f"State Output: {state_output}")
            state_input = state_output.to_state_input()
            current_state_id = next_state_id


@define
class StateMachine(Workflow):
    pass


@define
class Iterator(Workflow):
    processor_config: dict = field(default=None)
    pass

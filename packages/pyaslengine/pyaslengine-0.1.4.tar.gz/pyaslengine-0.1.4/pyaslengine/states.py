"""pyaslengine.states"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import datetime
from dateutil.parser import parse as date_parse
import time
from typing import TYPE_CHECKING

from attrs import define, field

from pyaslengine.data import Context, StateInput, StateOutput, WorkflowInput, JSON
from pyaslengine.log import get_logger
from pyaslengine.rules import ChoiceRule

if TYPE_CHECKING:
    from pyaslengine.patch.states import StatePatch
    from pyaslengine.workflows import Iterator
    from pyaslengine.workflows import Workflow

logger = get_logger(__name__)


@define
class State:
    # ASL fields
    type: str = field(default=None, repr=True)
    comment: str = field(default=None, repr=True)
    next: str = field(default=None, repr=True)
    end: bool = field(default=None, repr=True)
    input_path: str = field(default=None, repr=True)
    output_path: str = field(default=None, repr=True)
    result: str = field(default=None, repr=True)
    result_path: bool = field(default=None, repr=True)
    retry: list = field(default=None, repr=True)
    catch: list = field(default=None, repr=True)
    parameters: dict = field(default=None, repr=True)
    result_selector: dict = field(default=None, repr=True)

    # pyaslengine fields
    state_id: str = field(default=None)
    state_patch: "StatePatch" = field(default=None)

    def set_state_patch(self, state_patches):
        state_patches = state_patches or {}
        self.state_patch = state_patches.get(self.state_id)
        if self.state_patch:
            logger.info(f"StatePatch applied to State: '{self.state_id}'")


@define
class Task(State):
    resource: str = field(default=None, repr=True)

    def run(
        self,
        state_input: StateInput,
        registered_resources: dict = None,
    ) -> tuple[str, StateOutput]:
        from pyaslengine.workflows import TaskInvoker

        if not registered_resources:
            registered_resources = {}
        task_invoker = TaskInvoker(resources=registered_resources)
        next_state_id = self.next

        output_data = task_invoker.invoke(
            self,
            state_input.data,
            None,
        )

        return next_state_id, StateOutput(data=output_data)


@define
class Choice(State):
    default: str = field(default=None, repr=True)
    choices: list[ChoiceRule] = field(default=None, repr=True)

    def run(self, state_input: StateInput) -> tuple[str, StateOutput]:
        state_output = StateOutput(data=state_input.data)
        for choice in self.choices:
            if choice.check_rule(state_input):
                return choice.next, state_output
        return self.default, state_output


@define
class Pass(State):
    result: JSON = field(default=None, repr=True)

    def run(self, state_input: StateInput) -> tuple[str, StateOutput]:
        if self.result:
            return self.next, StateOutput(data=self.result)
        return self.next, state_input.to_state_output()


@define
class Succeed(State):
    pass


@define
class Fail(State):
    pass


@define
class ConcurrentWorkflow(State):
    max_concurrency: int = field(default=None, repr=True)
    use_threads: bool = field(default=True, repr=True)

    @property
    def num_workers(self):
        """Default to single worker if not set."""
        return self.max_concurrency or 1

    def run_workflows_concurrently(
        self,
        context: Context,
        workflows: list["Workflow"],
        input_data_items: list[JSON],
        registered_resources: dict,
    ):
        """
        Supports concurrent execution of workflow + input for both Map and Parallel states
        """
        # prepare list of results in advance that matches length of tasks
        ordered_output_results = [None for _ in range(len(workflows))]

        # determine if using threads or processes
        executor_class = ThreadPoolExecutor if self.use_threads else ProcessPoolExecutor

        with executor_class(max_workers=self.num_workers) as executor:
            future_to_index = {
                executor.submit(
                    workflow_data_tuple[0].run,
                    WorkflowInput(data=workflow_data_tuple[1], context=context),
                    registered_resources,
                    context,
                ): i
                for i, workflow_data_tuple in enumerate(zip(workflows, input_data_items))
            }

            # as tasks complete, store in proper order of results list
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                loop_output_data = future.result()
                ordered_output_results[index] = loop_output_data.data

        return ordered_output_results


@define
class Map(ConcurrentWorkflow):
    """
    https://states-language.net/#map-state

    Deprecations:
        - "Iterator" deprecated in favor of "ItemProcessor"
        - "Parameters" deprecated in favor of "ItemSelector"
    """

    iterator: "Iterator" = field(default=None)
    item_processor: "Iterator" = field(default=None)
    items_path: str = field(default=None, repr=True)
    item_selector: dict = field(default=None, repr=True)

    @property
    def get_item_processor(self):
        """
        "Iterator" has been deprecated in favor of "ItemProcessor", but both may show up
        for pre-existing StateMachine definitions.  This property will return either
        self.iterator or self.item_processor, whichever is defined.
        """
        item_processor = self.item_processor or self.iterator
        if not item_processor:
            raise AttributeError("Either Iterator or ItemProcessor must be set.")
        return item_processor

    def run(
        self,
        state_input,
        registered_resources=None,
        context: Context = None,
    ) -> tuple[str, StateOutput]:
        """Process SINGLE Workflow across MULTIPLE data inputs"""
        # get list of data inputs via ItemsPath
        input_data_items = state_input.jsonpath_match(self.items_path or "$")

        # generate list of Workflows equal to length of items
        workflows = [self.get_item_processor] * len(input_data_items)

        output_datas = self.run_workflows_concurrently(
            context,
            workflows,
            input_data_items,
            registered_resources,
        )

        return self.next, StateOutput(data=output_datas)


@define
class Parallel(ConcurrentWorkflow):
    branches: list["Workflow"] = field(default=None, repr=True)

    def run(
        self,
        state_input,
        registered_resources=None,
        context: Context = None,
    ) -> tuple[str, StateOutput]:
        """Process MULTIPLE Workflows across SINGLE data input"""
        # clone data input for each Workflow
        input_data_items = [state_input.data for x in range(len(self.branches))]

        # set workflows as branches
        workflows = self.branches

        output_datas = self.run_workflows_concurrently(
            context,
            workflows,
            input_data_items,
            registered_resources,
        )
        return self.next, StateOutput(data=output_datas)


@define
class Wait(State):
    seconds: int = field(default=None, repr=True)
    seconds_path: str = field(default=None, repr=True)
    timestamp: str = field(default=None, repr=True)
    timestamp_path: str = field(default=None, repr=True)

    def run(self, state_input: StateInput):
        if self.seconds or self.seconds_path:
            wait_time = self.seconds or state_input.jsonpath_match(self.seconds_path)
        elif self.timestamp or self.timestamp_path:
            target_timestamp = date_parse(self.timestamp or self.timestamp_path)
            wait_time = target_timestamp - datetime.datetime.utcnow()
        else:
            raise AttributeError("Either Seconds or SecondsPath must be set")
        logger.debug(f"Waiting {wait_time} seconds...")
        time.sleep(wait_time)
        return self.next, state_input.to_state_output()

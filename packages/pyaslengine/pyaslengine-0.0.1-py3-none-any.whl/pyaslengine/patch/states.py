"""pyaslengine.patch.states"""


from pyaslengine.data import StateInput, StateOutput, JSON
from pyaslengine.states import State
from pyaslengine.log import get_logger

logger = get_logger(__name__)


class StatePatch:
    """"""

    def hook_defined(self, hook):
        """Return boolean if hook is overridden"""
        return getattr(self, hook).__func__ is not getattr(StatePatch, hook)

    def pre_input_process_hook(
        self, state_input: StateInput, current_state: State
    ) -> tuple[StateInput, State]:
        """Override to run method BEFORE input data processed."""
        raise NotImplementedError()

    def post_input_process_hook(
        self, state_input: StateInput, current_state: State, original_data: JSON
    ) -> tuple[StateInput, JSON]:
        """Override to run method AFTER input data processed."""
        raise NotImplementedError()

    def run_override(
        self, state: State, state_input: StateInput, registered_resources: dict
    ) -> tuple[str, StateOutput]:
        """Override to define State run logic."""
        raise NotImplementedError()

    def pre_output_process_hook(
        self, state_output: StateOutput, current_state: State, original_data: JSON
    ) -> tuple[StateOutput, State, JSON]:
        """Override to run method BEFORE output data processed."""
        raise NotImplementedError()

    def post_output_process_hook(
        self, state_output: StateOutput, current_state: State, original_data: JSON
    ) -> StateOutput:
        """Override to run method AFTER output data processed."""
        raise NotImplementedError()

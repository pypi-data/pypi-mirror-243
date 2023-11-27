"""pyaslengine.schemas"""

from attrs import asdict
from marshmallow import Schema, fields, post_load, pre_dump, RAISE

from pyaslengine.log import get_logger
from pyaslengine.rules import ChoiceRule
from pyaslengine.states import Pass, Task, Choice, Succeed, Fail, Map, Wait, Parallel
from pyaslengine.workflows import Iterator, StateMachine

logger = get_logger(__name__)


class BaseSchema(Schema):
    class Meta:
        unknown = RAISE

    @pre_dump
    def remove_none_fields(self, data, **kwargs):
        if isinstance(data, dict):
            return {key: value for key, value in data.items() if value is not None}
        else:
            return {
                key: value for key, value in asdict(data).items() if value is not None
            }


class DynamicStateField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        state_type = value.get("Type").lower()
        state_class = STATE_TYPE_MAP.get(state_type)
        schema = state_class()
        return schema.load(value)

    def _serialize(self, value, attr, data, **kwargs):
        if isinstance(value, dict):
            state_type = value.get("type").lower()
        else:
            state_type = value.__class__.__name__.lower()
        state_class = STATE_TYPE_MAP[state_type]
        schema = state_class()
        return schema.dump(value)


class StateSchema(BaseSchema):
    type = fields.Str(data_key="Type")
    comment = fields.Str(data_key="Comment")
    next = fields.Str(data_key="Next")
    end = fields.Boolean(data_key="End")
    input_path = fields.Str(data_key="InputPath")
    output_path = fields.Str(data_key="OutputPath")
    result_path = fields.Str(data_key="ResultPath")
    retry = fields.List(fields.Dict, data_key="Retry")
    catch = fields.List(fields.Dict, data_key="Catch")
    parameters = fields.Dict(data_key="Parameters")
    result_selector = fields.Dict(data_key="ResultSelector")


class TaskSchema(StateSchema):
    resource = fields.Str(data_key="Resource")

    @post_load
    def make_state(self, data, **kwargs):
        return Task(**data)


class PassSchema(StateSchema):
    result = fields.Raw(data_key="Result")

    @post_load
    def make_state(self, data, **kwargs):
        return Pass(**data)


class SucceedSchema(StateSchema):
    @post_load
    def make_state(self, data, **kwargs):
        return Succeed(**data)


class FailSchema(StateSchema):
    @post_load
    def make_state(self, data, **kwargs):
        return Fail(**data)


class ChoiceRuleSchema(BaseSchema):
    variable = fields.Str(data_key="Variable")
    comment = fields.Str(data_key="Comment")
    next = fields.Str(data_key="Next")

    # boolean compound comparisons
    is_not = fields.Dict(data_key="Not")
    is_and = fields.List(fields.Dict(), data_key="And")
    is_or = fields.List(fields.Dict(), data_key="Or")

    # comparisons
    string_equals = fields.Str(data_key="StringEquals")
    string_equals_path = fields.Str(data_key="StringEqualsPath")
    string_less_than = fields.Str(data_key="StringLessThan")
    string_less_than_path = fields.Str(data_key="StringLessThanPath")
    string_greater_than = fields.Str(data_key="StringGreaterThan")
    string_greater_than_path = fields.Str(data_key="StringGreaterThanPath")
    string_less_than_equals = fields.Str(data_key="StringLessThanEquals")
    string_less_than_equals_path = fields.Str(data_key="StringLessThanEqualsPath")
    string_greater_than_equals = fields.Str(data_key="StringGreaterThanEquals")
    string_greater_than_equals_path = fields.Str(data_key="StringGreaterThanEqualsPath")
    numeric_equals = fields.Str(data_key="NumericEquals")
    numeric_equals_path = fields.Str(data_key="NumericEqualsPath")
    numeric_less_than = fields.Str(data_key="NumericLessThan")
    numeric_less_than_path = fields.Str(data_key="NumericLessThanPath")
    numeric_greater_than = fields.Str(data_key="NumericGreaterThan")
    numeric_greater_than_path = fields.Str(data_key="NumericGreaterThanPath")
    numeric_less_than_equals = fields.Str(data_key="NumericLessThanEquals")
    numeric_less_than_equals_path = fields.Str(data_key="NumericLessThanEqualsPath")
    numeric_greater_than_equals = fields.Number(data_key="NumericGreaterThanEquals")
    numeric_greater_than_equals_path = fields.Str(data_key="NumericGreaterThanEqualsPath")
    boolean_equals = fields.Str(data_key="BooleanEquals")
    boolean_equals_path = fields.Str(data_key="BooleanEqualsPath")
    timestamp_equals = fields.Str(data_key="TimestampEquals")
    timestamp_equals_path = fields.Str(data_key="TimestampEqualsPath")
    timestamp_less_than = fields.Str(data_key="TimestampLessThan")
    timestamp_less_than_path = fields.Str(data_key="TimestampLessThanPath")
    timestamp_greater_than = fields.Str(data_key="TimestampGreaterThan")
    timestamp_greater_than_path = fields.Str(data_key="TimestampGreaterThanPath")
    timestamp_less_than_equals = fields.Str(data_key="TimestampLessThanEquals")
    timestamp_less_than_equals_path = fields.Str(data_key="TimestampLessThanEqualsPath")
    timestamp_greater_than_equals = fields.Str(data_key="TimestampGreaterThanEquals")
    timestamp_greater_than_equals_path = fields.Str(
        data_key="TimestampGreaterThanEqualsPath"
    )
    is_null = fields.Str(data_key="IsNull")
    is_present = fields.Boolean(data_key="IsPresent")
    is_string = fields.Str(data_key="IsString")
    is_numeric = fields.Str(data_key="IsNumeric")
    is_timestamp = fields.Str(data_key="IsTimestamp")
    is_boolean = fields.Str(data_key="IsBoolean")
    string_matches = fields.Str(data_key="StringMatches")

    @post_load
    def make_state(self, data, **kwargs):
        return ChoiceRule(**data)


class ChoiceSchema(StateSchema):
    default = fields.Str(data_key="Default")
    choices = fields.List(fields.Nested(ChoiceRuleSchema()), data_key="Choices")

    @post_load
    def make_state(self, data, **kwargs):
        return Choice(**data)


class WorkflowSchema(BaseSchema):
    comment = fields.Str(data_key="Comment")
    start_at = fields.Str(data_key="StartAt")
    states = fields.Dict(keys=fields.Str, values=DynamicStateField(), data_key="States")


class StateMachineSchema(WorkflowSchema):
    @post_load
    def make_state_machine(self, data, **kwargs):
        return StateMachine(**data)


class IteratorSchema(WorkflowSchema):
    processor_config = fields.Dict(data_key="ProcessorConfig")

    @post_load
    def make_iterator(self, data, **kwargs):
        return Iterator(**data)


class MapSchema(StateSchema):
    """
    https://states-language.net/#map-state

    Deprecations:
        - "Iterator" deprecated in favor of "ItemProcessor"
        - "Parameters" deprecated in favor of "ItemSelector"
    """

    iterator = fields.Nested(IteratorSchema(), data_key="Iterator")
    item_processor = fields.Nested(IteratorSchema(), data_key="ItemProcessor")
    items_path = fields.Str(data_key="ItemsPath")
    max_concurrency = fields.Int(data_key="MaxConcurrency")
    item_selector = fields.Dict(data_key="ItemSelector")

    @post_load
    def make_map(self, data, **kwargs):
        return Map(**data)


class ParallelSchema(StateSchema):
    max_concurrency = fields.Int(data_key="MaxConcurrency")
    branches = fields.List(fields.Nested(IteratorSchema()), data_key="Branches")

    @post_load
    def make_parallel(self, data, **kwargs):
        return Parallel(**data)


class WaitSchema(StateSchema):
    seconds = fields.Int(data_key="SecondsPath")
    seconds_path = fields.Str(data_key="SecondsPath")
    timestamp = fields.Str(data_key="Timestamp")
    timestamp_path = fields.Str(data_key="TimestampPath")

    @post_load
    def make_map(self, data, **kwargs):
        return Wait(**data)


STATE_TYPE_MAP = {
    "pass": PassSchema,
    "choice": ChoiceSchema,
    "task": TaskSchema,
    "map": MapSchema,
    "succeed": SucceedSchema,
    "fail": FailSchema,
    "wait": WaitSchema,
    "parallel": ParallelSchema,
}

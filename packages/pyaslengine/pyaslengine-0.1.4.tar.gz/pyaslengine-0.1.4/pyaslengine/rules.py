"""pyaslengine.rules"""

from attrs import define, field, fields

from pyaslengine.data import StateInput
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class ChoiceRule:
    """

    https://states-language.net/#choice-state
    """

    comment: str = field(default=None, repr=True)
    variable: str = field(default=None, repr=True)
    next: str = field(default=None, repr=True)
    is_not: dict = field(default=None, repr=True)
    is_and: list = field(default=None, repr=True)
    is_or: list = field(default=None, repr=True)
    string_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_less_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_less_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_greater_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_greater_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_less_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_less_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_greater_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_greater_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_less_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_less_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_greater_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_greater_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_less_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_less_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_greater_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    numeric_greater_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    boolean_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    boolean_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_less_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_less_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_greater_than: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_greater_than_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_less_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_less_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_greater_than_equals: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    timestamp_greater_than_equals_path: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    is_null: str = field(default=None, repr=False, metadata={"group": "data_comparisons"})
    is_present: bool = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    is_string: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    is_numeric: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    is_timestamp: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    is_boolean: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )
    string_matches: str = field(
        default=None, repr=False, metadata={"group": "data_comparisons"}
    )

    @classmethod
    def get_data_comparison_fields(cls) -> field:
        """Return list of ChoiceRule fields that are data comparisons."""
        data_comparison_fields = fields(cls)
        return [
            field
            for field in data_comparison_fields
            if field.metadata.get("group") == "data_comparisons"
        ]

    def check_rule(self, state_input: StateInput):
        for _field in self.get_data_comparison_fields():
            if rule_value := getattr(self, _field.name):
                logger.debug(f"Data comparison rule type: '{_field.name}'")

                # check for method that matches comparison type
                rule_method = getattr(self, f"run_{_field.name}")
                if not rule_method:
                    from pyaslengine.schemas import ChoiceRuleSchema

                    original_field_name = ChoiceRuleSchema().fields[_field.name]
                    raise AttributeError(
                        f"Data comparison type '{original_field_name}' not recognized"
                    )
                input_value = state_input.jsonpath_match(self.variable)

                # if not matches, rule is not satisfied, return False
                if not input_value:
                    return False

                # else, run rule logic
                return rule_method(input_value, rule_value)

    def run_string_equals(self, input_value, rule_value):
        return input_value == rule_value

    def run_string_equals_path(self, state_data, value):
        raise NotImplementedError()

    def run_string_less_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_less_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_greater_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_greater_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_less_than_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_less_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_greater_than_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_greater_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_less_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_less_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_greater_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_greater_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_less_than_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_less_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_numeric_greater_than_equals(self, input_value, rule_value):
        return input_value >= rule_value

    def run_numeric_greater_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_boolean_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_boolean_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_less_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_less_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_greater_than(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_greater_than_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_less_than_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_less_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_greater_than_equals(self, input_value, rule_value):
        raise NotImplementedError()

    def run_timestamp_greater_than_equals_path(self, input_value, rule_value):
        raise NotImplementedError()

    def run_is_null(self, input_value, rule_value):
        raise NotImplementedError()

    def run_is_present(self, input_value, rule_value):
        return input_value is not None

    def run_is_string(self, input_value, rule_value):
        raise NotImplementedError()

    def run_is_numeric(self, input_value, rule_value):
        raise NotImplementedError()

    def run_is_timestamp(self, input_value, rule_value):
        raise NotImplementedError()

    def run_is_boolean(self, input_value, rule_value):
        raise NotImplementedError()

    def run_string_matches(self, input_value, rule_value):
        """
        # TODO: handle wildcard equality
        """
        return input_value == rule_value

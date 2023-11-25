"""pyaslengine.data"""

import datetime
import json
import random
import re
from typing import TypeAlias, TYPE_CHECKING, Optional
import uuid

from attrs import define, field, asdict
from jsonpath_ng import parse

from pyaslengine.log import get_logger

if TYPE_CHECKING:
    from pyaslengine.workflows import Workflow

logger = get_logger(__name__)

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
JSONPath: TypeAlias = JSON


@define
class Context:
    """
    Default:
    https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html

    Map:
    https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html
    #contextobject-map
    """

    execution: JSON = field(default=None)
    state: JSON = field(default=None)
    state_machine: JSON = field(default=None)
    task: JSON = field(default=None)

    @classmethod
    def create(
        cls,
        workflow: Optional["Workflow"] = None,
        workflow_input: Optional["WorkflowInput"] = None,
    ):
        return cls(
            execution={
                "id": str(uuid.uuid4()),
                "input": json.dumps(workflow_input.data) if workflow_input else None,
                "start_time": datetime.datetime.utcnow().isoformat(),
            },
            state_machine={
                "id": str(uuid.uuid4()),
                "definition": workflow.to_json() if workflow else None,
            },
            task={"token": cls.mint_task_token()},
        )

    def set_current_state(self, state_name: str):
        self.state = {
            "entered_time": datetime.datetime.utcnow().isoformat(),
            "name": state_name,
            "retry_count": 0,
        }

    @classmethod
    def mint_task_token(cls):
        return str(uuid.uuid4())

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())


@define
class Payload:
    data: JSON = field(default=None)
    context: Context = field(default=None)

    def jsonpath_match(self, json_path):
        """Return value from JSON based on JSONPath expression.

        According to ASL, "all Reference Paths MUST be unambiguous references to a single
        value, array, or object (subtree)", therefore if the JSONPath matches multiple
        nodes in the data an exception will be raised.

        If no matches are found, None will be returned.  It is the responsibility of the
        calling context to handle None results.

        If double $$ prefixes the JSONPath, this instructs to look to the context for
        matching values.
        """
        # context match
        if json_path.startswith("$$"):
            json_path = json_path.replace("$$.", "$.")
            target = self.context.to_dict()
        # data match
        elif json_path.startswith("$"):
            target = self.data
        else:
            raise ValueError(f"Invalid JSONPath: {json_path}")
        json_path_expr = parse(json_path)
        matches = json_path_expr.find(target)
        if len(matches) > 1:
            raise ValueError("Multiple matches for JSONPath")
        elif not matches:
            return None
        return matches[0].value

    def apply_template(self, template: JSON):
        logger.debug(f"Applying template: {template}")
        if template is None:
            return self.data

        # Update template by processing any intrinsic functions
        new_template = {}
        for k, v in template.items():
            func_name, func_args = IntrinsicFunction.parse_function(v, self)
            if k.endswith(".$") and func_name and func_args:
                new_key = k.rstrip(".$")
                new_value = IntrinsicFunction().transform(func_name, func_args, self)
            else:
                new_key = k
                new_value = v
            new_template[new_key] = new_value
        template = new_template

        def recursive_process(node):
            if isinstance(node, dict):
                output = {}
                for k, v in node.items():
                    if k.endswith(".$"):
                        json_path_expr = v
                        _k = k.rstrip(".$")
                        _v = self.jsonpath_match(json_path_expr)
                    else:
                        _k = k
                        _v = recursive_process(v)
                    output[_k] = _v
                return output
            elif isinstance(node, list):
                return [recursive_process(item) for item in node]
            else:
                return node

        return recursive_process(template)


@define
class StateInput(Payload):
    def apply_parameters(self, template: JSONPath):
        """
        Parameters: This field creates a collection of key-value pairs that are passed
        as input to the task. This can be particularly useful for customizing the input
        to the task by combining static values with JSON from the state's input using
        JsonPath queries.
        """
        logger.info(f"Applying Parameters: {template}")
        return self.apply_template(template)

    def apply_input_path(self, input_path: JSONPath):
        """
        InputPath: This field filters the input to a state, selecting a portion of the
        state's input to pass to the state's task as input. If you omit the InputPath,
        the whole input is passed to the task. If you set it as null, no input is passed
        to the task.
        """
        logger.info(f"Applying InputPath: {input_path}")
        if input_path is None:
            return self.data
        return self.jsonpath_match(input_path)

    def to_state_output(self):
        return StateOutput(data=self.data, context=self.context)


@define
class StateOutput(Payload):
    def apply_result_path(
        self,
        result_path: JSONPath,
        result_value: JSON,
        original_data: JSON,
    ):
        """
        ResultPath: This field specifies where (in the state's input data) to place the
        output of the state's task. If you don't specify a ResultPath, the task's output
        replaces the entire input. If you specify a ResultPath of null, the task's output
        is discarded. This gives you control over how the output is combined with the
        original input JSON (if at all).
        """
        logger.info(f"Applying ResultPath: {result_path}")
        # TODO: this will need to potentially pull from self.context for double $$
        if result_path is None:
            return result_value
        if not isinstance(original_data, dict):
            raise TypeError("Cannot apply ResultPath to non-object input data")
        new_output_data = original_data.copy()
        jsonpath_expr = parse(result_path)
        jsonpath_expr.update_or_create(new_output_data, result_value)
        return new_output_data

    def apply_result_selector(self, template: JSON):
        """
        ResultSelector: This field allows you to filter and manipulate the raw result of
        the state, such as the output of a task. You can create a new JSON object from
        the state's output, selecting only the pieces of data you need or transforming
        the output as required. This occurs immediately after the task completes and
        before the ResultPath is applied.
        """
        logger.info(f"Applying ResultSelector: {template}")
        return self.apply_template(template)

    def apply_output_path(self, output_path: JSONPath):
        """
        OutputPath: This field filters the state's output, selecting a portion of the
        state's output to pass as input to the next state. This allows you to control
        what data is passed to the next state, reducing the need for tasks in your state
        machine to know the full structure of the input.
        """
        logger.info(f"Applying OutputPath: {output_path}")
        if output_path is None:
            return self.data
        return self.jsonpath_match(output_path)

    def to_state_input(self):
        return StateInput(data=self.data, context=self.context)


@define
class WorkflowInput(Payload):
    def apply_item_selector(self, template: JSONPath):
        """
        ItemSelector: This field is used within a Map state to dynamically construct the
        input for each iteration of the map loop. It allows the inclusion and
        transformation of elements from the original input, as well as the integration
        of additional static or dynamic data. Specifically, ItemSelector defines a
        template that is applied to each item identified by the ItemsPath. The template
        can reference elements of the current item being processed as well as other
        parts of the state input. If ItemSelector is omitted, each item identified by
        ItemsPath is passed as is to the iteration. If set, ItemSelector shapes the
        input for each task iteration, enabling the inclusion of both the current item's
        data and other relevant data from the state input.

        NOTE: the state of self.data is what ItemsPath provided, but this can reach into
        the ORIGINAL payload.
        """
        logger.info(f"Applying ItemSelector: {template}")
        return self.apply_template(template)


@define
class WorkflowOutput(Payload):
    pass


class IntrinsicFunction:
    """Base class for ASL intrinsic functions.

    Functions: https://states-language.net/spec.html#appendix-b
        - States.Format
        - States.StringToJson
        - States.JsonToString
        - States.Array
        - States.ArrayPartition
        - States.ArrayContains
        - States.ArrayRange
        - States.ArrayGetItem
        - States.ArrayLength
        - States.ArrayUnique
        - States.Base64Encode
        - States.Base64Decode
        - States.Hash
        - States.JsonMerge
        - States.MathRandom
        - States.MathAdd
        - States.StringSplit
        - States.UUID

    Examples:
        - States.StringToJson($.Payload.body)
        - States.MathRandom(1,10)
    """

    @classmethod
    def parse_function(
        cls,
        payload_value: str,
        payload: Payload,
    ) -> tuple[str | None, list[JSON] | None]:
        """Parse Intrinsic Function name and arguments.

        Arguments MAY be a JSONPath; for these, retrieve them from Payload or Context
        before passing to the function, where the function will be responsible for any
        further processing or type casting.
        """

        # if payload value is not a string, not an intrinsic function
        if not isinstance(payload_value, (str, bytes)):
            return None, None

        # regex string to see if instrinsic function
        match = re.match(r"^States.(.+?)\((.+?)\).*", payload_value)

        # if no match, not an intrinsic function
        if match is None:
            return None, None

        # extract function name and arguments as string from regex match
        function_name, function_args_str = match.groups()

        # parse arguments
        function_args = cls.parse_args(function_args_str, payload)

        return function_name, function_args

    @classmethod
    def parse_args(cls, function_args_str: str, payload: Payload) -> list:
        """Parse function args to a list from the string they originate from.

        While arguments are comma separated, arguments may also be single quoted and
        contain commas within them; these should not be split.  Approach is to find all
        single quoted strings and preserve these via a PLACEHOLDER value, and then split
        on remaining commas.
        """

        pattern = re.compile(r"'(.*?)'")
        placeholders = []

        def replace_with_placeholder(match):
            placeholders.append(match.group(1))
            return f"PLACEHOLDER_{len(placeholders) - 1}"

        modified_args_str = pattern.sub(replace_with_placeholder, function_args_str)
        args = modified_args_str.split(",")
        parsed_args = []
        for arg in args:
            arg = arg.strip()
            if arg.startswith("PLACEHOLDER_"):
                placeholder_index = int(arg.split("_")[-1])
                parsed_args.append(placeholders[placeholder_index])
            elif arg.startswith("$"):
                parsed_args.append(payload.jsonpath_match(arg))
            else:
                parsed_args.append(arg)
        return parsed_args

    @classmethod
    def transform(
        cls,
        func_name,
        func_args,
        payload: Payload,
    ) -> JSON:
        """Method to transform a Payload value via an intrinsic function.

        If the payload value passed IS an intrinsic function, apply appropriate function
        and return transformed value.  Else, return original value untouched.

        QUESTION: will an intrinsic function ever require the payload?
        """
        func = getattr(cls, f"_func_{func_name.lower()}", None)
        if not func:
            raise AttributeError(f"Intrinsic function '{func_name}' not recognized")
        logger.info(f"Processing intrinsic function: {func_name}")
        return func(func_args, payload)

    @staticmethod
    def _func_stringtojson(func_args, payload):
        json_string = func_args[0]
        return json.loads(json_string)

    @staticmethod
    def _func_mathrandom(func_args, payload):
        if len(func_args) == 2:
            a, b = func_args
        elif len(func_args) == 3:
            a, b, seed = func_args
            random.seed(seed)
        else:
            raise ValueError("MathRandom expects 2 or 3 arguments")
        return random.randint(int(a), int(b))

    @staticmethod
    def _func_format(func_args, payload):
        if len(func_args) > 1:
            template_string, variables = func_args[0], func_args[1:]
            final_string = template_string.format(*variables)
        else:
            final_string = func_args[0][1:-1]
        return final_string

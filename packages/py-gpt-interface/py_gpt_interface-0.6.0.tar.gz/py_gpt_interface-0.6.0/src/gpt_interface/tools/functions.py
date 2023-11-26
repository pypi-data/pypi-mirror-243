from dataclasses import dataclass
import inspect
from typing import Callable, Literal


@dataclass
class AnnotatedFunction:
    name: str
    function: Callable
    annotation: dict


# https://community.openai.com/t/function-calling-parameter-types/268564/7
ParamType = Literal[
    "integer", "string", "float", "boolean", "object",
    "array[integer]", "array[string]", "array[float]", "array[boolean]",
]


def _get_function_required_params(func: Callable) -> list[str]:
    return [
        name
        for name, param in inspect.signature(func).parameters.items()
        if param.default == inspect.Parameter.empty and param.kind == param.POSITIONAL_OR_KEYWORD
    ]


def make_annotated_function(
    func: Callable,
    description: str,  # function description
    param_descriptions: dict[str, str],  # must have a description for every parameter
    param_types: dict[str, ParamType],  # type of each parameter (GPT only recognizes a small subset)
    param_allowed_values: dict[str, list[str]] | None = None,  # for any params that only have a few allowed values
) -> AnnotatedFunction:
    function_annotation = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    parameter: {
                        **(
                            {
                                "type": "array",
                                "items": {
                                    "type": param_types[parameter][6:][:-1],
                                },
                            }
                            if param_types[parameter].startswith("array")
                            else
                            {
                                "type": param_types[parameter],
                            }
                        ),
                        "description": param_descriptions.get(parameter, ""),
                    }
                    for parameter in func.__code__.co_varnames[
                        : func.__code__.co_argcount
                    ]
                },
                "required": _get_function_required_params(func),
            },
        },
    }
    if param_allowed_values is not None:
        for parameter, allowed_values in param_allowed_values.items():
            function_annotation["function"]["parameters"]["properties"][parameter]["enum"] = allowed_values
    return AnnotatedFunction(
        name=func.__name__,
        function=func,
        annotation=function_annotation,
    )


# TODO: auto-parse parameter types in JSON format
"""
def _get_function_param_types(
    func: Callable,
    param_types: dict[str, str],
) -> dict[str, str]:
    type_mapping = {
        int: "int",
        str: "string",
        float: "float",
        bool: "boolean",
        list: "array",
        # add more mappings as needed
    }
    return {
        name : (
            type_mapping[param.annotation]
            if param.annotation is not inspect.Parameter.empty
            else ""
        )
        for name, param in inspect.signature(func).parameters.items()
    }
"""

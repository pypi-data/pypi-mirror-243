import inspect
from typing import Callable


def get_param_types(func: Callable) -> dict[str, str]:
    type_mapping = {
        int: "int",
        str: "string",
        float: "float",
        bool: "boolean",
        # add more mappings as needed
    }
    return {
        name : (
            type_mapping.get(param.annotation, str(param.annotation))
            if param.annotation is not inspect.Parameter.empty
            else ""
        )
        for name, param in inspect.signature(func).parameters.items()
    }


def get_required_parameters(func: Callable) -> list[str]:
    return [
        name
        for name, param in inspect.signature(func).parameters.items()
        if param.default == inspect.Parameter.empty and param.kind == param.POSITIONAL_OR_KEYWORD
    ]


def describe_function(
    func: Callable,
    description: str,  # function description
    param_descriptions: dict[str, str],  # must have a description for every parameter
    param_types: dict[str, str] | None = None,  # manually override these param types (will be auto-extracted otherwise)
    param_allowed_values: dict[str, list[str]] | None = None,  # for any params that only have a few allowed values
) -> dict:
    extracted_param_types = get_param_types(func)
    if param_types is not None:
        extracted_param_types = {
            **extracted_param_types,
            **param_types,
        }
    func_dict = {
        "name": func.__name__,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {
                parameter: {
                    "type": extracted_param_types[parameter],
                    "description": param_descriptions.get(parameter, ""),
                }
                for parameter in func.__code__.co_varnames[
                    : func.__code__.co_argcount
                ]
            },
            "required": get_required_parameters(func),
        },
    }
    if param_allowed_values is not None:
        for parameter, allowed_values in param_allowed_values.items():
            func_dict["parameters"]["properties"][parameter]["enum"] = allowed_values
    return func_dict


# function_call={"name": "get_answer_for_user_query"}


# def get_function_call_from_message(message: dict, function: Function) -> Callable:
    # ...

# response = {
    # "role": "assistant",
    # "content": None,
    # "function_call": {
        # "name": "get_current_weather",
        # "arguments": "{ \"location\": \"Boston, MA\"}",
    # },
# }

# {"role": "function", "name": "get_current_weather", "content": "{\"temperature\": "22", \"unit\": \"celsius\", \"description\": \"Sunny\"}"}

from random import randint
from typing import Literal

from gpt_interface.functions import describe_function


def add(a: int, b: int) -> int:
    return a + b


def test_function_dict():
    func_dict = describe_function(
        add,
        description="Add two numbers",
        param_descriptions={
            "a": "The first number",
            "b": "The second number",
        },
    )
    assert func_dict == {
        "name": "add",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "int",
                    "description": "The first number",
                },
                "b": {
                    "type": "int",
                    "description": "The second number",
                },
            },
            "required": ["a", "b"],
        },
    }


def repeat_string(s: str, n: int) -> str:
    return s * n


def test_function_dict_with_param_types():
    func_dict = describe_function(
        repeat_string,
        description="Repeat a string n times",
        param_descriptions={
            "s": "The string to repeat",
            "n": "The number of times to repeat the string",
        },
        param_types={
            "s": "string",
            "n": "int",
        },
    )
    assert func_dict == {
        "name": "repeat_string",
        "description": "Repeat a string n times",
        "parameters": {
            "type": "object",
            "properties": {
                "s": {
                    "type": "string",
                    "description": "The string to repeat",
                },
                "n": {
                    "type": "int",
                    "description": "The number of times to repeat the string",
                },
            },
            "required": ["s", "n"],
        },
    }


def convert_day_to_int(day: Literal["M", "T", "W", "Th", "F", "Sa", "Su"], random: bool = False) -> int:
    if random:
        return randint(0, 6)
    return ["M", "T", "W", "Th", "F", "Sa", "Su"].index(day)


def test_function_dict_with_allowed_values():
    func_dict = describe_function(
        convert_day_to_int,
        description="Convert a day of the week to an integer",
        param_descriptions={
            "day": "The day of the week",
            "random": "Whether to return a random integer",
        },
        param_types={
            "day": "string",
        },
        param_allowed_values={
            "day": ["M", "T", "W", "Th", "F", "Sa", "Su"],
        },
    )
    assert func_dict == {
        "name": "convert_day_to_int",
        "description": "Convert a day of the week to an integer",
        "parameters": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "description": "The day of the week",
                    "enum": ["M", "T", "W", "Th", "F", "Sa", "Su"],
                },
                "random": {
                    "type": "boolean",
                    "description": "Whether to return a random integer",
                },
            },
            "required": ["day"],
        },
    }

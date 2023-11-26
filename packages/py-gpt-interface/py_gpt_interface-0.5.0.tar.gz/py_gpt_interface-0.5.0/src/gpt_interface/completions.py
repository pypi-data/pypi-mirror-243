from dataclasses import dataclass
import json
from openai import OpenAI

from gpt_interface.log import Log
from gpt_interface.models import known_models


@dataclass
class SystemMessageOptions:
    use_system_message: bool
    system_message: str
    message_at_end: bool = True


def call_completion(
    interface: OpenAI,
    model: str,
    log: Log,
    temperature: float,
    system_message_options: SystemMessageOptions,
    json_mode: bool,
    functions: list[dict],
) -> str:
    if model in [m.name for m in known_models if not m.legacy_chat_api]:
        return call_modern_model(
            interface=interface,
            model=model,
            log=log,
            temperature=temperature,
            system_message_options=system_message_options,
            json_mode=json_mode,
            functions=functions,
        )
    elif model in [m.name for m in known_models]:
        return call_legacy_model(
            interface=interface,
            model=model,
            log=log,
            temperature=temperature,
            system_message_options=system_message_options,
        )
    else:
        raise ValueError(f"Unrecognized model: {model}")


def call_modern_model(
    interface: OpenAI,
    model: str,
    log: Log,
    temperature: float,
    system_message_options: SystemMessageOptions,
    json_mode: bool,
    functions: list[dict],
) -> str:
    messages=[
        {
            "role": message.role,
            "content": message.content
        }
        for message in log.messages
    ]
    if system_message_options.use_system_message:
        system_message = {
            "role": "system",
            "content": system_message_options.system_message,
        }
        if system_message_options.message_at_end:
            messages.append(system_message)
        else:
            messages.insert(0, system_message)
    completion_args = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    if len(functions) > 0:
        completion_args["functions"] = functions
    if json_mode and model in ["gpt-3.5-turbo-1106", "gpt-4-1106-preview"]:
        completion_args["response_format"] = { "type": "json_object" }
    response = interface.chat.completions.create(**completion_args)
    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.function_call
        return_message = json.dumps({
            "function_name": function_call.name,
            "arguments": json.loads(function_call.arguments),
        })
    else:
        return_message = response.choices[0].message.content
    return return_message if return_message else "[ERROR: NO RESPONSE]"


def call_legacy_model(
    interface: OpenAI,
    model: str,
    log: Log,
    temperature: float,
    system_message_options: SystemMessageOptions,
) -> str:
    prompt = "\n".join([
        f"{message.role}: {message.content}"
        for message in log.messages
    ])
    if system_message_options.use_system_message:
        if system_message_options.message_at_end:
            prompt += "\nsystem: " + system_message_options.system_message
        else:
            prompt = "system: " + system_message_options.system_message + "\n" + prompt
    prompt += "\nassistant: "
    response = interface.completions.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text

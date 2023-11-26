from openai import OpenAI

from gpt_interface.calls.call_gpt import call_gpt
from gpt_interface.calls.rate_limiter import RateLimiter
from gpt_interface.log import Log
from gpt_interface.options.models import known_models
from gpt_interface.options.system_message import SystemMessageOptions
from gpt_interface.tools import Tool


class GptInterface:
    def __init__(
        self,
        openai_api_key: str,
        model: str,
        json_mode: bool = False,
        temperature: float = 1.0,
    ) -> None:
        self.set_model(model)
        self.set_json_mode(json_mode)
        self.temperature = temperature
        self.interface = OpenAI(api_key=openai_api_key)
        self.log = Log()
        self.rate_limiter = RateLimiter()
        self.system_message_options = SystemMessageOptions(
            use_system_message=False,
            system_message="",
            message_at_end=True,
        )
        self.tools: list[Tool] = []

    def set_model(self, model: str) -> None:
        self.model = model
        if model not in [m.name for m in known_models]:
            print(f"Warning: unrecognized model {model}. Known models list may be out of date.")

    def set_json_mode(self, json_mode: bool) -> None:
        self.json_mode = json_mode

    def set_system_message(
        self,
        system_message: str = "",
        use_system_message: bool = True,
        message_at_end: bool = True,
    ) -> None:
        self.system_message_options = SystemMessageOptions(
            use_system_message=use_system_message,
            system_message=system_message,
            message_at_end=message_at_end,
        )

    def set_tools(self, tools: list[Tool]) -> None:
        self.tools = tools

    def say(self, user_message: str) -> str:
        self.log.append("user", user_message)
        return self.get_assistant_message()

    def retry(self) -> str:
        self.log.messages = self.log.messages[:-1]
        return self.get_assistant_message()

    def get_assistant_message(self) -> str:
        assistant_message = call_gpt(
            interface=self.interface,
            model=self.model,
            log=self.log,
            system_message_options=self.system_message_options,
            temperature=self.temperature,
            json_mode=self.json_mode,
            tools=self.tools,
            call_again_fn=self.get_assistant_message,
        )
        self.rate_limiter.wait()
        self.log.append("assistant", assistant_message)
        return assistant_message

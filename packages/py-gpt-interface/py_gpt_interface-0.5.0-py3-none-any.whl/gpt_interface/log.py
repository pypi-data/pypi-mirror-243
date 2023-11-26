from dataclasses import dataclass, asdict
import json
import os
from pathlib import Path
from typing import Literal


Role = Literal["user", "assistant", "system"]


@dataclass
class Message:
    role: Role
    content: str

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"


class Log:
    def __init__(self):
        self.messages: list[Message] = []

    def __str__(self) -> str:
        return "\n".join([str(message) for message in self.messages])

    def clear(self) -> None:
        self.messages = []

    def append(self, role: Role, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def set_messages(self, messages: list[Message]) -> None:
        self.messages = messages

    def save(self, path: Path) -> None:
        if not os.path.exists(path.parent):
            os.makedirs(path.parent)
        with open(path, "w") as f:
            json.dump([asdict(message) for message in self.messages], f, indent=4)

    def load(self, path: Path) -> None:
        with open(path, "r") as f:
            self.messages = [Message(**message) for message in json.load(f)]

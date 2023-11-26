from dataclasses import dataclass


@dataclass
class SystemMessageOptions:
    use_system_message: bool
    system_message: str
    message_at_end: bool = True

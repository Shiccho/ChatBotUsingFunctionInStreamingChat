from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    TOOL = "tool"

    def __str__(self):
        return self.value

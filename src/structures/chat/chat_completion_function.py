from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from openai.types.chat.chat_completion_message_tool_call import Function as ChatCompletionMessageToolCallFunction

@dataclass
class Function():
    name: Optional[str] = None
    arguments: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "arguments": self.arguments
        }

    def update(self, function: Function):
        if function.name != None:
            self.name = function.name

        if function.arguments != None:
            self.arguments += function.arguments

    @classmethod
    def from_api_response(cls, function: ChatCompletionMessageToolCallFunction):
        return cls(
            name=function.name,
            arguments=function.arguments
        )
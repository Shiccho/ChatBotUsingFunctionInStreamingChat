from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from openai.types.chat import ChatCompletionMessageToolCall
from .chat_completion_function import Function

@dataclass
class ToolCall():
    id: Optional[str]  = None
    type: str = "function"
    function: Optional[Function] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "function": self.function.to_dict() if self.function != None else None
        }

    def update(self, tool_call: ToolCall):
        if tool_call.id != None:
            self.id = tool_call.id

        if self.function == None:
            self.function = tool_call.function
        else:
            self.function.update(tool_call.function)
    
    @classmethod
    def from_api_response(cls, tool_call: ChatCompletionMessageToolCall):
        return cls(
            id=tool_call.id,
            function=Function.from_api_response(tool_call.function)
        )

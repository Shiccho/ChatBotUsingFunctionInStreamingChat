from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

from openai.types.chat import ChatCompletionMessage
from ...constants.chat import Role
from .chat_completion_tool_call import ToolCall

@dataclass
class Message():
    content: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self) -> Dict:
        dump_dict = {
            "role": self.role,
            "content": self.content if self.content != None else ""
        }
        return dump_dict

    def update(self, message: Message):
        if self.role == None:
            self.role = message.role
        
        if self.content == None:
            self.content = message.content
        elif message.content != None:
            self.content += message.content

    @classmethod
    def from_api_response(cls, message: ChatCompletionMessage):
        return cls(
            content=message.content,
            role=message.role
        )

@dataclass
class SystemMessage(Message):
    role: str = str(Role.SYSTEM)

@dataclass
class UserMessage(Message):
    role: str = str(Role.USER)

@dataclass
class AssistantMessage(Message):
    role: str = str(Role.ASSISTANT)
    tool_calls: Optional[List[ToolCall]] = None

    def to_dict(self) -> Dict:
        dump_dict = super().to_dict()
        if self.tool_calls != None:
            dump_dict['tool_calls'] = [tool_call.to_dict() for tool_call in self.tool_calls]
        return dump_dict

    def update(self, message: AssistantMessage):
        super().update(message)

        if self.tool_calls == None:
            self.tool_calls = message.tool_calls
        elif message.tool_calls != None:
            for i, tool_call in enumerate(message.tool_calls):
                self.tool_calls[i].update(tool_call)
    
    @classmethod
    def from_api_response(cls, message: ChatCompletionMessage):
        return cls(
            content=message.content,
            role=message.role,
            tool_calls=[ToolCall.from_api_response(tool_call) for tool_call in message.tool_calls] if message.tool_calls != None else None
        )

@dataclass
class ToolMessage(Message):
    tool_call_id: Optional[str] = None
    role: str = str(Role.TOOL)

    def to_dict(self) -> Dict:
        dump_dict = super().to_dict()
        dump_dict['tool_call_id'] = self.tool_call_id
        return dump_dict
    
    def update(self, message: ToolMessage):
        super().update(message)
        if message.tool_call_id != None:
            self.tool_call_id = message.tool_call_id


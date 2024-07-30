# Chatbot Using Function with Chat Streaming, Sample Code of Chat AI
# Copyright (C) 2024  Yuki Matsutani

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

from openai.types.chat import ChatCompletionMessage
from ...constants.chat import Role
from .chat_completion_tool_call import ToolCall

@dataclass
class Message():
    content: Optional[str|list[dict[str, str|dict[str,str]]]] = None
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
            already_called_tool = [tool_call.id for tool_call in self.tool_calls]
            for tool_call in message.tool_calls:
                if tool_call.id is not None and tool_call.id not in already_called_tool:
                    self.tool_calls.append(tool_call)
            self.tool_calls[-1].update(tool_call)
    
    @classmethod
    def from_api_response(cls, message: ChatCompletionMessage):
        return cls(
            content=message.content,
            role=message.role,
            tool_calls=[
                ToolCall.from_api_response(tool_call) 
                    for tool_call in message.tool_calls
                ] if message.tool_calls != None else None
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


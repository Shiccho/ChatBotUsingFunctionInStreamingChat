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

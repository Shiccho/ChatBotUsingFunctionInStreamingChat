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
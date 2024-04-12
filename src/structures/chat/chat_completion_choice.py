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
from typing import Optional
from openai.types.chat.chat_completion_chunk import Choice as ChatCompletionChoice
from .chat_completion_message import AssistantMessage, Message

@dataclass
class Choice():
    finish_reason: Optional[str] = None
    index: Optional[int] = None
    message: Optional[Message] = None

    def update(self, choice: Choice):
        if choice.index != None:
            self.index = choice.index

        if self.finish_reason == None:
            self.finish_reason = choice.finish_reason
        
        if self.message == None:
            self.message = choice.message
        else:
            self.message.update(choice.message)
    
    @classmethod
    def from_api_response(cls, choice: ChatCompletionChoice):
        return cls(
            finish_reason=choice.finish_reason,
            index=choice.index,
            message=AssistantMessage.from_api_response(choice.delta)
        )

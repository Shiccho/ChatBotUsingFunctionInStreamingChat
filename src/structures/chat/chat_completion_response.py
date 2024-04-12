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
from typing import List, Optional
from openai.types.chat import ChatCompletionChunk
from .chat_completion_choice import Choice
from .chat_completion_message import Message

@dataclass
class Response():
    id : Optional[str] = None
    choices: Optional[List[Choice]] = None

    def get_message(self) -> Message:
        return self.choices[0].message

    def update(self, chunk: Response):
        if self.id ==  None:
            self.id = chunk.id
        
        assert self.id == chunk.id

        if self.choices == None:
            self.choices = chunk.choices
        else:
            for i, choice in enumerate(chunk.choices):
                self.choices[i].update(choice)

    @classmethod
    def from_api_response(cls, response: ChatCompletionChunk):
        return cls(
            id=response.id,
            choices=[Choice.from_api_response(choice) for choice in response.choices]
        )


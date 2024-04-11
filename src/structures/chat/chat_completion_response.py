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


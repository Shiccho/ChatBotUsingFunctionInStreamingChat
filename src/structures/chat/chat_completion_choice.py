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

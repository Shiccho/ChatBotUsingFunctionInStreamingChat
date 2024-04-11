from typing import List, Dict
from ..chat import Message

class Thread():
    def __init__(self):
        self.messages: List[Message] = [] 

    def add_message(self, message: Message):
        self.messages.append(message)
    
    def get_messages(self) -> List[Dict[str, str]]:
        return [message.to_dict() for message in self.messages]
    
    def render(self):
        rendered = ''
        for message in self.messages:
            rendered += f"{message.render()}\n"
        return rendered
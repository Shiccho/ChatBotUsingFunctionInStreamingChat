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
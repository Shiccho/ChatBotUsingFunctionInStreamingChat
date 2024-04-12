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

from pydantic import BaseModel, ValidationError
from typing import List, Dict, Literal, Optional, Union
from os import PathLike
import json

class ParameterProperties(BaseModel):
    location: Dict
    unit: Dict

class Parameters(BaseModel):
    type: Literal["object"]
    properties: ParameterProperties
    required: List[str]

class Function(BaseModel):
    name: str
    description: str
    parameters: Optional[Parameters]

class ToolFunction(BaseModel):
    type: Literal["function"]
    function: Function

class Tools(BaseModel):
    tools: List[ToolFunction]

    @classmethod
    def load_json(cls, file_path: Union[str, bytes, PathLike]):
        with open(file_path, "r") as file:
            data = json.load(file)
        return cls.model_validate(data)
    
    def get_tools(self):
        return self.tools

### Test ###
if __name__ == '__main__':
    try:
        tools = Tools.load_json("tools.json")
        print(tools.get_tools())
    except ValidationError as e:
        print(f"Validation error: {e}")
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
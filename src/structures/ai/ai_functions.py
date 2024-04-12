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

from typing import Dict, Union, Callable
from os import PathLike
from pathlib import Path
from pydantic import BaseModel, ValidationError
import importlib.util
import json

class Functions(BaseModel):
    availables: Dict[str, Callable]

    @classmethod
    def load_functions(cls, 
                       implementation_directory_path: Union[str, bytes, PathLike], 
                       setting_file_path: Union[str, bytes, PathLike]
    ) -> Functions:
        
        # Load function names from setting file
        with open(setting_file_path, "r") as file:
            setting_data = json.load(file)
        function_names = [
            tool['function']['name'] for tool in setting_data['tools'] 
            if tool['type'] == 'function'
        ]

        # Load functions in `function_names` from the implementation directory
        availables = {}
        for file in Path(implementation_directory_path).glob("*.py"):
            module_name = file.stem
            if module_name in function_names:
                spec = importlib.util.spec_from_file_location(module_name, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Add functions to `functions` by `module_name`
                for attr_name in function_names:
                    if attr_name in function_names and callable(getattr(module, attr_name)):
                        availables[attr_name] = getattr(module, attr_name)
        return cls.model_validate({"availables": availables})
    
    def get(self, function_name: str):
        if function_name not in self.availables:
            raise ValueError(f"Function {function_name} is not available")
        return self.availables[function_name]


### Test ###
if __name__ == '__main__':
    try:
        functions = Functions.load_functions('configs/tools/implementation' ,"configs/tools/settings/tools.json")
        print(functions.get('get_current_weather'))
    except ValidationError as e:
        print(f"Validation error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
        print(f"Available functions: {functions.availables}")
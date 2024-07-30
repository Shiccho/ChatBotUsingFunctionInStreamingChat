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

from os import PathLike
from typing import Union, Optional

from ..structures.chat import SystemMessage, UserMessage, Response, ToolMessage
from ..structures.ai import Thread, Tools, Functions

from openai import AsyncOpenAI
from openai import BadRequestError

import json


class ChatAI:
    def __init__(        
        self, 
        model: str,
        system_prompt: Optional[str] = None,
        tools_setting_file: Optional[Union[str, bytes, PathLike]] = None,
        tools_implementation_directory: Optional[Union[str, bytes, PathLike]] = None
    ):
        self.thread = None
        self.client = AsyncOpenAI()
        self.model = str(model)
        self.thread = Thread()
        self.system_prompt = system_prompt
        if self.system_prompt is not None:
            self.thread.add_message(SystemMessage(content=system_prompt))
        self.tools = Tools.load_json(tools_setting_file).get_tools() if tools_setting_file is not None else None
        self.tool_choices = 'auto' if self.tools is not None else None
        self.functions = Functions.load_functions(
            tools_implementation_directory,
            tools_setting_file
        ) if tools_implementation_directory is not None else None

    async def chat(self, text: str) -> str:
        # Add user message to thread
        self.thread.add_message(UserMessage(content=text))

        # Initialize
        response_stream = None
        request_count = 0
        # Loop until the finish reason become 'stop'
        while request_count < 10:
            if response_stream is None:
                # Create a new completion request
                request_count += 1
                response_stream = await self.client.chat.completions.create( 
                    model=self.model,
                    messages=self.thread.get_messages(),
                    tools=self.tools,
                    tool_choice=self.tool_choices,
                    stream=True,
                )
                # Initialize response object
                response_object = Response()
            
            enter_count = 0
            async for chunk in response_stream:
                chunk_object = Response.from_api_response(chunk)
                response_object.update(chunk_object)
                
                finish_reason = chunk_object.choices[0].finish_reason
                
                if finish_reason == None:
                    # Continue the generation and print the content
                    delta = chunk_object.choices[0].message
                    if delta.content is not None:
                        if delta.content == "\n":
                            enter_count += 1
                        else:
                            enter_count = 0
                        if enter_count > 10:
                            response_stream = None
                            break
                        # print only if there is delta content
                        print(delta.content, end='', flush=True)
                    continue

                elif finish_reason == "stop":
                    print("") # New line
                    # Add response to thread
                    self.thread.add_message(response_object.get_message())
                    response_message = response_object.get_message().content
                    # Return the last JSON object
                    return response_message

                elif finish_reason == "tool_calls":
                    # Call the tool function
                    self.thread.add_message(response_object.get_message())
                    tool_calls = response_object.choices[0].message.tool_calls
                    if tool_calls:
                        try:
                            for tool_call in tool_calls:
                                function_name = tool_call.function.name
                                function_to_call = self.functions.get(function_name)
                                function_args = json.loads(tool_call.function.arguments)
                                tool_response = function_to_call(**function_args)
                                self.thread.add_message(
                                    ToolMessage(
                                        content=tool_response,
                                        tool_call_id=tool_call.id
                                    )
                                )
                        except json.JSONDecodeError as e:
                            print(f"JsonDecodeError: {e}")
                            self.thread.add_message(
                                ToolMessage(
                                    content="JsonDecodeError: Invalid json format for tool arguments",
                                    tool_call_id=tool_call.id
                                )
                            )
                        except ValueError as e:
                            print(f"ValueError: {e}")
                            self.thread.add_message(
                                ToolMessage(
                                    content=f"ValueError: {e}",
                                    tool_call_id=tool_call.id
                                )
                            )
                        except Exception as e:
                            print(f"Error: {e}")
                            self.thread.add_message(
                                ToolMessage(
                                    content=f"Error: {e}",
                                    tool_call_id=tool_call.id
                                )
                            )
                    
                    # Reset the response stream to send the next request
                    response_stream = None
                    break # Break the inner loop to continue the outer loop
                
                elif finish_reason == "length":
                    response_stream = None
                    break
                else:
                    print(f"Unknown finish reason {finish_reason}")
                    return response_object.get_message().content

from typing import Optional, Union, Dict
from os import PathLike

from openai import AsyncOpenAI
from ..structures.ai import Thread, Tools, Functions
from ..structures.chat import UserMessage, Response, ToolMessage
from ..constants.ai import Model

import json

class ChatAI:
    def __init__(
            self, 
            model: str = Model.GPT4,
            tools_setting_file: Optional[Union[str, bytes, PathLike]] = None,
            tools_implementation_directory: Optional[Union[str, bytes, PathLike]] = None
    ) -> None:
        
        self.thread = None
        self.client = AsyncOpenAI()
        self.model = str(model)
        self.thread = Thread()
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

        print("AI: ", end='')
        # Loop until the finish reason become 'stop'
        while True:
            if response_stream is None:
                # Create a new completion request
                response_stream = await self.client.chat.completions.create( 
                    model=self.model, 
                    messages=self.thread.get_messages(),
                    tools=self.tools,
                    tool_choice=self.tool_choices,
                    stream=True,
                )
                # Initialize response object
                response_object = Response()
                
            async for chunk in response_stream:
                chunk_object = Response.from_api_response(chunk)
                response_object.update(chunk_object)
                
                finish_reason = chunk_object.choices[0].finish_reason
                
                if finish_reason == None:
                    # Continue the generation and print the content
                    delta = chunk_object.choices[0].message
                    if delta.content is not None: 
                        # print only if there is delta content
                        print(delta.content, end='')
                    continue

                elif finish_reason == "stop":
                    print("") # New line
                    # Add response to thread
                    self.thread.add_message(response_object.get_message())
                    return response_object.get_message().content

                elif finish_reason == "tool_calls":
                    # Call the tool function
                    tool_calls = response_object.choices[0].message.tool_calls
                    if tool_calls:
                        for tool_call in tool_calls:
                            self.thread.add_message(response_object.get_message())
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
                    
                    # Reset the response stream to send the next request
                    response_stream = None
                    break # Break the inner loop to continue the outer loop

                else:
                    print(f"Unknown finish reason {finish_reason}")
                    return response_object.get_message().content

    def reset_thread(self) -> None:
        self.thread = Thread()

    def render_thread(self) -> str:
        return self.thread.render()

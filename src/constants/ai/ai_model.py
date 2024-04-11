from enum import Enum

class Model(Enum):
    GPT4: str = "gpt-4-turbo-preview"
    GPT4_VISION: str = "gpt-4-vision-preview" # Function Calling is not supported 
    GPT3: str = "gpt-3.5-turbo"

    def __str__(self):
        return self.value
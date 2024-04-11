import argparse

import logging
import asyncio
from dotenv import load_dotenv

from src.ai import ChatAI
from src.constants.ai import Model

dotenv_path = "configs/env/.env"
load_dotenv(dotenv_path=dotenv_path)
logger = logging.getLogger(__name__)

async def main(args) -> int:
    ai = ChatAI(
        model=Model.GPT4,
        tools_setting_file = 'configs/tools/settings/tools.json',
        tools_implementation_directory = 'configs/tools/implementation'
    )
    logger.info("AI initialized")
    while True:
        text = input("You: ")
        if text == "exit":
            break
        reply = await ai.chat(text)
        logger.info(f"AI: {reply}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Function Enabled Streaming Chatbot")
    # Sample add argment: parser.add_argument("--model", type=str, default="gpt4", help="OpenAI model to use")
    args = parser.parse_args()
    status = asyncio.run(main(args))
    exit(status)
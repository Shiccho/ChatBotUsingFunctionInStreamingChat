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

import argparse

import logging
import asyncio
from dotenv import load_dotenv

from src.ai import ChatAI
from src.constants.ai import Model

dotenv_path = "configs/env/.env"
load_dotenv(dotenv_path=dotenv_path)
logger = logging.getLogger(__name__)

license_notification = """
################################################################################################
Chatbot Using Function with Chat Streaming Copyright (C) 2024 Yuki Matsutani
This program comes with ABSOLUTELY NO WARRANTY;for detailes see the GNU General Public License.
This is free software, and you are welcome to redistribute it
under certain conditions; See the GNU General Public License.
################################################################################################
"""

async def main(args) -> int:
    # License Notification
    print(license_notification)

    # Initialize AI
    ai = ChatAI(
        model=Model.GPT4,
        tools_setting_file = 'configs/tools/settings/tools.json',
        tools_implementation_directory = 'configs/tools/implementation'
    )

    # Chat Loop
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
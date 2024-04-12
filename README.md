<!--
  Chatbot Using Function with Chat Streaming, Sample Code of Chat AI
  Copyright (C) 2024  Yuki Matsutani

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
# Usage
Please clone this repositry and use this command,
```bash
cd ChatBotUsingFunctionInStreamingChat
```
then, 
add OPEN_AI_API_KEY in `.env.exmaple` and modify file's name to `.env`

After that,
```bash
python -m src.main
```

# Function Calling
You can register tools or new functions by modify the `configs/tools/settings/tool.json` or `configs/tools/implementations/*.py`

# Usage
Please clone this repositry and use this command,
```bash
cd ChatGPTStreamingChatUsingFunction
```
then, 
add OPEN_AI_API_KEY in `.env.exmaple` and modify file's name to `.env`

After that,
```bash
python -m src.main
```

# Function Calling
You can register tools or new functions by modify the `configs/tools/settings/tool.json` or `configs/tools/implementations/*.py`

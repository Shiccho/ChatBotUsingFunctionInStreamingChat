# Sample Function from OpenAI API Documentation: https://platform.openai.com/docs/guides/function-calling
# tools.json is also from OpenAI API Documentation: https://platform.openai.com/docs/guides/function-calling

def get_current_weather(location, unit="fahrenheit"):
    import json
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
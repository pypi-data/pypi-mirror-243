# test.py
from promptmodel import PromptModel, DevClient, ChatModel
import promptmodel

promptmodel.init(use_cache=True)

client = DevClient()

prompt_model_config = PromptModel("summarize").get_config()

chat_model_config = ChatModel("weather_bot").get_config()


from typing import Optional


def get_current_weather(location: str, unit: Optional[str] = None):
    return "13 degrees celsius"


get_current_weather_desc = {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

import json
import asyncio


@client.register
async def main():
    # res = await PromptModel("function_call_test").astream_and_parse(
    #     {"user_message": "Hello, how are you?"},
    #     functions=[get_current_weather_desc],
    # )
    # async for chunk in res:
    #     print(chunk.__dict__)
    prompt = ChatModel("summary_bot").get_config()

    pass


# if __name__ == "__main__":
#     main()
#     async def sleep_func():
#         print(asyncio.all_tasks(loop=None))
#         asyncio.sleep(100)

#     asyncio.run(sleep_func())

# asyncio.run(main())

import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import geocode

load_dotenv()

def init_open_ai():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)

def ask_llm(llm_client, messages, tools=None, stream=False, model="gpt-4.1-nano-2025-04-14"):
    if stream:
        return llm_client.chat.completions.create(
            messages=messages,
            model=model,
            tools=tools,
            stream=stream
        )
    else: 
        return llm_client.chat.completions.create(
            messages=messages,
            model=model,
            tools=tools,
        ).choices[0].message
    
    
# Tool dispatcher
TOOL_MAP = {
    "geocode": geocode
    # Add more tools as needed
}

def execute_tools(tools_to_execute: list):
    results = []
    for tool in tools_to_execute:
        function_name = tool.function.name
        params = json.loads(tool.function.arguments)
        function_result = TOOL_MAP[function_name](**params)
        results.append(function_result)
    return results

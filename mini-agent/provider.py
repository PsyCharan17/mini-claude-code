from openai import AsyncOpenAI
from config import Config
from pydantic import BaseModel, Field
import json

def get_client(config) -> AsyncOpenAI:
    """
    Returns an AsyncOpenAI client wired up with the user's configuration.
    """
    return AsyncOpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
    )

async def call_model(client: AsyncOpenAI, config, messages: list[dict], tools: list[dict]):
    """
    Calls the model with tools, allowing the model to decide whether to use them.
    This demonstrates the core tool-calling format using the OpenAI client.
    """
    response = await client.chat.completions.create(
        model=config.model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    # Extract the message content
    message = response.choices[0].message
    
    # Parse the raw JSON string 'arguments' into a Python dictionary for easier use
    parsed_tool_calls = None
    if message.tool_calls:
        parsed_tool_calls = []
        for tc in message.tool_calls:
            parsed_tool_calls.append({
                "id": tc.id,
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments)
            })
            
    # Return the clean, parsed format
    return {
        "content": message.content,
        "tool_calls": parsed_tool_calls
    }

def make_tool(name, description, parameters_schema):
    """Build a tool definition dict for the OpenAI API"""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters_schema,
        }
    }
    

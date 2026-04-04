import asyncio
import json
from provider import get_client, call_model
from config import Config
from tools.base import BaseTool
from tools.bash import BashTool

async def agent_loop(messages, tools: list[BaseTool], client, config):
    print("Starting agent loop...\n")
    
    tool_registry = {tool.name(): tool for tool in tools}
    tool_defs = [tool.definition() for tool in tools]
    
    while True:
        # 1. Call the model
        print("Calling model...")
        response = await call_model(client, config, messages, tool_defs)
        
        content = response["content"]
        tool_calls = response["tool_calls"]
        
        # 5. Print assistant text
        if content:
            print(f"\nAssistant: {content}")
            
        # Build the assistant's message to append to history
        assistant_msg = {"role": "assistant", "content": content}
        
        # 4. If no tool calls, we're done
        if not tool_calls:
            print("\nNo more tool calls. Exiting loop.")
            messages.append(assistant_msg)
            break
            
        # If there are tool calls, we must attach them to the assistant message
        # before appending it to the history (OpenAI API requirement).
        assistant_msg["tool_calls"] = []
        for tc in tool_calls:
            assistant_msg["tool_calls"].append({
                "id": tc["id"],
                "type": "function",
                "function": {
                    "name": tc["name"],
                    "arguments": json.dumps(tc["arguments"])
                }
            })
            
        messages.append(assistant_msg)
            
        # 3. Execute each tool call
        for tc in tool_calls:
            print(f"\n🛠️  Calling Tool: {tc['name']}")
            print(f"   Arguments: {tc['arguments']}")
            
            tool = tool_registry.get(tc["name"])
            if not tool:
                result_content = f"Error: Unknown tool '{tc['name']}'"
            else:
                # 3. Call await tool.execute(**tc["arguments"])
                result = await tool.execute(**tc["arguments"])
                result_content = result.content
                
            print(f"   Result:\n{result_content[:200]}{'...' if len(result_content) > 200 else ''}")
            
            # 4. Use the returned ToolResult as the message content
            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "name": tc["name"],
                "content": result_content
            })
        
        print("\n--- Looping back with new messages ---")


async def main():
    config = Config()
    client = get_client(config)
    
    # Initial message
    messages = [{"role": "user", "content": "list the files in the current directory"}]
    
    tools = [BashTool()]
    
    await agent_loop(messages, tools, client, config)

if __name__ == "__main__":
    asyncio.run(main())

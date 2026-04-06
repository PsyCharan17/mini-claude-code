import asyncio 
_always_allowed = {"list_dir","read_file"}
_session_always = set()

async def check_permission(tool_name: str, args: dict) -> bool:
    
    if(tool_name in _always_allowed or tool_name in _session_always):
        return True
    

    print(f"Tool: {tool_name}\nArgs: {args}")
    response = await asyncio.to_thread(input,"Allow?[y/n/always] → ") 
    if response.strip().lower() == "y" or response.strip().lower() == "always":
        if response.strip().lower() == "always":
            _session_always.add(tool_name)
        return True
    return False   

import asyncio                                                                                                                               
from config import Config                                                                                                                    
from provider import get_client                                                                                                              
from prompt import build_system_prompt                                                                                                       
from tools.bash import BashTool                                                                                                              
from tools.list_dir import ListDirTool                                                                                                       
from tools.file_read import FileReadTool                                                                                                     
from tools.file_write import FileWriteTool                                                                                                   
from tools.file_edit import FileEditTool                                                                                                     
from loop import agent_loop                                                                                                                  
                                                                                                                                               
async def main():                                                                                                                            
    config = Config()                                                                                                                        
    client = get_client(config)                                                                                                              
    tools = [BashTool(), ListDirTool(), FileReadTool(), FileWriteTool(), FileEditTool()]                                                     
    system_prompt = build_system_prompt(tools)                                                                                               
    messages = [{"role": "system", "content": system_prompt}]                                                                                
                                                                                                                                            
    print("=" * 60)                                                                                                                          
    print("Mini Coding Agent — type 'exit' or 'quit' to leave")                                                                              
    print("=" * 60)                                                                                                                          
                                                                                                                                            
    while True:                                                                                                                              
        user_input = input("\nYou: ").strip()                                                                                                
        if user_input in ("exit", "quit"):                                                                                                   
            break                                                                                                                            
        if not user_input:                                                                                                                   
            continue                                                                                                                         
                                                                                                                                            
        messages.append({"role": "user", "content": user_input})                                                                             
        await agent_loop(messages, tools, client, config)
                                                                                                                                            
if __name__ == "__main__":                                                                                                                   
    asyncio.run(main())
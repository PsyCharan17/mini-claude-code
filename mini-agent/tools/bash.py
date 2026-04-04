import asyncio
from tools.base import BaseTool, ToolResult

class BashTool(BaseTool):
    def name(self) -> str:
        return "bash"

    def description(self) -> str:
        return (
            "Run a bash command on the system. "
            "Use this to navigate the filesystem, view files, or run scripts."
        )

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run"
                }
            },
            "required": ["command"]
        }

    async def execute(self, command: str, **kwargs) -> ToolResult:
        timeout = 30  # Hardcoded timeout of 30 seconds
        
        try:
            # Create the subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for it to finish with a timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                
                output = stdout.decode('utf-8', errors='replace')
                err_output = stderr.decode('utf-8', errors='replace')
                
                full_output = ""
                if output:
                    full_output += f"STDOUT:\n{output}\n"
                if err_output:
                    full_output += f"STDERR:\n{err_output}\n"
                    
                if not full_output.strip():
                    full_output = "Command executed successfully with no output."
                    
                return ToolResult(
                    content=full_output.strip(),
                    is_error=process.returncode != 0
                )
                
            except asyncio.TimeoutError:
                # If command times out, terminate it to prevent runaway processes
                try:
                    process.kill()
                except OSError:
                    pass
                return ToolResult(
                    content=f"Error: Command timed out after {timeout} seconds.",
                    is_error=True
                )
                
        except Exception as e:
            return ToolResult(
                content=f"Exception trying to execute command: {str(e)}",
                is_error=True
            )

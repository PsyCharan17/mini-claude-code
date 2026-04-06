import os

class ListDirTool(BaseTool):
    def name(self) -> str:
        return "list_dir"
    
    def description(self) -> str:
        return "List the files in the current directory"
    
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to list the files in"
                }
            },
            "required": ["path"]
        }
    
    async def execute(self, path: str = ".", **kwargs) -> ToolResult:
        try:
            entries = os.listdir(path)

            formatted = []
            for name in sorted(entries):
                full_path = os.path.join(path, name)
                if os.path.isdir(full_path):
                    formatted.append(f"{name}/ (dir)")
                else:
                    formatted.append(f"{name} (file)")

            return ToolResult(
                content=f"Contents of '{path}':\n" + "\n".join(formatted),
                is_error=False
            )

        except FileNotFoundError:
            return ToolResult(
                content=f"Error: Path '{path}' does not exist.",
                is_error=True
            )
        except PermissionError:
            return ToolResult(
                content=f"Error: Permission denied for '{path}'.",
                is_error=True
            )
        except Exception as e:
            return ToolResult(
                content=f"Error: {str(e)}",
                is_error=True
            )
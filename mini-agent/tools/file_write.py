from tools.base import BaseTool, ToolResult


class FileWriteTool(BaseTool):
    def name(self) -> str:
        return "write_file"

    def description(self) -> str:
        return (
            "Write content to a file. Creates the file if it does not exist, "
            "overwrites it if it does. Will create intermediate directories if needed."
        )

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to write to"
                },
                "content": {
                    "type": "string",
                    "description": "The full content to write to the file"
                }
            },
            "required": ["path", "content"]
        }

    async def execute(self, path: str, content: str, **kwargs) -> ToolResult:
        try:
            import os
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return ToolResult(content=f"Successfully wrote {len(content)} bytes to {path}",is_error=False)
        except Exception as e:
            return ToolResult(content=f"Error writing file: {e}", is_error=True)

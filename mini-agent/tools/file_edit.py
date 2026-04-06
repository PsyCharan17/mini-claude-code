from tools.base import BaseTool, ToolResult


class FileEditTool(BaseTool):
    def name(self) -> str:
        return "edit_file"

    def description(self) -> str:
        return (
            "Replace a specific string in a file with a new string. "
            "The old_string must match exactly (including whitespace). "
            "All occurrences of old_string will be replaced."
        )

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to edit"
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact text to replace (must match exactly, including whitespace)"
                },
                "new_string": {
                    "type": "string",
                    "description": "The new text to replace it with"
                }
            },
            "required": ["path", "old_string", "new_string"]
        }

    async def execute(self, path: str, old_string: str, new_string: str, **kwargs) -> ToolResult:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return ToolResult(content=f"Error: File not found: {path}", is_error=True)
        except UnicodeDecodeError:
            return ToolResult(content=f"Error: File is binary: {path}", is_error=True)

        if old_string not in content:
            return ToolResult(
                content=f"Error: The text to replace was not found in {path}. "
                        f"Make sure it matches exactly, including whitespace.",
                is_error=True,
            )

        count = content.count(old_string)
        content = content.replace(old_string, new_string)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        if count > 1:
            note = f"\nNote: replaced {count} occurrences."
        else:
            note = ""

        return ToolResult(content=f"Successfully replaced text in {path}.{note}")

from tools.base import BaseTool, ToolResult


class FileReadTool(BaseTool):
    def name(self) -> str:
        return "read_file"

    def description(self) -> str:
        return "Read the contents of a file. Supports optional line range slicing."

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read"
                },
                "start_line": {
                    "type": "integer",
                    "description": "Start line number (1-based, inclusive). If omitted, reads from the beginning."
                },
                "end_line": {
                    "type": "integer",
                    "description": "End line number (1-based, inclusive). If omitted, reads to the end."
                }
            },
            "required": ["path"]
        }

    async def execute(self, path: str, start_line: int = None, end_line: int = None, **kwargs) -> ToolResult:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return ToolResult(content=f"Error: File not found: {path}", is_error=True)
        except UnicodeDecodeError:
            return ToolResult(content=f"Error: File appears to be binary and cannot be read as text: {path}", is_error=True)
        except Exception as e:
            return ToolResult(content=f"Error: {e}", is_error=True)

        total = len(lines)

        if start_line is not None or end_line is not None:
            s = (start_line or 1) - 1
            e = end_line if end_line is not None else total
            lines = lines[s:e]
            actual_start = s + 1
            actual_end = min(e, total)
        else:
            actual_start = 1
            actual_end = total

        content = f"Lines {actual_start}-{actual_end} of {path}:\n{''.join(lines)}"
        return ToolResult(content=content.strip(), is_error=False)

    def get_prompt(self) -> str:
        return (
            "Read the contents of a text file and return its lines.\n"
            "\n"
            "Use this tool to:\n"
            "  - Inspect source code, configs, scripts, or logs\n"
            "  - Verify the contents of a file after modifying it\n"
            "  - Understand existing code before making changes\n"
            "\n"
            "Guidelines:\n"
            "  - Always provide an absolute or project-root-relative path\n"
            "  - Use start_line/end_line to read small sections of large files\n"
            "    instead of loading the entire file\n"
            "  - If you need the full file, omit start_line/end_line\n"
            "  - This tool reads as UTF-8 text; binary files will return an error\n"
            "  - For directory listings, use list_dir or bash instead\n"
        )

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from provider import make_tool

@dataclass
class ToolResult:
    """A simple placeholder class to indicate the structure of tool results."""
    content: str
    is_error: bool

class BaseTool(ABC):
    @abstractmethod
    def name(self) -> str:
        """Name of the tool, used in the OpenAI schema."""
        ...

    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        ...

    @abstractmethod
    def parameters(self) -> dict:
        """JSON Schema dictionary defining the expected parameters."""
        ...

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Executes the tool with the matched kwargs.
        Should return a ToolResult-like dictionary (e.g. {"content": "...", "is_error": False})
        """
        ...

    def definition(self) -> dict:
        """Convenience method to format this tool for the OpenAI API."""
        return make_tool(self.name(), self.description(), self.parameters())

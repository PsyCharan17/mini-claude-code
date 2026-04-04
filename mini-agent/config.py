import os
from dotenv import load_dotenv

# Load from the parent directory where your .env file is located!
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
load_dotenv(os.path.join(parent_dir, ".env"))
# Also run the default which looks in the immediate current working directory just in case
load_dotenv()
# ---------------------------------------------------------------------------
# Provider configuration — reads from env vars, all values are validated at
# startup so we fail fast with a clear message instead of a cryptic API error.
# ---------------------------------------------------------------------------

SUPPORTED_PROVIDERS = {"openrouter", "openai"}


class Config:
    def __init__(self):
        provider = os.getenv("AGENT_PROVIDER", "openrouter").lower()
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"AGENT_PROVIDER must be one of {SUPPORTED_PROVIDERS}, got '{provider}'"
            )
        self.provider = provider

        # API key
        key_var = "OPENROUTER_API_KEY" if provider == "openrouter" else "OPENAI_API_KEY"
        self.api_key = os.getenv(key_var)
        if not self.api_key:
            raise ValueError(
                f"Environment variable {key_var} is not set. "
                f"Set it before running the agent."
            )

        # Base URL — OpenRouter has a different endpoint
        if provider == "openrouter":
            self.base_url = os.getenv(
                "AGENT_BASE_URL", "https://openrouter.ai/api/v1"
            )
        else:
            self.base_url = os.getenv("AGENT_BASE_URL", None)  # None = default

        # Model identifier
        self.model = os.getenv(
            "AGENT_MODEL",
            "anthropic/claude-sonnet-4-20250514"  # default for openrouter
        )

    def __repr__(self):
        return (
            f"Config(provider={self.provider!r}, "
            f"model={self.model!r}, "
            f"base_url={self.base_url!r})"
        )

from dataclasses import dataclass, field
import os


@dataclass
class LLMSettings:
    provider: str = "deepseek"
    model: str = "deepseek-chat"
    base_url: str = ""
    api_key: str = ""


@dataclass
class Settings:
    app_name: str = "minibot"
    env: str = "dev"
    llm: LLMSettings = field(default_factory=LLMSettings)

    @classmethod
    def from_env(cls) -> "Settings":
        provider = os.getenv("MINIBOT_LLM_PROVIDER", "deepseek").lower()
        if provider == "ollama":
            model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            api_key = ""
        elif provider == "deepseek":
            model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
            api_key = os.getenv("DEEPSEEK_API_KEY", "")
        else:
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            base_url = os.getenv("OPENAI_BASE_URL", "")
            api_key = os.getenv("OPENAI_API_KEY", "")

        return cls(
            app_name=os.getenv("MINIBOT_APP_NAME", "minibot"),
            env=os.getenv("MINIBOT_ENV", "dev"),
            llm=LLMSettings(
                provider=provider,
                model=model,
                base_url=base_url,
                api_key=api_key,
            ),
        )

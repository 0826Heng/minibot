from dataclasses import dataclass, field
import os
from pathlib import Path

def _load_env_file(env_file: Path) -> None:
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            os.environ.setdefault(key, value)


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
        project_root = Path(__file__).resolve().parents[3]
        _load_env_file(project_root / ".env")

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

from dataclasses import dataclass, field


@dataclass
class MemoryStore:
    data: dict[str, str] = field(default_factory=dict)

    def set(self, key: str, value: str) -> None:
        self.data[key] = value

    def get(self, key: str, default: str = "") -> str:
        return self.data.get(key, default)

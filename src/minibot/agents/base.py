from dataclasses import dataclass


@dataclass
class BaseAgent:
    name: str

    def think(self, user_input: str) -> str:
        raise NotImplementedError("Agent must implement think().")

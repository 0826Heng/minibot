from dataclasses import dataclass


@dataclass
class BaseTool:
    name: str

    def call(self, payload: str) -> str:
        raise NotImplementedError("Tool must implement call().")

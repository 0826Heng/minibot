from dataclasses import dataclass

from minibot.agents.echo_agent import EchoAgent
from minibot.memory.store import MemoryStore


@dataclass
class ChatWorkflow:
    agent: EchoAgent
    memory: MemoryStore

    def run_once(self, user_input: str) -> str:
        self.memory.set("last_user_input", user_input)
        response = self.agent.think(user_input)
        self.memory.set("last_response", response)
        return response

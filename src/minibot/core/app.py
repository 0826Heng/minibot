from dataclasses import dataclass

from minibot.agents.echo_agent import EchoAgent
from minibot.memory.store import MemoryStore
from minibot.workflows.chat_workflow import ChatWorkflow


@dataclass
class MiniBotApp:
    name: str = "minibot"

    def run_once(self, user_input: str) -> str:
        workflow = ChatWorkflow(agent=EchoAgent(), memory=MemoryStore())
        return workflow.run_once(user_input)

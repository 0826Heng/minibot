from minibot.agents.base import BaseAgent
from minibot.tools.echo_tool import EchoTool


class EchoAgent(BaseAgent):
    def __init__(self, name: str = "echo-agent") -> None:
        super().__init__(name=name)
        self.tool = EchoTool(name="echo")

    def think(self, user_input: str) -> str:
        return self.tool.call(f"[{self.name}] {user_input}")

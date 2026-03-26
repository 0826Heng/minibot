from minibot.tools.base import BaseTool


class EchoTool(BaseTool):
    def call(self, payload: str) -> str:
        return payload

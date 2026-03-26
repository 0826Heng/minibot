# Minibot Agent

一个参考 nanobot 思路的 Python Agent 最小框架，包含：

- Agent 抽象与示例实现
- Tool 注册与调用
- Workflow 编排
- Memory 状态存储
- 命令行运行入口

## LLM 配置文件

- 环境变量模板：`.env.example`
- LLM 配置文件：`config/llm.yaml`

建议先复制环境变量模板：

```bash
cp .env.example .env
```

如使用 OpenAI，至少配置：

```bash
MINIBOT_LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

如使用 DeepSeek，至少配置：

```bash
MINIBOT_LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

如使用 Ollama，配置：

```bash
MINIBOT_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2.5:7b
```



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

## 科幻风 Web 界面（上传 + 聊天）

已提供前端页面与后端 API，可直接使用你已配置好的 DeepSeek API。

### 安装依赖

```bash
pip install -e .
```

### 启动服务

```bash
python -m minibot.web.app
```

启动后访问：`http://127.0.0.1:8000`

### 功能说明

- 上传文件：点击上传区选择文件并上传。
- 向量入库：上传后自动解析并分块，写入本地 Chroma 向量库（目录：`.chroma/`）。
- 检索增强聊天：对话时先从向量库检索相关片段，再调用 DeepSeek 生成回答。
- 支持格式：`.txt`、`.md`、`.docx`、`.pdf`（其余格式会提示不支持）。

## 项目过程记录

> 说明：本区块用于记录项目实施过程中的关键操作，按时间顺序持续追加。

### 2026-03-27

1. 明确需求：希望给 Minibot 上传作业文档后，自动生成答案并整合回文档。
2. 创建项目级 Cursor Skill：`homework-doc-solver`。
3. 新增主技能文件：`.cursor/skills/homework-doc-solver/SKILL.md`。
4. 在技能中定义了完整流程：文档识别、题目抽取、答案生成、答案回填、质量检查。
5. 新增参考文件：`.cursor/skills/homework-doc-solver/reference.md`。
6. 在参考文件中补充了短答题、解释题、代码题模板，以及覆盖率检查模板。
7. 修复参考文件中的嵌套代码块渲染问题，确保 Markdown 可正确展示。
8. 进行基本检查，确认新增 Skill 文件无明显格式问题。
9. 新增依赖：`fastapi`、`uvicorn`、`python-multipart`、`httpx`，用于 Web 服务与文件上传。
10. 新建 Web 后端：`src/minibot/web/app.py`，提供 `/`、`/api/upload`、`/api/chat` 接口。
11. 新建科幻风前端页面：`src/minibot/web/static/index.html`、`styles.css`、`main.js`。
12. 前端支持文件上传、聊天消息展示、调用后端接口并呈现回复。
13. 后端已接入环境变量中的 LLM 配置，按 DeepSeek/OpenAI 兼容格式调用 `chat/completions`。
14. 更新 README：补充 Web 界面启动方式与功能说明，便于后续演示与记录追踪。
15. 用户反馈网页无法打开，开始排查启动与环境问题。
16. 检查终端日志后确认失败原因：系统 Python 3.9 不满足 `>=3.10`，且启动模块名误写为 `minibot.web.ap`。
17. 使用 `.venv` 的 Python 并执行正确命令 `python -m minibot.web.app` 后，服务可正常启动在 `0.0.0.0:8000`。
18. 补充 README 常见问题排查章节，记录正确启动命令和错误示例，降低复现概率。
19. 用户反馈聊天时报 `Missing LLM API key`，定位为服务进程未自动加载 `.env` 导致环境变量缺失。
20. 在 `Settings.from_env()` 中加入项目根目录 `.env` 自动加载逻辑，并新增 `python-dotenv` 依赖。
21. 更新 README 故障排查条目，补充 key 缺失时的检查步骤。
22. 用户提供 DeepSeek API Key 与地址，请求直接代为配置运行环境。
23. 新增项目根目录 `.env` 并写入 `MINIBOT_LLM_PROVIDER=deepseek`、`DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL`、`DEEPSEEK_BASE_URL`。
24. 将 DeepSeek 地址规范化为 `https://api.deepseek.com/v1`，以匹配 OpenAI 兼容 `chat/completions` 路径。
25. 用户反馈上传文件无法解析，提出接入 embedding 与 Chroma 向量数据库需求。
26. 新增 RAG 模块：`src/minibot/rag/document_parser.py`（文档解析与分块）。
27. 新增 Chroma 封装：`src/minibot/rag/vector_store.py`（持久化向量库索引与检索）。
28. Web 上传接口改为“解析 -> 分块 -> 向量入库”，并返回分块数量。
29. Web 聊天接口改为“先向量检索上下文，再调用 DeepSeek 回答”。
30. 前端上传成功提示增加“已入库分块数”，便于确认 embedding 生效。

### 维护约定

- 后续每次关键变更都在本章节按“日期 + 编号步骤”追加记录。
- 记录内容建议包含：目标、修改文件、执行动作、结果与风险说明。


from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from minibot.config.settings import Settings
from minibot.rag.document_parser import chunk_text, parse_document
from minibot.rag.vector_store import ChromaStore


class ChatRequest(BaseModel):
    message: str
    file_context: str = ""


class ChatResponse(BaseModel):
    reply: str


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = Path.cwd() / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR = Path.cwd() / ".chroma"
STORE = ChromaStore(persist_dir=CHROMA_DIR)

app = FastAPI(title="Minibot Sci-Fi UI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _build_headers(settings: Settings) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if settings.llm.api_key:
        headers["Authorization"] = f"Bearer {settings.llm.api_key}"
    return headers


async def _call_deepseek(prompt: str) -> str:
    settings = Settings.from_env()
    if not settings.llm.base_url:
        raise HTTPException(status_code=500, detail="Missing LLM base URL.")
    if not settings.llm.api_key:
        raise HTTPException(status_code=500, detail="Missing LLM API key.")

    api_url = f"{settings.llm.base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.llm.model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是 Minibot。请用简体中文回答，给出清晰、可执行、"
                    "尽量结构化的结果。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }

    timeout = httpx.Timeout(60.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(api_url, headers=_build_headers(settings), json=payload)
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"LLM request failed: {resp.text}",
            )
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    save_path = UPLOAD_DIR / file.filename
    content = await file.read()
    save_path.write_bytes(content)

    try:
        text = parse_document(save_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - parser runtime errors
        raise HTTPException(status_code=500, detail=f"解析文档失败: {exc}") from exc

    chunks = chunk_text(text)
    indexed_count = STORE.index_chunks(file.filename, chunks)
    preview = text[:1200]
    return {
        "filename": file.filename,
        "saved_to": str(save_path),
        "preview": preview,
        "indexed_chunks": str(indexed_count),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    user_prompt = req.message.strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    retrieved_docs = STORE.search(user_prompt, top_k=4)
    rag_context = "\n\n".join(retrieved_docs).strip()
    prompt = user_prompt
    if rag_context:
        prompt = (
            "以下是从向量数据库检索到的文档片段，请优先基于这些内容回答。\n\n"
            f"[检索片段开始]\n{rag_context}\n[检索片段结束]\n\n"
            f"用户问题：{user_prompt}"
        )
    elif req.file_context.strip():
        prompt = (
            "以下是用户上传文件的内容片段，请结合该内容回答用户问题。\n\n"
            f"[文件片段开始]\n{req.file_context.strip()}\n[文件片段结束]\n\n"
            f"用户问题：{user_prompt}"
        )

    reply = await _call_deepseek(prompt)
    return ChatResponse(reply=reply)


if __name__ == "__main__":
    # local start: python -m minibot.web.app
    import uvicorn

    uvicorn.run("minibot.web.app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

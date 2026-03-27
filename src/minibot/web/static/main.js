const chatBox = document.getElementById("chatBox");
const uploadBtn = document.getElementById("uploadBtn");
const sendBtn = document.getElementById("sendBtn");
const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");
const messageInput = document.getElementById("messageInput");

let fileContext = "";

function addMessage(role, content) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = content;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    uploadStatus.textContent = "请先选择文件";
    return;
  }

  const fd = new FormData();
  fd.append("file", file);
  uploadStatus.textContent = "上传中...";

  try {
    const resp = await fetch("/api/upload", {
      method: "POST",
      body: fd,
    });
    if (!resp.ok) {
      throw new Error(await resp.text());
    }
    const data = await resp.json();
    fileContext = data.preview || "";
    uploadStatus.textContent = `上传成功：${data.filename}，已入库分块 ${data.indexed_chunks}`;
    addMessage(
      "bot",
      `文件已接收：${data.filename}\n已写入向量库分块：${data.indexed_chunks}\n可开始提问。`
    );
  } catch (err) {
    uploadStatus.textContent = `上传失败：${err.message}`;
  }
});

sendBtn.addEventListener("click", async () => {
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  messageInput.value = "";

  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        file_context: fileContext,
      }),
    });
    if (!resp.ok) {
      throw new Error(await resp.text());
    }
    const data = await resp.json();
    addMessage("bot", data.reply);
  } catch (err) {
    addMessage("bot", `请求失败：${err.message}`);
  }
});

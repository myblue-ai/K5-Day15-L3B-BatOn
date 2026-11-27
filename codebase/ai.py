"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    giả lập quyết định thiếu căn cứ, model "fake", token 0 — để luồng chạy hết trước CP2.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối DeepInfra hoặc OpenAI bằng .env, xem docs/connect-model.md.
Không dán API key vào file này.
"""
import json
import os
from urllib.request import Request, urlopen

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
CHAT_ENDPOINTS = {
    "deepinfra": "https://api.deepinfra.com/v1/openai/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
}
# Nhà cung cấp trung gian theo chuẩn OpenAI: đặt OPENAI_BASE_URL (vd https://.../v1) trong .env.
OPENAI_BASE_URL = (os.environ.get("OPENAI_BASE_URL") or "").strip().rstrip("/")
if OPENAI_BASE_URL:
    CHAT_ENDPOINTS["openai"] = OPENAI_BASE_URL + "/chat/completions"


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        return {"text": '{"action":"no_source"}', "model": "fake", "tokens_in": 0, "tokens_out": 0}

    endpoint = CHAT_ENDPOINTS.get(MODEL_PROVIDER)
    if endpoint is None:
        raise NotImplementedError(f"Chưa hỗ trợ MODEL_PROVIDER={MODEL_PROVIDER}")
    if not MODEL_NAME or not API_KEY:
        raise ValueError(f"Điền MODEL_NAME và API_KEY trong .env để gọi {MODEL_PROVIDER}.")

    messages = [{"role": "user", "content": user}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    payload = {"model": MODEL_NAME, "messages": messages}
    if MODEL_PROVIDER == "deepinfra":
        payload.update(
            response_format={"type": "json_object"},
            reasoning_effort="none",
            max_tokens=768,
        )
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=90) as response:
        result = json.load(response)

    text = result["choices"][0]["message"]["content"]
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError(f"{MODEL_PROVIDER} không trả nội dung văn bản.")
    usage = result["usage"]
    return {
        "text": text,
        "model": result["model"],
        "tokens_in": usage["prompt_tokens"],
        "tokens_out": usage["completion_tokens"],
    }

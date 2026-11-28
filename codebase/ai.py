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
from pathlib import Path
from urllib.request import HTTPRedirectHandler, Request, build_opener

from model_config import DEFAULT_URLS, ModelConfig, ModelConfigStore
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
CONFIG_DIR = os.environ.get("MODEL_CONFIG_DIR", "").strip()
provider = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
base_url = os.environ.get("OPENAI_BASE_URL", "").strip().rstrip("/") if provider == "openai" else ""
STORE = ModelConfigStore(
    ModelConfig(provider, os.environ.get("MODEL_NAME", "").strip(),
                base_url or DEFAULT_URLS.get(provider, ""), os.environ.get("API_KEY", "").strip()),
    Path(CONFIG_DIR) / "model.json" if CONFIG_DIR else None,
)


class PublicModelDisabled(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward a provider credential to a URL from a response header.
        return None


@model_call
def call_model(system: str, user: str) -> dict:
    state = STORE.snapshot()
    if not state.public_enabled:
        raise PublicModelDisabled
    return request_model(state.config, system, user)


def request_model(config, system, user, *, timeout=90, test=False):
    if config.provider == "fake":
        return {"text": '{"action":"no_source"}', "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if config.provider not in DEFAULT_URLS:
        raise NotImplementedError("Nhà cung cấp model chưa được hỗ trợ.")
    if not config.model or not config.api_key:
        raise ValueError("Cần cấu hình model và API key.")

    messages = [{"role": "user", "content": user}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    payload = {"model": config.model, "messages": messages}
    if config.provider == "deepinfra":
        payload.update(
            response_format={"type": "json_object"},
            reasoning_effort="none",
            max_tokens=256 if test else 768,
        )
    request = Request(
        config.base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
        result = json.loads(response.read(1024 * 1024))

    text = result["choices"][0]["message"]["content"]
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("Model không trả nội dung văn bản.")
    usage = result["usage"]
    return {
        "text": text,
        "model": result["model"],
        "tokens_in": usage["prompt_tokens"],
        "tokens_out": usage["completion_tokens"],
    }

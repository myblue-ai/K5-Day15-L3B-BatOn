"""Single-process model settings with atomic persistence for the web admin."""

import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit


DEFAULT_URLS = {
    "deepinfra": "https://api.deepinfra.com/v1/openai",
    "openai": "https://api.openai.com/v1",
}


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    base_url: str
    api_key: str = field(repr=False)

    def public(self):
        return {
            "provider": self.provider, "model": self.model, "base_url": self.base_url,
            "has_key": bool(self.api_key),
        }


@dataclass(frozen=True)
class State:
    config: ModelConfig
    previous: ModelConfig | None = None
    public_enabled: bool = True
    revision: int = 0


def normalize_url(value):
    value = value.strip().rstrip("/")
    if (len(value) > 1024 or any(ord(c) < 33 or ord(c) >= 127 for c in value)
            or any(char in value for char in "\\?#")):
        raise ValueError("Base URL phải là endpoint HTTPS hợp lệ, không có tham số.")
    try:
        url = urlsplit(value)
        host = url.hostname or ""
        if (url.scheme != "https" or url.username is not None or url.port not in (None, 443)
                or not re.fullmatch(r"[a-z0-9.-]+\.[a-z][a-z0-9-]*", host)):
            raise ValueError
        return url._replace(netloc=host).geturl()
    except ValueError:
        raise ValueError("Base URL phải dùng tên miền HTTPS, không chứa thông tin đăng nhập.") from None


def allowed_urls():
    extra = os.environ.get("MODEL_ALLOWED_BASE_URLS", "").split(",")
    return {DEFAULT_URLS["openai"], *(normalize_url(url) for url in extra if url.strip())}


def draft_config(payload, current):
    values = [payload.get(name, "") for name in ("provider", "model", "base_url", "api_key")]
    if not all(isinstance(value, str) for value in values):
        raise ValueError("Cấu hình không đúng định dạng.")
    provider, model, base_url, key = (value.strip() for value in values)
    if provider not in DEFAULT_URLS:
        raise ValueError("Chọn DeepInfra hoặc gateway tương thích OpenAI.")
    if not model or len(model) > 160 or any(ord(c) < 33 or ord(c) > 126 for c in model):
        raise ValueError("Nhập mã model hợp lệ.")
    base_url = normalize_url(base_url or DEFAULT_URLS[provider])
    approved = {DEFAULT_URLS["deepinfra"]} if provider == "deepinfra" else allowed_urls()
    if base_url not in approved:
        raise ValueError("Base URL chưa nằm trong danh sách endpoint được phép.")
    if not key and (provider, base_url) == (current.provider, current.base_url):
        key = current.api_key
    if not key or len(key) > 4096 or any(ord(c) < 33 or ord(c) > 126 for c in key):
        raise ValueError("Nhập API key của gateway đã chọn.")
    return ModelConfig(provider, model, base_url, key)


class StaleConfig(Exception):
    pass


class ModelConfigStore:
    def __init__(self, config, path=None):
        self.path = path
        self.lock = Lock()
        self.state = self.load() or State(config)

    def load(self):
        if not self.path:
            return None
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        try:
            if (type(data["public_enabled"]) is not bool or type(data["revision"]) is not int
                    or data["revision"] < 0):
                raise ValueError
            previous = data["previous"]
            return State(ModelConfig(**data["config"]), ModelConfig(**previous) if previous else None,
                         data["public_enabled"], data["revision"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("Tệp cấu hình model không hợp lệ.") from None

    def snapshot(self):
        with self.lock:
            return self.state

    def change(self, revision, *, config=None, public_enabled=None, rollback=False):
        with self.lock:
            current = self.state
            if revision != current.revision:
                raise StaleConfig
            updated = current
            if rollback:
                if current.previous is None:
                    raise ValueError("Chưa có phiên bản để quay lại.")
                updated = replace(current, config=current.previous, previous=current.config)
            elif config is not None and config != current.config:
                updated = replace(current, config=config, previous=current.config)
            elif public_enabled is not None:
                updated = replace(current, public_enabled=public_enabled)
            if updated == current:
                return current
            updated = replace(updated, revision=current.revision + 1)
            self.save(updated)
            self.state = updated
            return updated

    def save(self, state):
        if not self.path:
            raise OSError("Chưa gắn thư mục cấu hình.")
        fd, name = tempfile.mkstemp(prefix=".config-", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(asdict(state), handle)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(name, self.path)
        finally:
            Path(name).unlink(missing_ok=True)

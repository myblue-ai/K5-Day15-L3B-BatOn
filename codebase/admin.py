"""Private admin listener. Its host port is reachable through the SSH tunnel."""

import hmac
import json
import secrets
import time
from pathlib import Path
from threading import Lock
from urllib.error import HTTPError
from urllib.parse import urlsplit

from ai import STORE, request_model
from http_io import HttpHandler, InputError
from model_config import StaleConfig, draft_config


def public_state(state):
    return {
        "config": state.config.public(), "revision": state.revision,
        "public_enabled": state.public_enabled, "can_rollback": state.previous is not None,
    }


class Admin:
    def __init__(self, traffic, token_file):
        self.traffic = traffic
        self.token = Path(token_file).read_text(encoding="ascii").strip()
        if len(self.token) < 32 or not self.token.isalnum():
            raise ValueError("Token quản trị không hợp lệ.")
        self.page = Path(__file__).with_name("admin.html").read_bytes()
        self.test_lock = Lock()
        self.ticket_lock = Lock()
        self.pending = None

    def test(self, payload, current):
        draft = draft_config(payload, current.config)
        if not self.test_lock.acquire(blocking=False):
            raise InputError(429, "Một lượt kiểm tra khác đang chạy.")
        try:
            with self.ticket_lock:
                self.pending = None
            try:
                result = request_model(
                    draft, 'Reply with exactly one JSON object: {"action":"no_source"}.',
                    "Return the JSON object now.", timeout=60, test=True,
                )
                if json.loads(result["text"]) != {"action": "no_source"}:
                    raise ValueError
                if not all(type(result[k]) is int and result[k] > 0 for k in ("tokens_in", "tokens_out")):
                    raise ValueError
            except HTTPError as exc:
                self.traffic.record("admin", "test_failed", exc.code)
                raise InputError(502, f"Gateway trả lỗi HTTP {exc.code}. Kiểm tra key, model và base URL.") from None
            except Exception:
                self.traffic.record("admin", "test_failed")
                raise InputError(502, "Gateway không phản hồi đúng định dạng hoặc đã hết thời gian chờ.") from None
            if STORE.snapshot().revision != current.revision:
                raise StaleConfig
            ticket = secrets.token_urlsafe(24)
            with self.ticket_lock:
                self.pending = (ticket, draft, current.revision, time.monotonic() + 300)
            self.traffic.record("admin", "tested")
            return {"ticket": ticket, "config": draft.public()}
        finally:
            self.test_lock.release()

    def apply(self, payload, revision):
        with self.ticket_lock:
            if self.pending is None:
                raise ValueError("Cần kiểm tra cấu hình trước khi áp dụng.")
            ticket, config, tested_revision, expiry = self.pending
            if (payload.get("ticket") != ticket or tested_revision != revision
                    or time.monotonic() >= expiry):
                raise ValueError("Phiên kiểm tra đã hết hiệu lực. Hãy kiểm tra lại.")
            changed = STORE.change(revision, config=config)
            self.pending = None
        if changed.revision != revision:
            self.traffic.record("admin", "applied")
        return changed


class AdminHandler(HttpHandler):
    def end_headers(self):
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
        )
        super().end_headers()

    def permitted_host(self):
        host = self.headers.get("Host", "")
        try:
            authority = urlsplit("http://" + host)
        except ValueError:
            return False
        origin = self.headers.get("Origin")
        return (authority.netloc == host and authority.hostname in {"localhost", "127.0.0.1", "::1"}
                and authority.username is None and (origin is None or origin == "http://" + host))

    def authorize(self):
        if not self.permitted_host():
            raise InputError(403, "Hãy mở admin qua SSH tunnel trên máy của bạn.")
        expected = "Bearer " + self.server.admin.token
        if not hmac.compare_digest(self.headers.get("Authorization", "").encode(), expected.encode()):
            raise InputError(401, "Token quản trị không đúng.")

    def do_GET(self):
        try:
            if self.path == "/":
                if not self.permitted_host():
                    raise InputError(403, "Hãy mở admin qua SSH tunnel trên máy của bạn.")
                return self.send_body(200, self.server.admin.page, "text/html; charset=utf-8")
            self.authorize()
            if self.path == "/api/state":
                return self.send_json(200, {"state": public_state(STORE.snapshot()),
                                            "traffic": self.server.admin.traffic.snapshot()})
            raise InputError(404, "Đường dẫn không tồn tại.")
        except InputError as exc:
            self.send_json(exc.status, {"error": str(exc)})

    def do_POST(self):
        try:
            self.authorize()
            payload = self.read_json(8192)
            revision = payload.get("revision")
            current = STORE.snapshot()
            if type(revision) is not int or revision != current.revision:
                raise StaleConfig
            admin = self.server.admin
            if self.path == "/api/model/test":
                return self.send_json(200, admin.test(payload, current))
            if self.path == "/api/model/apply":
                state = admin.apply(payload, revision)
            elif self.path == "/api/model/rollback":
                state = STORE.change(revision, rollback=True)
                admin.traffic.record("admin", "rolled_back")
            elif self.path == "/api/public":
                enabled = payload.get("enabled")
                if type(enabled) is not bool:
                    raise ValueError("Chọn bật hoặc khoá lượt gọi công khai.")
                state = STORE.change(revision, public_enabled=enabled)
                if state.revision != revision:
                    admin.traffic.record("admin", "public_enabled" if enabled else "public_disabled")
            else:
                raise InputError(404, "Đường dẫn không tồn tại.")
            self.send_json(200, {"state": public_state(state)})
        except InputError as exc:
            self.send_json(exc.status, {"error": str(exc)})
        except StaleConfig:
            self.send_json(409, {"error": "Cấu hình đã thay đổi. Hãy tải trạng thái mới và thử lại."})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except OSError:
            self.server.admin.traffic.record("admin", "save_failed")
            self.send_json(500, {"error": "Không lưu được cấu hình trên máy chủ."})

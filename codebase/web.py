"""Same-origin demo for the existing Day01 agent. Run with python codebase/web.py."""

import json
import os
import sys
import threading
import time
from collections import deque
from http.server import ThreadingHTTPServer
from pathlib import Path

from admin import Admin, AdminHandler
from agent import answer
from ai import CONFIG_DIR, STORE, PublicModelDisabled
from http_io import HttpHandler, InputError
from tools import read_lesson_segments
from traffic import Traffic


PAGE = (Path(__file__).parent / "index.html").read_bytes()
MAX_QUESTION = 1500
slots = threading.BoundedSemaphore(4)
calls = deque()
calls_lock = threading.Lock()
hourly_limit = int(os.environ.get("CHAT_CALLS_PER_HOUR", "120"))
traffic = Traffic()


def question_for_agent(payload):
    if not isinstance(payload, dict):
        raise ValueError
    question = payload.get("message")
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= MAX_QUESTION:
        raise ValueError
    question = question.strip()
    history = payload.get("history", [])
    if not isinstance(history, list) or len(history) > 4:
        raise ValueError
    turns = []
    for turn in history:
        if not isinstance(turn, dict) or turn.get("role") not in ("user", "assistant"):
            raise ValueError
        content = turn.get("content")
        if not isinstance(content, str) or len(content) > 1500:
            raise ValueError
        turns.append({"role": turn["role"], "content": content})
    if not turns:
        return question
    return ("Lịch sử để hiểu câu hỏi tiếp theo. Chỉ các đoạn bài được cấp là nguồn.\n"
            + json.dumps(turns, ensure_ascii=False) + "\nCâu hỏi hiện tại: " + question)


class Handler(HttpHandler):
    metric = None

    def send_body(self, status, body, mime):
        if self.metric is not None:
            result = "page_view" if self.metric == "page" else {
                200: "chat_ok", 429: "chat_limited", 502: "chat_error", 503: "chat_blocked",
            }.get(status, "chat_invalid")
            traffic.record(self.metric, result, status, round((time.perf_counter() - self.started) * 1000))
        super().send_body(status, body, mime)

    def do_GET(self):
        path = self.path.partition("?")[0]
        if path == "/":
            self.metric = "page"
            self.started = time.perf_counter()
            self.send_body(200, PAGE, "text/html; charset=utf-8")
        elif path == "/health":
            self.send_json(200, {"status": "ok"})
        elif path == "/api/lesson":
            self.send_json(200, {"segments": read_lesson_segments()})
        else:
            self.send_json(404, {"error": "Đường dẫn không tồn tại."})

    def do_POST(self):
        if self.path not in ("/api/chat", "/api/call"):
            return self.send_json(404, {"error": "Đường dẫn không tồn tại."})
        self.metric = "chat"
        self.started = time.perf_counter()
        if not STORE.snapshot().public_enabled:
            return self.send_disabled()
        try:
            question = question_for_agent(self.read_json(32768))
        except InputError as exc:
            return self.send_json(exc.status, {"error": str(exc)})
        except ValueError:
            return self.send_json(400, {"error": "Kiểm tra câu hỏi và lịch sử hội thoại."})
        if not slots.acquire(blocking=False):
            return self.send_json(429, {"error": "Trợ giảng đang bận. Bạn thử lại sau nhé."})
        try:
            now = time.monotonic()
            with calls_lock:
                while calls and calls[0] <= now - 3600:
                    calls.popleft()
                allowed = len(calls) < hourly_limit
                if allowed:
                    calls.append(now)
            if not allowed:
                return self.send_json(429, {"error": "Bản demo đã dùng hết lượt hỏi trong giờ này."})
            try:
                result = answer(question)
            except PublicModelDisabled:
                return self.send_disabled()
            except Exception as exc:
                print("agent call failed:", type(exc).__name__, file=sys.stderr, flush=True)
                return self.send_json(502, {"error": "Chưa nhận được phản hồi từ model. Bạn thử gửi lại nhé."})
            self.send_json(200, result)
        finally:
            slots.release()

    def send_disabled(self):
        self.send_json(503, {"error": "Trợ giảng đang tạm đóng lượt hỏi công khai."})


if __name__ == "__main__":
    address = (os.environ.get("BIND_HOST", "127.0.0.1"), int(os.environ.get("PORT", "8091")))
    server = ThreadingHTTPServer(address, Handler)
    admin_port = os.environ.get("ADMIN_PORT")
    if admin_port:
        if not CONFIG_DIR:
            raise ValueError("MODEL_CONFIG_DIR là bắt buộc khi bật admin.")
        admin = ThreadingHTTPServer((address[0], int(admin_port)), AdminHandler)
        admin.admin = Admin(traffic, Path(CONFIG_DIR) / "admin-token")
        threading.Thread(target=admin.serve_forever, name="admin-listener", daemon=True).start()
    print("Day01 web listening on %s:%d" % address, flush=True)
    server.serve_forever()

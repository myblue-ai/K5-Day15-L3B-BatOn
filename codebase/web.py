"""Same-origin demo for the existing Day01 agent. Run with python codebase/web.py."""

import json
import os
import sys
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from agent import answer
from tools import read_lesson_segments


PAGE = (Path(__file__).parent / "index.html").read_bytes()
MAX_QUESTION = 1500
slots = threading.BoundedSemaphore(4)
calls = deque()
calls_lock = threading.Lock()
hourly_limit = int(os.environ.get("CHAT_CALLS_PER_HOUR", "120"))


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


class Handler(BaseHTTPRequestHandler):
    def send_body(self, status, body, mime):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        self.send_body(status, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        path = self.path.partition("?")[0]
        if path == "/":
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
        if self.headers.get_content_type() != "application/json":
            return self.send_json(415, {"error": "Cần gửi dữ liệu JSON."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= 32768:
                return self.send_json(413, {"error": "Nội dung quá dài hoặc trống."})
            self.connection.settimeout(12)
            question = question_for_agent(json.loads(self.rfile.read(size).decode("utf-8")))
        except (ValueError, TimeoutError, RecursionError):
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
            except Exception as exc:
                print("agent call failed:", type(exc).__name__, file=sys.stderr, flush=True)
                return self.send_json(502, {"error": "Chưa nhận được phản hồi từ model. Bạn thử gửi lại nhé."})
            self.send_json(200, result)
        finally:
            slots.release()

    def log_message(self, fmt, *args):
        # Omit client addresses, query strings and chat text from the demo logs.
        pass


if __name__ == "__main__":
    address = (os.environ.get("BIND_HOST", "127.0.0.1"), int(os.environ.get("PORT", "8091")))
    server = ThreadingHTTPServer(address, Handler)
    print("Day01 web listening on %s:%d" % address, flush=True)
    server.serve_forever()

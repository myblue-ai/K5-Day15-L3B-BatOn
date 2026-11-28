"""HTTP helpers used by the public and private listeners."""

import json
from http.server import BaseHTTPRequestHandler


class InputError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class HttpHandler(BaseHTTPRequestHandler):
    def setup(self):
        self.request.settimeout(12)
        super().setup()

    def send_body(self, status, body, mime):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        self.send_body(status, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def read_json(self, max_bytes):
        if self.headers.get_content_type() != "application/json":
            raise InputError(415, "Cần gửi dữ liệu JSON.")
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= max_bytes:
                raise InputError(413, "Nội dung quá dài hoặc trống.")
            raw = self.rfile.read(size)
            if len(raw) != size:
                raise ValueError
            value = json.loads(raw.decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError
            return value
        except (ValueError, TimeoutError, RecursionError):
            raise InputError(400, "Dữ liệu JSON không hợp lệ.") from None

    def log_message(self, fmt, *args):
        # Never log client addresses, raw paths, headers or request bodies.
        pass

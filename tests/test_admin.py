"""Regression checks for credential updates and the public API kill switch."""

import http.client
import json
import sys
import tempfile
import threading
import unittest
from contextlib import ExitStack
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))

import admin
import ai
import web
from model_config import DEFAULT_URLS, ModelConfig, ModelConfigStore


TOKEN = "test" * 16
KEY = "not-a-real-provider-key"


class AdminTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name)
        token_path = path / "admin-token"
        token_path.write_text(TOKEN, encoding="ascii")
        self.initial = ModelConfig("deepinfra", "test-original", DEFAULT_URLS["deepinfra"], KEY)
        self.store = ModelConfigStore(self.initial, path / "model.json")
        stack = ExitStack()
        self.addCleanup(stack.close)
        for module in (admin, ai, web):
            stack.enter_context(patch.object(module, "STORE", self.store))
        stack.enter_context(patch.object(web, "traffic", web.Traffic()))
        stack.enter_context(patch.object(web, "calls", web.deque()))
        self.public = self.open(web.Handler)
        self.private = self.open(admin.AdminHandler)
        self.private.admin = admin.Admin(web.traffic, token_path)

    def open(self, handler):
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        thread.start()
        return server

    def request(self, server, path, data=None, headers=None):
        conn = http.client.HTTPConnection(*server.server_address, timeout=5)
        try:
            headers = dict(headers or {})
            if data is not None:
                headers["Content-Type"] = "application/json"
            conn.request("GET" if data is None else "POST", path,
                         None if data is None else json.dumps(data), headers)
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def manage(self, path, data=None):
        return self.request(self.private, path, data, {"Authorization": "Bearer " + TOKEN})

    def draft(self, **overrides):
        values = {"revision": self.store.snapshot().revision, "provider": "deepinfra",
                  "model": "test-changed", "base_url": "", "api_key": ""}
        return {**values, **overrides}

    def test_admin_private_and_key_never_returned(self):
        self.assertEqual(self.request(self.public, "/api/state")[0], 404)
        self.assertEqual(self.request(self.private, "/api/state")[0], 401)
        bad_headers = {"Authorization": "Bearer " + TOKEN, "Origin": "https://other.example"}
        self.assertEqual(self.request(self.private, "/api/state", headers=bad_headers)[0], 403)
        status, result = self.manage("/api/state")
        self.assertEqual(status, 200)
        self.assertTrue(result["state"]["config"]["has_key"])
        self.assertNotIn(KEY, json.dumps(result))

    def test_requires_approved_endpoint_and_new_key_on_provider_change(self):
        with patch.object(admin, "request_model") as external:
            for draft in (
                self.draft(provider="openai", base_url="https://unapproved.example/v1", api_key=KEY),
                self.draft(provider="openai", base_url=DEFAULT_URLS["openai"]),
            ):
                self.assertEqual(self.manage("/api/model/test", draft)[0], 400)
            external.assert_not_called()

    def test_verified_revision_can_apply_and_rollback_without_restart(self):
        reply = {"text": '{"action":"no_source"}', "tokens_in": 5, "tokens_out": 4}
        with patch.object(admin, "request_model", return_value=reply) as test_model:
            status, result = self.manage("/api/model/test", self.draft())
        self.assertEqual(status, 200)
        self.assertEqual(test_model.call_args.args[0].api_key, KEY)
        self.assertEqual(self.store.snapshot().config, self.initial)
        self.assertNotIn(KEY, json.dumps(result))
        self.assertEqual(self.manage("/api/model/apply", {"revision": 0, "ticket": result["ticket"]})[0], 200)
        self.assertEqual(self.manage("/api/model/apply", {"revision": 0, "ticket": result["ticket"]})[0], 409)
        with patch.object(ai, "request_model", return_value={"text": "{}", "model": "stub",
                                                            "tokens_in": 5, "tokens_out": 4}) as answer:
            self.assertEqual(self.request(self.public, "/api/chat", {"message": "Test"})[0], 200)
        self.assertEqual(answer.call_args.args[0].model, "test-changed")
        self.assertEqual(ModelConfigStore(self.initial, self.store.path).snapshot().config.model, "test-changed")
        self.assertEqual(self.manage("/api/model/rollback", {"revision": 1})[0], 200)
        self.assertEqual(self.store.snapshot().config, self.initial)

    def test_denied_requests_never_call_provider_and_survive_restart(self):
        self.assertEqual(self.manage("/api/public", {"revision": 0, "enabled": False})[0], 200)
        with patch.object(ai, "request_model") as external:
            for path in ("/api/chat", "/api/call"):
                self.assertEqual(self.request(self.public, path, {"message": "Test"})[0], 503)
            external.assert_not_called()
        self.assertFalse(ModelConfigStore(self.initial, self.store.path).snapshot().public_enabled)
        self.assertEqual(self.manage("/api/state")[1]["traffic"]["counts"]["chat_blocked"], 2)
        self.assertEqual(self.manage("/api/public", {"revision": 1, "enabled": True})[0], 200)
        self.assertTrue(self.store.snapshot().public_enabled)


if __name__ == "__main__":
    unittest.main()

"""Additional security regression tests to cover fixed vulnerabilities."""

import json
import unittest

from service import Shop


class SecurityTest(unittest.TestCase):
    def setUp(self):
        self.shop = Shop()
        self.addCleanup(self.shop.close)

    def request(self, method, path, body=None, headers=None):
        with self.shop.lock:
            return self.shop.dispatch(method, path, body or {}, headers or {})

    def login(self, username="alice", password="learn-alice"):
        status, result = self.request("POST", "/login", {"username": username, "password": password})
        self.assertEqual(status, 200)
        return {"X-Token": result["token"]}

    def test_profile_requires_auth_and_is_scoped(self):
        self.assertEqual(self.request("GET", "/profile?id=2")[0], 401)
        auth = self.login()
        status, rows = self.request("GET", "/profile?id=999", headers=auth)
        self.assertEqual(status, 200)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "TEST_ALICE")

    def test_orders_require_auth_and_only_own(self):
        self.assertEqual(self.request("GET", "/orders")[0], 401)
        alice = self.login()
        status, orders = self.request("GET", "/orders", headers=alice)
        self.assertEqual(status, 200)
        self.assertTrue(all(o["owner"] == 1 for o in orders))

    def test_admin_export_by_session_role_only(self):
        # header-only role is ignored
        self.assertEqual(self.request("GET", "/admin/export", headers={"X-Role": "staff"})[0], 403)
        # staff session passes
        staff = self.login("staff", "learn-staff")
        status, profiles = self.request("GET", "/admin/export", headers=staff)
        self.assertEqual(status, 200)
        self.assertEqual(len(profiles), 2)

    def test_files_user_scoped_and_staff_access(self):
        alice = self.login()
        # alice cannot read bob's file
        self.assertEqual(self.request("GET", "/files?user=bob&path=receipt.txt", headers=alice)[0], 403)
        # staff can read under files/bob
        staff = self.login("staff", "learn-staff")
        status, data = self.request("GET", "/files?user=bob&path=receipt.txt", headers=staff)
        self.assertEqual(status, 200)
        self.assertIn("TEST_BOB", data["content"])

    def test_reviews_are_escaped(self):
        alice = self.login()
        self.assertEqual(self.request("POST", "/reviews", {"product": "chair", "text": "<img src=x onerror=alert(1)>"}, headers=alice)[0], 201)
        status, html = self.request("GET", "/reviews/view", headers=alice)
        self.assertEqual(status, 200)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)

    def test_assistant_context_and_tools_rbac(self):
        alice = self.login()
        # context requires auth and scopes orders
        status, ctx = self.request("GET", "/assistant/context?order_id=2", headers=alice)
        self.assertEqual(status, 200)
        self.assertIn("Заказ: []", ctx["prompt"])  # alice cannot see bob's order
        # tools: customers restricted
        self.assertEqual(self.request("POST", "/assistant/execute", {"decision": {"tool": "export_profiles"}}, headers=alice)[0], 403)
        self.assertEqual(self.request("POST", "/assistant/execute", {"decision": {"tool": "delete_tree", "arguments": {"path": "files/alice"}}}, headers=alice)[0], 403)
        self.assertEqual(self.request("POST", "/assistant/execute", {"decision": {"tool": "read_file", "arguments": {"path": "private/operator-note.txt"}}}, headers=alice)[0], 403)
        # allowed path for alice
        status, res = self.request("POST", "/assistant/execute", {"decision": {"tool": "read_file", "arguments": {"path": "files/alice/receipt.txt"}}}, headers=alice)
        self.assertEqual(status, 200)
        self.assertIn("TEST_ALICE", res["content"])

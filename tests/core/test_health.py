import time

from django.test import TestCase
from rest_framework.test import APIClient


class CoreHealthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/health/"

    def test_health_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_health_returns_expected_keys(self):
        response = self.client.get(self.url)
        expected_keys = {"status", "timestamp", "uptime_seconds"}
        self.assertTrue(expected_keys.issubset(response.data.keys()))

    def test_health_returns_healthy_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["status"], "ok")

    def test_health_returns_positive_uptime(self):
        response = self.client.get(self.url)
        self.assertGreater(response.data["uptime_seconds"], 0)

    def test_health_returns_valid_timestamp(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.data["timestamp"])

    def test_health_returns_aware_datetime_timestamp(self):
        response = self.client.get(self.url)
        timestamp = response.data["timestamp"]
        self.assertIsNotNone(timestamp.tzinfo)

    def test_health_uptime_increases(self):
        response1 = self.client.get(self.url)
        time.sleep(1)
        response2 = self.client.get(self.url)
        self.assertGreater(
            response2.data["uptime_seconds"], response1.data["uptime_seconds"]
        )

    def test_health_rejects_non_get_methods(self):
        for method in ("post", "put", "patch", "delete"):
            response = getattr(self.client, method)(self.url)
            self.assertEqual(response.status_code, 405)

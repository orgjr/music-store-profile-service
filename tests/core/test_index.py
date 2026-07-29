from django.test import TestCase
from rest_framework.test import APIClient


class CoreIndexTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/"

    def test_index_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_returns_expected_keys(self):
        response = self.client.get(self.url)
        expected_keys = {
            "name",
            "version",
            "description",
            "environment",
            "redoc_url",
            "health_url",
            "api_version",
        }
        self.assertTrue(expected_keys.issubset(response.data.keys()))

    def test_index_returns_service_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["name"], "Music Store Profile Service")

    def test_index_returns_version(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["version"], "0.9.0")

    def test_index_returns_environment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["environment"], "development")

    def test_index_returns_documentation_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["redoc_url"], "/api/v1/redoc/")

    def test_index_returns_health_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["health_url"], "/api/v1/health/")

    def test_index_returns_description(self):
        response = self.client.get(self.url)
        self.assertIn("Profile management microservice", response.data["description"])

    def test_index_rejects_non_get_methods(self):
        for method in ("post", "put", "patch", "delete"):
            response = getattr(self.client, method)(self.url)
            self.assertEqual(response.status_code, 405)

from django.test import TestCase
from rest_framework.test import APIClient

from profiles.customer.models import Customer


VALID_CUSTOMER_DATA = {
    "first_name": "marcelo",
    "last_name": "felisberto",
    "doc": "10212345452",
    "address": "main street",
    "address_number": "234",
    "address_line_2": "apartment 12",
    "neighborhood": "downtown",
    "city": "sao paulo",
    "state": "sp",
    "country": "bra",
}

MINIMAL_CUSTOMER_DATA = {
    "first_name": "ana",
    "last_name": "souza",
    "doc": "99887766554",
    "address": "some street",
    "neighborhood": "east",
    "city": "curitiba",
    "state": "pr",
    "country": "bra",
}


class CustomerEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = "/api/v1/profiles/customer/"

    def _detail_url(self, uuid):
        return f"/api/v1/profiles/customer/{uuid}/"

    def test_create_customer_returns_201(self):
        response = self.client.post(self.list_url, VALID_CUSTOMER_DATA, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_customer_returns_expected_fields(self):
        response = self.client.post(self.list_url, VALID_CUSTOMER_DATA, format="json")
        for key in ("uuid", "first_name", "last_name", "doc", "created_at"):
            self.assertIn(key, response.data)

    def test_list_customers_returns_paginated_response(self):
        Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_list_customers_returns_empty_results(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(len(response.data["results"]), 0)

    def test_retrieve_customer_returns_200(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.get(self._detail_url(customer.uuid))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(customer.uuid))

    def test_retrieve_nonexistent_customer_returns_404(self):
        response = self.client.get(self._detail_url("00000000-0000-0000-0000-000000000000"))
        self.assertEqual(response.status_code, 404)

    def test_update_customer_returns_200(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550")
        response = self.client.put(
            self._detail_url(customer.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "marcelo")

    def test_partial_update_customer_returns_200(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.patch(
            self._detail_url(customer.uuid),
            {"first_name": "mariana"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "mariana")

    def test_delete_customer_returns_204(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.delete(self._detail_url(customer.uuid))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Customer.objects.filter(pk=customer.uuid).exists())

    def test_create_customer_with_duplicate_doc_returns_400(self):
        Customer.objects.create(**VALID_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, first_name="outro", last_name="cliente")
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_empty_body_returns_400(self):
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_missing_required_field_returns_400(self):
        data = dict(VALID_CUSTOMER_DATA)
        del data["first_name"]
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)

    def test_create_customer_with_blank_required_field_returns_400(self):
        data = dict(VALID_CUSTOMER_DATA, first_name="")
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_exceeding_max_length_returns_400(self):
        data = dict(VALID_CUSTOMER_DATA, first_name="a" * 101)
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_wrong_type_coerces_to_string(self):
        data = dict(VALID_CUSTOMER_DATA, first_name=123)
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], "123")

    def test_update_customer_with_missing_required_field_returns_400(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550")
        del data["first_name"]
        response = self.client.put(
            self._detail_url(customer.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_customer_with_exceeding_max_length_returns_400(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550", first_name="a" * 101)
        response = self.client.put(
            self._detail_url(customer.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partial_update_non_existent_field_returns_200(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.patch(
            self._detail_url(customer.uuid),
            {"nonexistent": "value"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_customer_returns_404(self):
        response = self.client.delete(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
        )
        self.assertEqual(response.status_code, 404)

    def test_update_customer_with_blank_required_field_returns_400(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550", first_name="")
        response = self.client.put(
            self._detail_url(customer.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partial_update_customer_with_blank_required_field_returns_400(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        response = self.client.patch(
            self._detail_url(customer.uuid),
            {"first_name": ""},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_invalid_json_returns_400(self):
        response = self.client.post(
            self.list_url,
            "not valid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_long_strings_for_all_fields_returns_400(self):
        data = dict(
            VALID_CUSTOMER_DATA,
            first_name="a" * 101,
            last_name="a" * 101,
            doc="1234567890123",
            address="a" * 251,
            neighborhood="a" * 251,
            city="a" * 251,
            state="spa",
            country="brazil",
        )
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_customer_returns_404(self):
        response = self.client.put(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
            VALID_CUSTOMER_DATA,
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_nonexistent_customer_returns_404(self):
        response = self.client.patch(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
            {"first_name": "test"},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_create_customer_with_only_optional_fields_returns_400(self):
        response = self.client.post(
            self.list_url,
            {"address_number": "100", "address_line_2": "apt 5"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

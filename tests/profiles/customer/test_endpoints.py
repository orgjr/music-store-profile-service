from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now
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
        self.staff_uuid = uuid4()
        self.staff_user = User.objects.create_user(
            username="staff1", password="testpass123", is_staff=True,
        )
        self.staff_user.user_uuid = self.staff_uuid

        self.regular_uuid = uuid4()
        self.regular_user = User.objects.create_user(
            username="regular", password="testpass123", is_staff=False,
        )
        self.regular_user.user_uuid = self.regular_uuid

        self.customers_url = "/api/v1/profiles/customers/"

    def _auth(self, user=None):
        if user is None:
            self.client.credentials()
        else:
            self.client.force_authenticate(user=user)

    def _detail_url(self, uuid):
        return f"/api/v1/profiles/customers/{uuid}/"

    # ── CRUD (create as customer, then retrieve/update/delete own) ──

    def test_create_customer_returns_201(self):
        self._auth(self.regular_user)
        response = self.client.post(self.customers_url, VALID_CUSTOMER_DATA, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_uuid"], str(self.regular_uuid))

    def test_create_customer_returns_expected_fields(self):
        self._auth(self.regular_user)
        response = self.client.post(self.customers_url, VALID_CUSTOMER_DATA, format="json")
        for key in ("uuid", "first_name", "last_name", "doc", "created_at", "user_uuid"):
            self.assertIn(key, response.data)

    def test_retrieve_customer(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        response = self.client.get(self._detail_url(customer.uuid))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(customer.uuid))

    def test_retrieve_nonexistent_customer_returns_404(self):
        self._auth(self.regular_user)
        response = self.client.get(self._detail_url(uuid4()))
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550")
        response = self.client.put(self._detail_url(customer.uuid), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "marcelo")

    def test_partial_update_customer(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        response = self.client.patch(
            self._detail_url(customer.uuid), {"first_name": "mariana"}, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "mariana")

    def test_delete_customer(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.staff_user)
        response = self.client.delete(self._detail_url(customer.uuid))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Customer.objects.filter(pk=customer.uuid).exists())

    def test_delete_customer_requires_staff(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        response = self.client.delete(self._detail_url(customer.uuid))
        self.assertEqual(response.status_code, 403)

    def test_create_customer_with_duplicate_doc_returns_400(self):
        self._auth(self.regular_user)
        Customer.objects.create(user_uuid=self.regular_uuid, **VALID_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, first_name="outro", last_name="cliente")
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_empty_body_returns_400(self):
        self._auth(self.regular_user)
        response = self.client.post(self.customers_url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_missing_required_field_returns_400(self):
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA)
        del data["first_name"]
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)

    def test_create_customer_with_blank_required_field_returns_400(self):
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, first_name="")
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_exceeding_max_length_returns_400(self):
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, first_name="a" * 101)
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_wrong_type_coerces_to_string(self):
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, first_name=123)
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], "123")

    def test_update_customer_with_missing_required_field_returns_400(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550")
        del data["first_name"]
        response = self.client.put(self._detail_url(customer.uuid), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_customer_with_exceeding_max_length_returns_400(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550", first_name="a" * 101)
        response = self.client.put(self._detail_url(customer.uuid), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_partial_update_non_existent_field_returns_200(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        response = self.client.patch(
            self._detail_url(customer.uuid), {"nonexistent": "value"}, format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_customer_returns_404(self):
        self._auth(self.staff_user)
        response = self.client.delete(self._detail_url(uuid4()))
        self.assertEqual(response.status_code, 404)

    def test_update_customer_with_blank_required_field_returns_400(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        data = dict(VALID_CUSTOMER_DATA, doc="19283746550", first_name="")
        response = self.client.put(self._detail_url(customer.uuid), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_partial_update_customer_with_blank_required_field_returns_400(self):
        customer = Customer.objects.create(user_uuid=self.regular_uuid, **MINIMAL_CUSTOMER_DATA)
        self._auth(self.regular_user)
        response = self.client.patch(
            self._detail_url(customer.uuid), {"first_name": ""}, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_invalid_json_returns_400(self):
        self._auth(self.regular_user)
        response = self.client.post(
            self.customers_url, "not valid json", content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_customer_with_long_strings_for_all_fields_returns_400(self):
        self._auth(self.regular_user)
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
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_customer_returns_404(self):
        self._auth(self.regular_user)
        response = self.client.put(
            self._detail_url(uuid4()), VALID_CUSTOMER_DATA, format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_nonexistent_customer_returns_404(self):
        self._auth(self.regular_user)
        response = self.client.patch(
            self._detail_url(uuid4()), {"first_name": "test"}, format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_create_customer_with_only_optional_fields_returns_400(self):
        self._auth(self.regular_user)
        response = self.client.post(
            self.customers_url,
            {"address_number": "100", "address_line_2": "apt 5"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    # ── /customers/ list (requires staff authentication) ──

    def test_list_customers_returns_list(self):
        self._auth(self.staff_user)
        Customer.objects.create(user_uuid=uuid4(), **MINIMAL_CUSTOMER_DATA)
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(response.data["count"], 1)

    def test_list_customers_returns_empty_results(self):
        self._auth(self.staff_user)
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_list_customers_ordered_by_created_at_descending(self):
        self._auth(self.staff_user)
        c1 = Customer.objects.create(user_uuid=uuid4(), **dict(MINIMAL_CUSTOMER_DATA, doc="11111111111"))
        c2 = Customer.objects.create(user_uuid=uuid4(), **dict(MINIMAL_CUSTOMER_DATA, doc="22222222222"))
        c3 = Customer.objects.create(user_uuid=uuid4(), **dict(MINIMAL_CUSTOMER_DATA, doc="33333333333"))

        base = now()
        Customer.objects.filter(pk=c1.pk).update(created_at=base - timedelta(days=3))
        Customer.objects.filter(pk=c2.pk).update(created_at=base - timedelta(days=1))
        Customer.objects.filter(pk=c3.pk).update(created_at=base)

        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, 200)

        docs = [item["doc"] for item in response.data["results"]]
        self.assertEqual(docs, ["33333333333", "22222222222", "11111111111"])

    def test_list_customers_first_page_has_most_recent(self):
        self._auth(self.staff_user)
        base = now()
        c_old = Customer.objects.create(user_uuid=uuid4(), **dict(MINIMAL_CUSTOMER_DATA, doc="11111111111"))
        c_new = Customer.objects.create(user_uuid=uuid4(), **dict(MINIMAL_CUSTOMER_DATA, doc="22222222222"))

        Customer.objects.filter(pk=c_old.pk).update(created_at=base - timedelta(days=10))
        Customer.objects.filter(pk=c_new.pk).update(created_at=base)

        response = self.client.get(self.customers_url)
        self.assertEqual(response.data["results"][0]["doc"], "22222222222")

    # ── Auth / permissions ──

    def test_customer_create_requires_authentication(self):
        response = self.client.post(self.customers_url, VALID_CUSTOMER_DATA, format="json")
        self.assertEqual(response.status_code, 401)

    def test_customer_list_requires_staff(self):
        self._auth(self.regular_user)
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, 403)

from django.test import TestCase
from rest_framework.test import APIClient

from profiles.staff.models import Staff


VALID_STAFF_DATA = {
    "first_name": "claudia",
    "last_name": "mourao",
    "doc": "10125511827",
    "address": "market avenue",
    "address_number": "234",
    "address_line_2": "room 4",
    "neighborhood": "central district",
    "city": "sao paulo",
    "state": "sp",
    "country": "bra",
    "rn": "1925019",
    "role": "customer services",
}

MINIMAL_STAFF_DATA = {
    "first_name": "carlos",
    "last_name": "silva",
    "doc": "55667788990",
    "address": "main avenue",
    "neighborhood": "north",
    "city": "rio de janeiro",
    "state": "rj",
    "country": "bra",
    "rn": "1234567",
    "role": "attendant",
}


class StaffEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = "/api/v1/profiles/staff/"

    def _detail_url(self, uuid):
        return f"/api/v1/profiles/staff/{uuid}/"

    def test_create_staff_returns_201(self):
        response = self.client.post(self.list_url, VALID_STAFF_DATA, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_staff_returns_expected_fields(self):
        response = self.client.post(self.list_url, VALID_STAFF_DATA, format="json")
        for key in ("uuid", "first_name", "last_name", "doc", "rn", "role", "created_at"):
            self.assertIn(key, response.data)

    def test_list_staff_returns_paginated_response(self):
        Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_list_staff_returns_empty_results(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(len(response.data["results"]), 0)

    def test_retrieve_staff_returns_200(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.get(self._detail_url(staff.uuid))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(staff.uuid))

    def test_retrieve_nonexistent_staff_returns_404(self):
        response = self.client.get(self._detail_url("00000000-0000-0000-0000-000000000000"))
        self.assertEqual(response.status_code, 404)

    def test_update_staff_returns_200(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, doc="19283746550")
        response = self.client.put(
            self._detail_url(staff.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "claudia")

    def test_partial_update_staff_returns_200(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.patch(
            self._detail_url(staff.uuid),
            {"role": "store manager"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["role"], "store manager")

    def test_delete_staff_returns_204(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.delete(self._detail_url(staff.uuid))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Staff.objects.filter(pk=staff.uuid).exists())

    def test_create_staff_with_duplicate_doc_returns_400(self):
        Staff.objects.create(**VALID_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, first_name="outro", last_name="funcionario")
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_empty_body_returns_400(self):
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_missing_required_field_returns_400(self):
        data = dict(VALID_STAFF_DATA)
        del data["rn"]
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("rn", response.data)

    def test_create_staff_with_blank_rn_returns_400(self):
        data = dict(VALID_STAFF_DATA, rn="")
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_exceeding_max_length_returns_400(self):
        data = dict(VALID_STAFF_DATA, role="a" * 51)
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_rn_exceeding_max_length_returns_400(self):
        data = dict(VALID_STAFF_DATA, rn="12345678")
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_staff_with_missing_required_field_returns_400(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, doc="19283746550")
        del data["rn"]
        response = self.client.put(
            self._detail_url(staff.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_nonexistent_staff_returns_404(self):
        response = self.client.delete(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
        )
        self.assertEqual(response.status_code, 404)

    def test_update_staff_with_blank_required_field_returns_400(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, doc="19283746550", first_name="")
        response = self.client.put(
            self._detail_url(staff.uuid), data, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partial_update_staff_with_blank_required_field_returns_400(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.patch(
            self._detail_url(staff.uuid),
            {"first_name": ""},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partial_update_staff_non_existent_field_returns_200(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        response = self.client.patch(
            self._detail_url(staff.uuid),
            {"nonexistent": "value"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_staff_with_invalid_json_returns_400(self):
        response = self.client.post(
            self.list_url,
            "not valid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_staff_returns_404(self):
        response = self.client.put(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
            VALID_STAFF_DATA,
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_nonexistent_staff_returns_404(self):
        response = self.client.patch(
            self._detail_url("00000000-0000-0000-0000-000000000000"),
            {"role": "manager"},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_create_staff_with_only_optional_fields_returns_400(self):
        response = self.client.post(
            self.list_url,
            {"address_number": "100", "address_line_2": "room 1"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

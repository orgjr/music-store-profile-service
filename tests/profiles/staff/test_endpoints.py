from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now
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
    "role": "attendant",
}


class StaffEndpointTestCase(TestCase):
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

        self.staffs_url = "/api/v1/profiles/staffs/"

    def _auth(self, user=None):
        if user is None:
            self.client.credentials()
        else:
            self.client.force_authenticate(user=user)

    def _detail_url(self, uuid):
        return f"/api/v1/profiles/staffs/{uuid}/"

    # ── CRUD (create as staff, then retrieve/update/delete own) ──

    def test_create_staff_returns_201(self):
        self._auth(self.staff_user)
        response = self.client.post(self.staffs_url, VALID_STAFF_DATA, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user_uuid"], str(self.staff_uuid))

    def test_create_staff_returns_expected_fields(self):
        self._auth(self.staff_user)
        response = self.client.post(self.staffs_url, VALID_STAFF_DATA, format="json")
        for key in ("uuid", "first_name", "last_name", "doc", "staff_id", "role", "created_at", "user_uuid"):
            self.assertIn(key, response.data)

    def test_create_staff_returns_staff_id(self):
        self._auth(self.staff_user)
        response = self.client.post(self.staffs_url, VALID_STAFF_DATA, format="json")
        self.assertIsInstance(response.data["staff_id"], int)
        self.assertGreaterEqual(response.data["staff_id"], 1000000)

    def test_retrieve_staff(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        response = self.client.get(self._detail_url(staff.uuid))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(staff.uuid))

    def test_retrieve_nonexistent_staff_returns_404(self):
        self._auth(self.staff_user)
        response = self.client.get(self._detail_url(uuid4()))
        self.assertEqual(response.status_code, 404)

    def test_update_staff(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        data = dict(VALID_STAFF_DATA, doc="19283746550")
        response = self.client.put(self._detail_url(staff.uuid), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "claudia")

    def test_partial_update_staff(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        response = self.client.patch(
            self._detail_url(staff.uuid), {"role": "store manager"}, format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["role"], "store manager")

    def test_delete_staff(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        response = self.client.delete(self._detail_url(staff.uuid))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Staff.objects.filter(pk=staff.uuid).exists())

    def test_create_staff_with_duplicate_doc_returns_400(self):
        self._auth(self.staff_user)
        Staff.objects.create(user_uuid=self.staff_uuid, **VALID_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, first_name="outro", last_name="funcionario")
        response = self.client.post(self.staffs_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_empty_body_returns_400(self):
        self._auth(self.staff_user)
        response = self.client.post(self.staffs_url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_staff_with_missing_required_field_returns_400(self):
        self._auth(self.staff_user)
        data = dict(VALID_STAFF_DATA)
        del data["role"]
        response = self.client.post(self.staffs_url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("role", response.data)

    def test_create_staff_with_exceeding_max_length_returns_400(self):
        self._auth(self.staff_user)
        data = dict(VALID_STAFF_DATA, role="a" * 51)
        response = self.client.post(self.staffs_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_staff_with_missing_required_field_returns_400(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        data = dict(VALID_STAFF_DATA, doc="19283746550")
        del data["role"]
        response = self.client.put(self._detail_url(staff.uuid), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete_nonexistent_staff_returns_404(self):
        self._auth(self.staff_user)
        response = self.client.delete(self._detail_url(uuid4()))
        self.assertEqual(response.status_code, 404)

    def test_update_staff_with_blank_required_field_returns_400(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        data = dict(VALID_STAFF_DATA, doc="19283746550", first_name="")
        response = self.client.put(self._detail_url(staff.uuid), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_partial_update_staff_with_blank_required_field_returns_400(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        response = self.client.patch(
            self._detail_url(staff.uuid), {"first_name": ""}, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partial_update_staff_non_existent_field_returns_200(self):
        staff = Staff.objects.create(user_uuid=self.staff_uuid, **MINIMAL_STAFF_DATA)
        self._auth(self.staff_user)
        response = self.client.patch(
            self._detail_url(staff.uuid), {"nonexistent": "value"}, format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_staff_with_invalid_json_returns_400(self):
        self._auth(self.staff_user)
        response = self.client.post(
            self.staffs_url, "not valid json", content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_staff_returns_404(self):
        self._auth(self.staff_user)
        response = self.client.put(
            self._detail_url(uuid4()), VALID_STAFF_DATA, format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_nonexistent_staff_returns_404(self):
        self._auth(self.staff_user)
        response = self.client.patch(
            self._detail_url(uuid4()), {"role": "manager"}, format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_create_staff_with_only_optional_fields_returns_400(self):
        self._auth(self.staff_user)
        response = self.client.post(
            self.staffs_url,
            {"address_number": "100", "address_line_2": "room 1"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    # ── /staffs/ list (requires staff authentication) ──

    def test_list_staff_returns_list(self):
        self._auth(self.staff_user)
        Staff.objects.create(user_uuid=uuid4(), **MINIMAL_STAFF_DATA)
        response = self.client.get(self.staffs_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(response.data["count"], 1)

    def test_list_staff_returns_empty_results(self):
        self._auth(self.staff_user)
        response = self.client.get(self.staffs_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_list_staff_ordered_by_created_at_descending(self):
        self._auth(self.staff_user)
        s1 = Staff.objects.create(user_uuid=uuid4(), **dict(MINIMAL_STAFF_DATA, doc="11111111111"))
        s2 = Staff.objects.create(user_uuid=uuid4(), **dict(MINIMAL_STAFF_DATA, doc="22222222222"))
        s3 = Staff.objects.create(user_uuid=uuid4(), **dict(MINIMAL_STAFF_DATA, doc="33333333333"))

        base = now()
        Staff.objects.filter(pk=s1.pk).update(created_at=base - timedelta(days=3))
        Staff.objects.filter(pk=s2.pk).update(created_at=base - timedelta(days=1))
        Staff.objects.filter(pk=s3.pk).update(created_at=base)

        response = self.client.get(self.staffs_url)
        self.assertEqual(response.status_code, 200)

        docs = [item["doc"] for item in response.data["results"]]
        self.assertEqual(docs, ["33333333333", "22222222222", "11111111111"])

    def test_list_staff_first_page_has_most_recent(self):
        self._auth(self.staff_user)
        base = now()
        s_old = Staff.objects.create(user_uuid=uuid4(), **dict(MINIMAL_STAFF_DATA, doc="11111111111"))
        s_new = Staff.objects.create(user_uuid=uuid4(), **dict(MINIMAL_STAFF_DATA, doc="22222222222"))

        Staff.objects.filter(pk=s_old.pk).update(created_at=base - timedelta(days=10))
        Staff.objects.filter(pk=s_new.pk).update(created_at=base)

        response = self.client.get(self.staffs_url)
        self.assertEqual(response.data["results"][0]["doc"], "22222222222")

    # ── Auth / permissions ──

    def test_staff_create_requires_authentication(self):
        response = self.client.post(self.staffs_url, VALID_STAFF_DATA, format="json")
        self.assertEqual(response.status_code, 401)

    def test_staff_list_requires_staff(self):
        self._auth(self.regular_user)
        response = self.client.get(self.staffs_url)
        self.assertEqual(response.status_code, 403)

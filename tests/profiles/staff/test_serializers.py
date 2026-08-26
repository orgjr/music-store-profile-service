from django.test import TestCase

from profiles.staff.models import Staff
from profiles.staff.serializers import StaffSerializer


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


class StaffSerializerTestCase(TestCase):
    def test_serializer_validates_valid_data(self):
        serializer = StaffSerializer(data=VALID_STAFF_DATA)
        self.assertTrue(serializer.is_valid())

    def test_serializer_detects_missing_required_field(self):
        data = dict(VALID_STAFF_DATA)
        del data["role"]
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("role", serializer.errors)

    def test_serializer_rejects_blank_required_field(self):
        data = dict(VALID_STAFF_DATA, role="")
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_null_required_field(self):
        data = dict(VALID_STAFF_DATA, role=None)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_role_exceeding_max_length(self):
        data = dict(VALID_STAFF_DATA, role="a" * 51)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_accepts_null_for_optional_fields(self):
        data = dict(VALID_STAFF_DATA, address_number=None, address_line_2=None)
        serializer = StaffSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_detects_multiple_missing_fields(self):
        data = {}
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        for field in ("first_name", "last_name", "doc", "address",
                       "neighborhood", "city", "state", "country", "role"):
            self.assertIn(field, serializer.errors)

    def test_serializer_outputs_expected_fields(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        serializer = StaffSerializer(instance=staff)
        expected_fields = {
            "uuid", "first_name", "last_name", "doc",
            "address", "address_number", "address_line_2",
            "neighborhood", "city", "state", "country",
            "created_at", "staff_id", "role",
        }
        self.assertEqual(serializer.data.keys(), expected_fields)

    def test_serializer_staff_id_is_read_only(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        serializer = StaffSerializer(instance=staff)
        self.assertIn("staff_id", serializer.data)
        self.assertIsInstance(serializer.data["staff_id"], int)

    def test_serializer_detects_duplicate_doc(self):
        Staff.objects.create(**VALID_STAFF_DATA)
        data = dict(VALID_STAFF_DATA, first_name="outro", last_name="staff", doc=VALID_STAFF_DATA["doc"])
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("doc", serializer.errors)

    def test_serializer_update_accepts_same_doc_for_same_instance(self):
        staff = Staff.objects.create(**VALID_STAFF_DATA)
        serializer = StaffSerializer(instance=staff, data=VALID_STAFF_DATA)
        self.assertTrue(serializer.is_valid())

    def test_serializer_rejects_blank_last_name(self):
        data = dict(VALID_STAFF_DATA, last_name="")
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_city(self):
        data = dict(VALID_STAFF_DATA, city="")
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_state(self):
        data = dict(VALID_STAFF_DATA, state="")
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_last_name_exceeding_max_length(self):
        data = dict(VALID_STAFF_DATA, last_name="a" * 101)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_address_exceeding_max_length(self):
        data = dict(VALID_STAFF_DATA, address="a" * 251)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_city_exceeding_max_length(self):
        data = dict(VALID_STAFF_DATA, city="a" * 251)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_neighborhood_exceeding_max_length(self):
        data = dict(VALID_STAFF_DATA, neighborhood="a" * 251)
        serializer = StaffSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_accepts_empty_optional_fields(self):
        data = dict(
            VALID_STAFF_DATA,
            address_number="",
            address_line_2="",
            doc="99887766553",
        )
        serializer = StaffSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_error_messages_are_strings(self):
        serializer = StaffSerializer(data={})
        serializer.is_valid()
        for field_errors in serializer.errors.values():
            for error in field_errors:
                self.assertIsInstance(error, str)

from uuid import uuid4

from django.test import TestCase
from django.utils import timezone

from profiles.staff.models import Staff


VALID_STAFF_DATA = {
    "user_uuid": uuid4(),
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
    "user_uuid": uuid4(),
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


class StaffModelTestCase(TestCase):
    def test_create_staff(self):
        staff = Staff.objects.create(**VALID_STAFF_DATA)
        self.assertIsNotNone(staff.pk)
        self.assertEqual(staff.first_name, "claudia")
        self.assertIsNotNone(staff.staff_id)
        self.assertEqual(staff.role, "customer services")

    def test_create_staff_requires_unique_user_uuid(self):
        user_uuid = uuid4()
        Staff.objects.create(**dict(VALID_STAFF_DATA, user_uuid=user_uuid, doc="10125511828"))

        with self.assertRaises(Exception) as ctx:
            Staff.objects.create(**dict(VALID_STAFF_DATA, user_uuid=user_uuid, doc="10125511829"))

        exception_text = str(ctx.exception)
        self.assertTrue("already exists" in exception_text or "user_uuid" in exception_text or "UNIQUE" in exception_text)

    def test_create_staff_without_optional_fields(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertIsNone(staff.address_number)
        self.assertIsNone(staff.address_line_2)

    def test_staff_str_returns_full_name(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertEqual(str(staff), "Carlos Silva")

    def test_create_staff_with_invalid_role_chars_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="attendant@", doc="99988877766")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_special_chars_in_role_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="manager<>", doc="88877766655")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_parentheses_in_role_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="attendant()", doc="66655544433")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_sanitizes_whitespace_in_profile_fields(self):
        staff = Staff.objects.create(
            user_uuid=uuid4(),
            first_name="  claudia  ",
            last_name="  mourao  ",
            doc="99887766551",
            address="  market avenue  ",
            neighborhood="  central  ",
            city="  sao paulo  ",
            state="sp",
            country="bra",
            role="customer services",
        )
        self.assertEqual(staff.first_name, "claudia")

    def test_create_staff_preserves_input_case(self):
        staff = Staff.objects.create(
            user_uuid=uuid4(),
            first_name="CLAUDIA",
            last_name="MOURAO",
            doc="99887766552",
            address="MARKET AVENUE",
            neighborhood="CENTRAL",
            city="SAO PAULO",
            state="sp",
            country="bra",
            role="customer services",
        )
        self.assertEqual(staff.first_name, "CLAUDIA")

    def test_create_staff_with_numeric_role_is_valid(self):
        staff = Staff.objects.create(**dict(VALID_STAFF_DATA, role="12345", doc="88776655441"))
        self.assertEqual(staff.role, "12345")

    def test_updated_at_is_set_on_create(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertIsNotNone(staff.updated_at)
        self.assertIsInstance(staff.updated_at, type(timezone.now()))

    def test_updated_at_changes_on_update(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        original_updated = staff.updated_at

        staff.first_name = "carlos alberto"
        staff.save()
        staff.refresh_from_db()

        self.assertGreater(staff.updated_at, original_updated)
        self.assertEqual(staff.first_name, "carlos alberto")

    def test_updated_at_is_timezone_aware(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertTrue(timezone.is_aware(staff.updated_at))

from django.test import TestCase

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


class StaffModelTestCase(TestCase):
    def test_create_staff(self):
        staff = Staff.objects.create(**VALID_STAFF_DATA)
        self.assertIsNotNone(staff.pk)
        self.assertEqual(staff.first_name, "claudia")
        self.assertEqual(staff.rn, "1925019")
        self.assertEqual(staff.role, "customer services")

    def test_create_staff_without_optional_fields(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertIsNone(staff.address_number)
        self.assertIsNone(staff.address_line_2)

    def test_staff_str_returns_full_name(self):
        staff = Staff.objects.create(**MINIMAL_STAFF_DATA)
        self.assertEqual(str(staff), "Carlos Silva")

    def test_create_staff_with_non_numeric_rn_raises_error(self):
        data = dict(VALID_STAFF_DATA, rn="abc1234", doc="99988877766")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_non_numeric_rn_special_chars_raises_error(self):
        data = dict(VALID_STAFF_DATA, rn="123-456", doc="88877766655")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_empty_rn_raises_error(self):
        data = dict(VALID_STAFF_DATA, rn="", doc="77766655544")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_spaces_in_rn_raises_error(self):
        data = dict(VALID_STAFF_DATA, rn="123 456", doc="66655544433")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_invalid_role_chars_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="attendant@", doc="99988877766")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_special_chars_in_role_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="manager<>", doc="88877766655")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_with_empty_role_is_stored_as_empty(self):
        data = dict(VALID_STAFF_DATA, role="", doc="77766655544")
        staff = Staff.objects.create(**data)
        self.assertEqual(staff.role, "")

    def test_create_staff_with_parentheses_in_role_raises_error(self):
        data = dict(VALID_STAFF_DATA, role="attendant()", doc="66655544433")
        with self.assertRaises(ValueError):
            Staff.objects.create(**data)

    def test_create_staff_sanitizes_whitespace_in_profile_fields(self):
        staff = Staff.objects.create(
            first_name="  claudia  ",
            last_name="  mourao  ",
            doc="99887766551",
            address="  market avenue  ",
            neighborhood="  central  ",
            city="  sao paulo  ",
            state="sp",
            country="bra",
            rn="1925019",
            role="customer services",
        )
        self.assertEqual(staff.first_name, "claudia")

    def test_create_staff_lowercases_profile_fields(self):
        staff = Staff.objects.create(
            first_name="CLAUDIA",
            last_name="MOURAO",
            doc="99887766552",
            address="MARKET AVENUE",
            neighborhood="CENTRAL",
            city="SAO PAULO",
            state="sp",
            country="bra",
            rn="1925019",
            role="customer services",
        )
        self.assertEqual(staff.first_name, "claudia")

    def test_create_staff_with_numeric_role_is_valid(self):
        staff = Staff.objects.create(**dict(VALID_STAFF_DATA, role="12345", doc="88776655441"))
        self.assertEqual(staff.role, "12345")

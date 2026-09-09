from uuid import uuid4

from django.test import TestCase

from profiles.staff.models import Staff

STAFF_BASE_DATA = {
    "first_name": "claudia",
    "last_name": "mourao",
    "address": "market avenue",
    "address_number": "234",
    "address_line_2": "room 4",
    "neighborhood": "central district",
    "city": "sao paulo",
    "state": "sp",
    "country": "bra",
    "role": "customer services",
    "user_uuid": uuid4(),
}
from django.core.exceptions import ValidationError
from django.db import transaction


def _make_staff(**overrides):
    import random

    data = dict(STAFF_BASE_DATA, **overrides)
    data.setdefault("doc", f"{random.randint(10**10, 10**11 - 1)}")
    data["user_uuid"] = uuid4()
    return data


class StaffIdAutoGenerationTestCase(TestCase):
    def test_staff_id_is_set_automatically(self):
        staff = Staff.objects.create(**_make_staff())
        self.assertIsNotNone(staff.staff_id)

    def test_staff_id_is_integer(self):
        staff = Staff.objects.create(**_make_staff())
        self.assertIsInstance(staff.staff_id, int)

    def test_staff_id_is_within_valid_range(self):
        staff = Staff.objects.create(**_make_staff())
        self.assertGreaterEqual(staff.staff_id, 1000000)
        self.assertLessEqual(staff.staff_id, 9999999)

    def test_first_staff_id_starts_at_1000001(self):
        staff = Staff.objects.create(**_make_staff())
        self.assertEqual(staff.staff_id, 1000001)

    def test_multiple_staff_receive_sequential_ids(self):
        s1 = Staff.objects.create(**_make_staff())
        s2 = Staff.objects.create(**_make_staff())
        s3 = Staff.objects.create(**_make_staff())
        self.assertEqual(s1.staff_id, 1000001)
        self.assertEqual(s2.staff_id, 1000002)
        self.assertEqual(s3.staff_id, 1000003)

    def test_all_staff_ids_are_unique(self):
        staffs = [Staff.objects.create(**_make_staff()) for _ in range(10)]
        ids = [s.staff_id for s in staffs]
        self.assertEqual(len(ids), len(set(ids)))

    def test_staff_id_is_persisted_in_database(self):
        staff = Staff.objects.create(**_make_staff())
        refreshed = Staff.objects.get(pk=staff.pk)
        self.assertEqual(refreshed.staff_id, staff.staff_id)

    def test_staff_id_survives_update(self):
        staff = Staff.objects.create(**_make_staff())
        original_id = staff.staff_id
        staff.first_name = "Updated"
        staff.save()
        staff.refresh_from_db()
        self.assertEqual(staff.staff_id, original_id)


class StaffIdDuplicateHandlingTestCase(TestCase):
    def test_creating_with_duplicate_staff_id_auto_generates_new_one(self):
        first = Staff.objects.create(**_make_staff())
        duplicate_id = first.staff_id

        data = _make_staff()
        data["staff_id"] = duplicate_id
        second = Staff.objects.create(**data)
        self.assertNotEqual(second.staff_id, duplicate_id)
        self.assertEqual(second.staff_id, first.staff_id + 1)

    def test_creating_with_explicit_valid_staff_id_succeeds(self):
        staff = Staff.objects.create(**_make_staff(staff_id=5000000))
        self.assertEqual(staff.staff_id, 5000000)

    def test_generate_staff_id_uses_max_existing_plus_one(self):
        Staff.objects.create(**_make_staff(staff_id=5000000))
        Staff.objects.create(**_make_staff(staff_id=5000005))
        new_staff = Staff.objects.create(**_make_staff())
        self.assertEqual(new_staff.staff_id, 5000006)

    def test_generate_staff_id_after_deletion_fills_gap_above_max(self):
        s1 = Staff.objects.create(**_make_staff(staff_id=1000001))
        s2 = Staff.objects.create(**_make_staff(staff_id=1000002))
        s1.delete()
        new_staff = Staff.objects.create(**_make_staff())
        self.assertEqual(new_staff.staff_id, 1000003)
        s2.delete()
        new_staff = Staff.objects.create(**_make_staff())
        self.assertEqual(new_staff.staff_id, 1000004)

    def test_generate_staff_id_handles_high_values(self):
        Staff.objects.create(**_make_staff(staff_id=9999997))
        s2 = Staff.objects.create(**_make_staff())
        self.assertEqual(s2.staff_id, 9999998)
        s3 = Staff.objects.create(**_make_staff())
        self.assertEqual(s3.staff_id, 9999999)


class StaffIdValidatorBoundaryTestCase(TestCase):
    def test_accepts_minimum_valid_staff_id(self):
        staff = Staff.objects.create(**_make_staff(staff_id=1000000))
        self.assertEqual(staff.staff_id, 1000000)

    def test_accepts_maximum_valid_staff_id(self):
        staff = Staff.objects.create(**_make_staff(staff_id=9999999))
        self.assertEqual(staff.staff_id, 9999999)

    def test_rejects_staff_id_below_minimum(self):
        with self.assertRaises(ValidationError), transaction.atomic():
            Staff.objects.create(**_make_staff(staff_id=999999))

    def test_rejects_staff_id_above_maximum(self):
        with self.assertRaises(ValidationError), transaction.atomic():
            Staff.objects.create(**_make_staff(staff_id=10000000))

    def test_staff_id_field_is_unique_after_auto_generation(self):
        Staff.objects.create(**_make_staff(staff_id=2000000))
        second = Staff.objects.create(**_make_staff(staff_id=2000000))
        self.assertNotEqual(second.staff_id, 2000000)
        self.assertEqual(Staff.objects.filter(staff_id=2000000).count(), 1)

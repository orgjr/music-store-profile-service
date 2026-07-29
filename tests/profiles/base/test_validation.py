from django.core.exceptions import ValidationError
from django.test import TestCase

from profiles.customer.models import Customer


class ProfileValidationTestCase(TestCase):
    def _make_data(self, **overrides):
        data = {
            "first_name": "john",
            "last_name": "doe",
            "doc": "12345678901",
            "address": "main street",
            "neighborhood": "center",
            "city": "sao paulo",
            "state": "sp",
            "country": "bra",
        }
        data.update(overrides)
        return data

    def test_state_exceeds_max_length_raises_validation_error(self):
        customer = Customer(**self._make_data(doc="11111111111", state="spa"))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_country_exceeds_max_length_raises_validation_error(self):
        customer = Customer(**self._make_data(doc="22222222222", country="brazil"))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_doc_exceeds_max_length_raises_validation_error(self):
        customer = Customer(**self._make_data(doc="1234567890123"))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_first_name_exceeds_max_length_raises_validation_error(self):
        customer = Customer(
            **self._make_data(doc="33333333333", first_name="a" * 101)
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_state_blank_is_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="44444444444", state=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_country_blank_is_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="55555555555", country=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_address_blank_is_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="66666666666", address=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_create_without_address_number_is_null(self):
        data = self._make_data(doc="77777777777")
        data.pop("address_number", None)
        customer = Customer.objects.create(**data)
        self.assertIsNone(customer.address_number)

    def test_create_without_address_line_2_is_null(self):
        data = self._make_data(doc="88888888888")
        data.pop("address_line_2", None)
        customer = Customer.objects.create(**data)
        self.assertIsNone(customer.address_line_2)

    def test_duplicate_doc_raises_integrity_error(self):
        Customer.objects.create(**self._make_data())
        with self.assertRaises(Exception) as ctx:
            Customer.objects.create(
                **self._make_data(
                    first_name="other", last_name="person",
                    doc="12345678901",
                )
            )
        self.assertIn("UNIQUE", str(ctx.exception))

    def test_full_clean_rejects_missing_required_field(self):
        data = self._make_data(doc="99999999999")
        del data["address"]
        customer = Customer(**data)
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_address_number_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="10101010101", address_number="12345678901"))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_last_name_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="11121314151", last_name="a" * 101))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_neighborhood_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="12131415161", neighborhood="a" * 251))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_city_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="13141516171", city="a" * 251))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_address_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="14151617181", address="a" * 251))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_address_line_2_exceeds_max_length(self):
        customer = Customer(**self._make_data(doc="15161718191", address_line_2="a" * 251))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_blank_first_name_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="16171819201", first_name=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_blank_last_name_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="17181920212", last_name=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_blank_neighborhood_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="18192021223", neighborhood=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_blank_city_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc="19202122234", city=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_blank_doc_rejected_by_full_clean(self):
        customer = Customer(**self._make_data(doc=""))
        with self.assertRaises(ValidationError):
            customer.full_clean()

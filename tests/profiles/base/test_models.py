from uuid import uuid4

from django.test import TestCase

from profiles.customer.models import Customer


class ProfileModelTestCase(TestCase):
    def _make_customer(self, **overrides):
        fields = {
            "first_name": "john",
            "last_name": "doe",
            "doc": "12345678901",
            "address": "main street",
            "neighborhood": "center",
            "city": "sao paulo",
            "state": "sp",
            "country": "bra",
        }
        fields.update(overrides)
        return fields

    def test_get_full_name_returns_title_cased_full_name(self):
        customer = Customer.objects.create(**self._make_customer())
        self.assertEqual(customer.get_full_name(), "John Doe")

    def test_save_generates_uuid_when_not_set(self):
        customer = Customer(**self._make_customer(doc="10987654321"))
        customer.save()
        self.assertIsNotNone(customer.uuid)

    def test_save_preserves_existing_uuid(self):
        existing_uuid = uuid4()
        customer = Customer(
            uuid=existing_uuid,
            **self._make_customer(doc="11122233344"),
        )
        customer.save()
        self.assertEqual(customer.uuid, existing_uuid)

    def test_created_at_is_auto_set(self):
        customer = Customer.objects.create(**self._make_customer(doc="55566677788"))
        self.assertIsNotNone(customer.created_at)

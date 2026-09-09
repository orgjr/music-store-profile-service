from uuid import uuid4

from django.test import TestCase

from profiles.customer.models import Customer
from profiles.customer.serializers import CustomerSerializer


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
    "user_uuid": uuid4(),
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
    "user_uuid": uuid4(),
}


class CustomerSerializerTestCase(TestCase):
    def test_serializer_validates_valid_data(self):
        serializer = CustomerSerializer(data=VALID_CUSTOMER_DATA)
        self.assertTrue(serializer.is_valid())

    def test_serializer_detects_missing_required_field(self):
        data = dict(VALID_CUSTOMER_DATA)
        del data["first_name"]
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_serializer_detects_blank_required_field(self):
        data = dict(VALID_CUSTOMER_DATA, first_name="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_null_required_field(self):
        data = dict(VALID_CUSTOMER_DATA, first_name=None)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_coerces_int_to_string(self):
        data = dict(VALID_CUSTOMER_DATA, first_name=123)
        serializer = CustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["first_name"], "123")

    def test_serializer_rejects_whitespace_only_required_field(self):
        data = dict(VALID_CUSTOMER_DATA, first_name="   ")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_accepts_optional_fields_as_null(self):
        data = dict(VALID_CUSTOMER_DATA, address_number=None, address_line_2=None)
        serializer = CustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_rejects_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, first_name="a" * 101)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_state_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, state="spa")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_country_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, country="brazil")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_doc_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, doc="1234567890123")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_ignores_extra_unknown_field(self):
        data = dict(VALID_CUSTOMER_DATA, unknown_field="something")
        serializer = CustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("unknown_field", serializer.validated_data)

    def test_serializer_outputs_expected_fields(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        serializer = CustomerSerializer(instance=customer)
        expected_fields = {
            "uuid", "user_uuid", "first_name", "last_name", "doc",
            "address", "address_number", "address_line_2",
            "neighborhood", "city", "state", "country",
            "created_at", "updated_at",
        }
        self.assertEqual(serializer.data.keys(), expected_fields)

    def test_serializer_detects_duplicate_doc(self):
        Customer.objects.create(**VALID_CUSTOMER_DATA)
        data = dict(VALID_CUSTOMER_DATA, first_name="outro", last_name="nome")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("doc", serializer.errors)

    def test_serializer_update_accepts_same_doc_for_same_instance(self):
        customer = Customer.objects.create(**VALID_CUSTOMER_DATA)
        serializer = CustomerSerializer(instance=customer, data=VALID_CUSTOMER_DATA)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validates_multiple_missing_fields(self):
        data = {}
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        for field in ("first_name", "last_name", "doc", "address", "neighborhood", "city", "state", "country"):
            self.assertIn(field, serializer.errors)

    def test_serializer_rejects_blank_last_name(self):
        data = dict(VALID_CUSTOMER_DATA, last_name="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_neighborhood(self):
        data = dict(VALID_CUSTOMER_DATA, neighborhood="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_city(self):
        data = dict(VALID_CUSTOMER_DATA, city="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_state(self):
        data = dict(VALID_CUSTOMER_DATA, state="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_country(self):
        data = dict(VALID_CUSTOMER_DATA, country="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_address(self):
        data = dict(VALID_CUSTOMER_DATA, address="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_blank_doc(self):
        data = dict(VALID_CUSTOMER_DATA, doc="")
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_last_name_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, last_name="a" * 101)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_address_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, address="a" * 251)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_neighborhood_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, neighborhood="a" * 251)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_rejects_city_exceeding_max_length(self):
        data = dict(VALID_CUSTOMER_DATA, city="a" * 251)
        serializer = CustomerSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_accepts_empty_optional_fields(self):
        data = dict(
            VALID_CUSTOMER_DATA,
            address_number="",
            address_line_2="",
            doc="99887766555",
        )
        serializer = CustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_error_messages_are_strings(self):
        serializer = CustomerSerializer(data={})
        serializer.is_valid()
        for field_errors in serializer.errors.values():
            for error in field_errors:
                self.assertIsInstance(error, str)

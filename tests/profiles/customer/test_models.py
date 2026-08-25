from django.test import TestCase

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


class CustomerModelTestCase(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create(**VALID_CUSTOMER_DATA)
        self.assertIsNotNone(customer.pk)
        self.assertEqual(customer.first_name, "marcelo")
        self.assertEqual(customer.doc, "10212345452")

    def test_create_customer_without_optional_fields(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        self.assertIsNone(customer.address_number)
        self.assertIsNone(customer.address_line_2)

    def test_customer_str_returns_full_name(self):
        customer = Customer.objects.create(**MINIMAL_CUSTOMER_DATA)
        self.assertEqual(str(customer), "Ana Souza")

    def test_create_customer_with_invalid_chars_raises_error(self):
        invalid_data = dict(VALID_CUSTOMER_DATA, first_name="marcelo@", doc="99988877766")
        with self.assertRaises(ValueError):
            Customer.objects.create(**invalid_data)

    def test_create_customer_sanitizes_whitespace(self):
        customer = Customer.objects.create(
            first_name="  marcelo  ",
            last_name="  felisberto  ",
            doc="11223344556",
            address="  main street  ",
            neighborhood="  downtown  ",
            city="  sao paulo  ",
            state="sp",
            country="bra",
        )
        self.assertEqual(customer.first_name, "marcelo")

    def test_create_customer_preserves_input_case(self):
        customer = Customer.objects.create(
            first_name="MARCELO",
            last_name="FELISBERTO",
            doc="88776655441",
            address="MAIN STREET",
            neighborhood="DOWNTOWN",
            city="SAO PAULO",
            state="sp",
            country="bra",
        )
        self.assertEqual(customer.first_name, "MARCELO")
        self.assertEqual(customer.last_name, "FELISBERTO")

    def test_create_customer_with_special_chars_in_last_name_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, last_name="silva@#", doc="88776655441")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_address_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, address="main st$$", doc="77665544332")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_city_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, city="sao paulo!", doc="66554433221")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_neighborhood_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, neighborhood="centro<>", doc="55443322110")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_state_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, state="s@p", doc="44332211001")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_country_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, country="br#", doc="33221100012")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_doc_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, doc="123@5678901")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_address_number_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, address_number="12a!", doc="22334455660")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_special_chars_in_address_line_2_raises_error(self):
        data = dict(VALID_CUSTOMER_DATA, address_line_2="apt#1", doc="11223344557")
        with self.assertRaises(ValueError):
            Customer.objects.create(**data)

    def test_create_customer_with_valid_alphanumeric_with_accents(self):
        customer = Customer.objects.create(
            first_name="josé",
            last_name="da silva",
            doc="99887766552",
            address="rua são joão",
            neighborhood="centro",
            city="são paulo",
            state="sp",
            country="bra",
        )
        self.assertEqual(customer.first_name, "josé")

    def test_create_customer_with_unicode_is_valid(self):
        customer = Customer.objects.create(
            first_name="αβγ",
            last_name="δέ",
            doc="99887766553",
            address="οδός",
            neighborhood="κέντρο",
            city="αθήνα",
            state="at",
            country="grc",
        )
        self.assertEqual(customer.first_name, "αβγ")

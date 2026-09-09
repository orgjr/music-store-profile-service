from uuid import UUID

from profiles.validators import validate_alphanumeric, validate_doc


class ProfileValidationService:
    @staticmethod
    def validate(
        user_uuid,
        first_name,
        last_name,
        doc,
        address,
        neighborhood,
        city,
        state,
        country,
        address_number=None,
        address_line_2=None,
    ):

        user_uuid = UUID(str(user_uuid))
        first_name = validate_alphanumeric("first_name", first_name)
        last_name = validate_alphanumeric("last_name", last_name)
        doc = validate_doc(doc)
        address = validate_alphanumeric("address", address)
        if address_number is not None:
            address_number = validate_alphanumeric("address_number", address_number)
        if address_line_2 is not None:
            address_line_2 = validate_alphanumeric("address_line_2", address_line_2)
        neighborhood = validate_alphanumeric("neighborhood", neighborhood)
        city = validate_alphanumeric("city", city)
        state = validate_alphanumeric("state", state).upper()
        country = validate_alphanumeric("country", country).upper()

        return {
            "user_uuid": user_uuid,
            "first_name": first_name,
            "last_name": last_name,
            "doc": doc,
            "address": address,
            "address_number": address_number,
            "address_line_2": address_line_2,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
            "country": country,
        }

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
)

customer_request_example = {
    "first_name": "marcelo",
    "last_name": "felisberto",
    "doc": "10212345452",
    "address": "main street",
    "address_number": "234",
    "address_line_2": "apartment 12",
    "neighborhood": "downtown",
    "city": "sao paulo",
    "state": "SP",
    "country": "BRA",
}

customer_response_example = {
    "uuid": "3a4b5c6d-7e8f-9a0b-1c2d-3e4f5a6b7c8d",
    **customer_request_example,
    "created_at": "2026-07-24T12:00:00-03:00",
}

staff_request_example = {
    "first_name": "claudia",
    "last_name": "mourao",
    "doc": "10125511827",
    "address": "market avenue",
    "address_number": "234",
    "address_line_2": "room 4",
    "neighborhood": "central district",
    "city": "sao paulo",
    "state": "SP",
    "country": "BRA",
    "role": "customer services",
}

staff_response_example = {
    "uuid": "9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d",
    **staff_request_example,
    "staff_id": 1000001,
    "created_at": "2026-07-24T12:00:00-03:00",
}

customer_patch_request_example = {
    "address": "new avenue",
    "address_number": "1000",
    "city": "sao paulo",
}

staff_patch_request_example = {
    "role": "store manager",
    "address_line_2": "administrative room",
}

validation_error_example = {
    "doc": ["profile with this doc already exists."],
}

not_found_error_example = {"detail": "Not found."}


customer_uuid_parameter = OpenApiParameter(
    name="uuid",
    type=OpenApiTypes.UUID,
    location=OpenApiParameter.PATH,
    description="A UUID string that identifies a customer.",
)

staff_uuid_parameter = OpenApiParameter(
    name="uuid",
    type=OpenApiTypes.UUID,
    location=OpenApiParameter.PATH,
    description="A UUID string that identifies a staff member.",
)


def request_example(name, summary, value):
    return OpenApiExample(name, summary=summary, value=value, request_only=True)


def response_example(name, summary, value):
    return OpenApiExample(name, summary=summary, value=value, response_only=True)


def validation_error_response(entity_name):
    return OpenApiResponse(
        description=(
            f"Invalid {entity_name} payload. Returned when required "
            "fields are missing, fields have invalid values, or unique fields "
            "already exist."
        ),
        examples=[
            response_example(
                "Validation error",
                "Invalid or duplicated request data",
                validation_error_example,
            ),
        ],
    )


def not_found_response(entity_name):
    return OpenApiResponse(
        description=(f"{entity_name.title()} not found for the provided UUID."),
        examples=[
            response_example(
                f"{entity_name.title()} not found",
                "UUID does not match an existing resource",
                not_found_error_example,
            ),
        ],
    )


def method_not_allowed_response(action):
    return OpenApiResponse(
        description=(
            f"Method not allowed. Only GET is supported for the {action} action."
        ),
    )

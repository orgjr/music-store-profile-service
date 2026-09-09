from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
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
    "user_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    **customer_request_example,
    "created_at": "2026-07-24T12:00:00-03:00",
    "updated_at": "2026-07-24T12:30:00-03:00",
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
    "user_uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    **staff_request_example,
    "staff_id": 1000001,
    "created_at": "2026-07-24T12:00:00-03:00",
    "updated_at": "2026-07-24T12:30:00-03:00",
}


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
                {"doc": ["profile with this doc already exists."]},
            ),
        ],
    )


def not_found_response(entity_name):
    return OpenApiResponse(
        description=(f"{entity_name.title()} not found for the authenticated user."),
        examples=[
            response_example(
                f"{entity_name.title()} not found",
                "No resource matches the request",
                {"detail": "Not found."},
            ),
        ],
    )


def unauthorized_response():
    return OpenApiResponse(
        description="Authentication token is missing, invalid or expired.",
        examples=[
            response_example(
                "Unauthenticated",
                "No valid JWT provided in the Authorization header",
                {"detail": "Authentication credentials were not provided."},
            ),
        ],
    )


def forbidden_response(reason):
    return OpenApiResponse(
        description=f"Access denied: {reason}",
        examples=[
            response_example(
                "Permission denied",
                "Authenticated user lacks the required role",
                {"detail": "You do not have permission to perform this action."},
            ),
        ],
    )

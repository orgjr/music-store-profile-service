from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from profiles.customer.serializers import CustomerSerializer

from .config import (
    customer_request_example,
    customer_response_example,
    forbidden_response,
    not_found_response,
    request_example,
    response_example,
    unauthorized_response,
    validation_error_response,
)

customers_schema = extend_schema_view(
    list=extend_schema(
        summary="List customers",
        description=(
            "Returns all registered customer profiles, ordered by creation date "
            "(newest first). Access is restricted to authenticated staff members."
        ),
        tags=["Customers"],
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer(many=True),
                description="List of customer profiles.",
                examples=[
                    response_example(
                        "Customer list",
                        "All registered customer profiles",
                        [customer_response_example],
                    )
                ],
            ),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can list customer profiles."),
        },
    ),
    create=extend_schema(
        summary="Create a customer",
        description=(
            "Registers a new customer profile. Requires authentication. "
            "The `user_uuid` is taken from the authenticated user's JWT token."
        ),
        tags=["Customers"],
        request=CustomerSerializer,
        responses={
            201: OpenApiResponse(
                response=CustomerSerializer,
                description="Customer created successfully.",
                examples=[
                    response_example(
                        "Created customer",
                        "Newly created customer profile",
                        customer_response_example,
                    )
                ],
            ),
            400: validation_error_response("customer"),
            401: unauthorized_response(),
        },
        examples=[
            request_example(
                "New customer",
                "Request body for a customer profile",
                customer_request_example,
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a customer",
        description="Returns a single customer profile by its primary key. Access is restricted to the profile owner or staff.",
        tags=["Customers"],
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="Customer profile returned successfully.",
                examples=[
                    response_example(
                        "Customer profile",
                        "A single customer profile",
                        customer_response_example,
                    )
                ],
            ),
            401: unauthorized_response(),
            403: forbidden_response(
                "only the profile owner or staff members can access customer profiles."
            ),
            404: not_found_response("customer"),
        },
    ),
    update=extend_schema(
        summary="Replace a customer",
        description="Replaces all fields of an existing customer profile. Access is restricted to the profile owner or staff.",
        tags=["Customers"],
        request=CustomerSerializer,
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="Customer updated successfully.",
                examples=[
                    response_example(
                        "Updated customer",
                        "Customer profile after full update",
                        customer_response_example,
                    )
                ],
            ),
            400: validation_error_response("customer"),
            401: unauthorized_response(),
            403: forbidden_response(
                "only the profile owner or staff members can modify customer profiles."
            ),
            404: not_found_response("customer"),
        },
        examples=[
            request_example(
                "Update customer",
                "Full request body for customer profile update",
                customer_request_example,
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update a customer",
        description="Updates one or more fields of an existing customer profile. Access is restricted to the profile owner or staff.",
        tags=["Customers"],
        request=CustomerSerializer,
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="Customer partially updated successfully.",
                examples=[
                    response_example(
                        "Partially updated customer",
                        "Customer profile after partial update",
                        {
                            **customer_response_example,
                            "address": "new avenue",
                            "address_number": "1000",
                        },
                    )
                ],
            ),
            400: validation_error_response("customer"),
            401: unauthorized_response(),
            403: forbidden_response(
                "only the profile owner or staff members can modify customer profiles."
            ),
            404: not_found_response("customer"),
        },
        examples=[
            request_example(
                "Patch customer",
                "Partial request body for customer profile update",
                {
                    "address": "new avenue",
                    "address_number": "1000",
                    "city": "sao paulo",
                },
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a customer",
        description="Permanently deletes a customer profile. Only staff can perform this action.",
        tags=["Customers"],
        responses={
            204: OpenApiResponse(description="Customer deleted successfully."),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can delete customer profiles."),
            404: not_found_response("customer"),
        },
    ),
)

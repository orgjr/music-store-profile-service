from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from profiles.customer.serializers import CustomerSerializer

from .config import (
    customer_list_response_example,
    customer_patch_request_example,
    customer_request_example,
    customer_response_example,
    customer_uuid_parameter,
    not_found_response,
    page_parameter,
    request_example,
    response_example,
    validation_error_response,
)

customer_schema = extend_schema_view(
    list=(
        extend_schema(
            summary="List customers",
            description="Returns a paginated list of registered customers.",
            tags=["Customers"],
            parameters=[page_parameter],
            responses={
                200: OpenApiResponse(
                    response=CustomerSerializer(many=True),
                    description="HTTP 200 - Paginated customer list returned successfully.",
                    examples=[
                        response_example(
                            "Customer list",
                            "Paginated response with customer profiles",
                            customer_list_response_example,
                        ),
                    ],
                ),
            },
        ),
    ),
    create=(
        extend_schema(
            summary="Create a customer",
            description="Registers a new customer in the system.",
            tags=["Customers"],
            request=CustomerSerializer,
            responses={
                201: OpenApiResponse(
                    response=CustomerSerializer,
                    description="HTTP 201 - Customer created successfully.",
                    examples=[
                        response_example(
                            "Created customer",
                            "Newly registered customer profile",
                            customer_response_example,
                        ),
                    ],
                ),
                400: validation_error_response("customer"),
            },
            examples=[
                request_example(
                    "New customer",
                    "Complete request body for customer creation",
                    customer_request_example,
                ),
            ],
        ),
    ),
    retrieve=(
        extend_schema(
            summary="Retrieve a customer",
            description="Returns the data for a specific customer by UUID.",
            tags=["Customers"],
            parameters=[customer_uuid_parameter],
            responses={
                200: OpenApiResponse(
                    response=CustomerSerializer,
                    description="HTTP 200 - Customer profile returned successfully.",
                    examples=[
                        response_example(
                            "Customer details",
                            "Customer profile found by UUID",
                            customer_response_example,
                        ),
                    ],
                ),
                404: not_found_response("customer"),
            },
        ),
    ),
    update=(
        extend_schema(
            summary="Update a customer",
            description="Replaces all fields for an existing customer.",
            tags=["Customers"],
            parameters=[customer_uuid_parameter],
            request=CustomerSerializer,
            responses={
                200: OpenApiResponse(
                    response=CustomerSerializer,
                    description="HTTP 200 - Customer profile updated successfully.",
                    examples=[
                        response_example(
                            "Updated customer",
                            "Customer profile after full update",
                            customer_response_example,
                        ),
                    ],
                ),
                400: validation_error_response("customer"),
                404: not_found_response("customer"),
            },
            examples=[
                request_example(
                    "Replace customer",
                    "Complete request body for customer replacement",
                    customer_request_example,
                ),
            ],
        ),
    ),
    partial_update=(
        extend_schema(
            summary="Partially update a customer",
            description="Updates one or more fields for an existing customer.",
            tags=["Customers"],
            parameters=[customer_uuid_parameter],
            request=CustomerSerializer,
            responses={
                200: OpenApiResponse(
                    response=CustomerSerializer,
                    description="HTTP 200 - Customer profile partially updated successfully.",
                    examples=[
                        response_example(
                            "Partially updated customer",
                            "Customer profile after partial update",
                            {
                                **customer_response_example,
                                **customer_patch_request_example,
                            },
                        ),
                    ],
                ),
                400: validation_error_response("customer"),
                404: not_found_response("customer"),
            },
            examples=[
                request_example(
                    "Patch customer",
                    "Partial request body for customer update",
                    customer_patch_request_example,
                ),
            ],
        ),
    ),
    destroy=(
        extend_schema(
            summary="Delete a customer",
            description="Permanently deletes a customer from the system.",
            tags=["Customers"],
            parameters=[customer_uuid_parameter],
            responses={
                204: OpenApiResponse(
                    description="HTTP 204 - Customer profile deleted successfully."
                ),
                404: not_found_response("customer"),
            },
        ),
    ),
)

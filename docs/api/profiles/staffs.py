from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from profiles.staff.serializers import StaffSerializer

from .config import (
    forbidden_response,
    not_found_response,
    request_example,
    response_example,
    staff_request_example,
    staff_response_example,
    unauthorized_response,
    validation_error_response,
)

staffs_schema = extend_schema_view(
    list=extend_schema(
        summary="List staff members",
        description=(
            "Returns all registered staff profiles, ordered by creation date "
            "(newest first). Access is restricted to authenticated staff members."
        ),
        tags=["Staff"],
        responses={
            200: OpenApiResponse(
                response=StaffSerializer(many=True),
                description="List of staff profiles.",
                examples=[
                    response_example(
                        "Staff list",
                        "All registered staff profiles",
                        [staff_response_example],
                    )
                ],
            ),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can list staff profiles."),
        },
    ),
    create=extend_schema(
        summary="Create a staff member",
        description=(
            "Registers a new staff profile. Requires staff access. "
            "The `user_uuid` is taken from the authenticated user's JWT token. "
            "The `staff_id` is auto-generated."
        ),
        tags=["Staff"],
        request=StaffSerializer,
        responses={
            201: OpenApiResponse(
                response=StaffSerializer,
                description="Staff profile created successfully.",
                examples=[
                    response_example(
                        "Created staff member",
                        "Newly created staff profile",
                        staff_response_example,
                    )
                ],
            ),
            400: validation_error_response("staff profile"),
            401: unauthorized_response(),
        },
        examples=[
            request_example(
                "New staff member",
                "Request body for a staff profile",
                staff_request_example,
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a staff member",
        description="Returns a single staff profile by its primary key. Requires staff access.",
        tags=["Staff"],
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="Staff profile returned successfully.",
                examples=[
                    response_example(
                        "Staff profile",
                        "A single staff profile",
                        staff_response_example,
                    )
                ],
            ),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can access staff profiles."),
            404: not_found_response("staff profile"),
        },
    ),
    update=extend_schema(
        summary="Replace a staff member",
        description="Replaces all fields of an existing staff profile. Requires staff access.",
        tags=["Staff"],
        request=StaffSerializer,
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="Staff profile updated successfully.",
                examples=[
                    response_example(
                        "Updated staff member",
                        "Staff profile after full update",
                        staff_response_example,
                    )
                ],
            ),
            400: validation_error_response("staff profile"),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can modify staff profiles."),
            404: not_found_response("staff profile"),
        },
        examples=[
            request_example(
                "Update staff member",
                "Full request body for staff profile update",
                staff_request_example,
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update a staff member",
        description="Updates one or more fields of an existing staff profile. Requires staff access.",
        tags=["Staff"],
        request=StaffSerializer,
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="Staff profile partially updated successfully.",
                examples=[
                    response_example(
                        "Partially updated staff member",
                        "Staff profile after partial update",
                        {
                            **staff_response_example,
                            "role": "store manager",
                            "address_line_2": "administrative room",
                        },
                    )
                ],
            ),
            400: validation_error_response("staff profile"),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can modify staff profiles."),
            404: not_found_response("staff profile"),
        },
        examples=[
            request_example(
                "Patch staff member",
                "Partial request body for staff profile update",
                {"role": "store manager", "address_line_2": "administrative room"},
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a staff member",
        description="Permanently deletes a staff profile. Requires staff access.",
        tags=["Staff"],
        responses={
            204: OpenApiResponse(description="Staff profile deleted successfully."),
            401: unauthorized_response(),
            403: forbidden_response("only staff members can delete staff profiles."),
            404: not_found_response("staff profile"),
        },
    ),
)

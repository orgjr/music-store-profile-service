from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from profiles.staff.serializers import StaffSerializer

from .config import (
    not_found_response,
    page_parameter,
    request_example,
    response_example,
    staff_list_response_example,
    staff_patch_request_example,
    staff_request_example,
    staff_response_example,
    staff_uuid_parameter,
    validation_error_response,
)

staff_schema = extend_schema_view(
    list=extend_schema(
        summary="List staff members",
        description="Returns a paginated list of registered staff members.",
        tags=["Staff"],
        parameters=[page_parameter],
        responses={
            200: OpenApiResponse(
                response=StaffSerializer(many=True),
                description="HTTP 200 - Paginated staff list returned successfully.",
                examples=[
                    response_example(
                        "Staff list",
                        "Paginated response with staff profiles",
                        staff_list_response_example,
                    ),
                ],
            ),
        },
    ),
    create=extend_schema(
        summary="Create a staff member",
        description="Registers a new staff member in the system.",
        tags=["Staff"],
        request=StaffSerializer,
        responses={
            201: OpenApiResponse(
                response=StaffSerializer,
                description="HTTP 201 - Staff member created successfully.",
                examples=[
                    response_example(
                        "Created staff member",
                        "Newly registered staff profile",
                        staff_response_example,
                    ),
                ],
            ),
            400: validation_error_response("staff member"),
        },
        examples=[
            request_example(
                "New staff member",
                "Complete request body for staff creation",
                staff_request_example,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a staff member",
        description="Returns the data for a specific staff member by UUID.",
        tags=["Staff"],
        parameters=[staff_uuid_parameter],
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="HTTP 200 - Staff profile returned successfully.",
                examples=[
                    response_example(
                        "Staff member details",
                        "Staff profile found by UUID",
                        staff_response_example,
                    ),
                ],
            ),
            404: not_found_response("staff member"),
        },
    ),
    update=extend_schema(
        summary="Update a staff member",
        description="Replaces all fields for an existing staff member.",
        tags=["Staff"],
        parameters=[staff_uuid_parameter],
        request=StaffSerializer,
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="HTTP 200 - Staff profile updated successfully.",
                examples=[
                    response_example(
                        "Updated staff member",
                        "Staff profile after full update",
                        staff_response_example,
                    ),
                ],
            ),
            400: validation_error_response("staff member"),
            404: not_found_response("staff member"),
        },
        examples=[
            request_example(
                "Replace staff member",
                "Complete request body for staff replacement",
                staff_request_example,
            ),
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update a staff member",
        description="Updates one or more fields for an existing staff member.",
        tags=["Staff"],
        parameters=[staff_uuid_parameter],
        request=StaffSerializer,
        responses={
            200: OpenApiResponse(
                response=StaffSerializer,
                description="HTTP 200 - Staff profile partially updated successfully.",
                examples=[
                    response_example(
                        "Partially updated staff member",
                        "Staff profile after partial update",
                        {
                            **staff_response_example,
                            **staff_patch_request_example,
                        },
                    ),
                ],
            ),
            400: validation_error_response("staff member"),
            404: not_found_response("staff member"),
        },
        examples=[
            request_example(
                "Patch staff member",
                "Partial request body for staff update",
                staff_patch_request_example,
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Delete a staff member",
        description="Permanently deletes a staff member from the system.",
        tags=["Staff"],
        parameters=[staff_uuid_parameter],
        responses={
            204: OpenApiResponse(
                description="HTTP 204 - Staff profile deleted successfully."
            ),
            404: not_found_response("staff member"),
        },
    ),
)

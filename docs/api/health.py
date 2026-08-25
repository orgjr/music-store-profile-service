from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

health_response_serializer = inline_serializer(
    name="HealthCheck",
    fields={
        "status": serializers.CharField(),
        "timestamp": serializers.DateTimeField(),
        "uptime_seconds": serializers.FloatField(),
    },
)

health_response_example = {
    "status": "ok",
    "timestamp": "2026-07-24T12:00:00-03:00",
    "uptime_seconds": 123.453478,
}

health_no_content_example = {"detail": "Method \"POST\" not allowed."}


health_schema = extend_schema(
    summary="Health check",
    description="Returns the service health status, timestamp and uptime.",
    tags=["Core"],
    responses={
        200: OpenApiResponse(
            response=health_response_serializer,
            description="HTTP 200 - Service health status returned successfully.",
            examples=[
                OpenApiExample(
                    "Health status",
                    summary="Healthy service response",
                    value=health_response_example,
                    response_only=True,
                ),
            ],
        ),
        405: OpenApiResponse(
            description="HTTP 405 - Method not allowed. Only GET is supported.",
            examples=[
                OpenApiExample(
                    "Method not allowed",
                    summary="Non-GET request rejected",
                    value=health_no_content_example,
                    response_only=True,
                ),
            ],
        ),
    },
)

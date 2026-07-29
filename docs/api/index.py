from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

index_response_serializer = inline_serializer(
    name="ServiceInfo",
    fields={
        "name": serializers.CharField(),
        "version": serializers.CharField(),
        "description": serializers.CharField(),
        "environment": serializers.CharField(),
        "redoc_url": serializers.CharField(),
        "health_url": serializers.CharField(),
        "api_version": serializers.CharField(),
    },
)

index_response_example = {
    "name": "Music Store Profile Service",
    "version": "0.9.0",
    "description": "Profile management microservice for the Music Store project",
    "environment": "development",
    "redoc_url": "/api/v1/redoc/",
    "health_url": "/api/v1/health/",
    "api_version": "v1",
}


index_schema = extend_schema(
    summary="Service information",
    description="Returns metadata for the Music Store Profile Service.",
    tags=["core"],
    responses={
        200: OpenApiResponse(
            response=index_response_serializer,
            description="HTTP 200 - Service metadata returned successfully.",
            examples=[
                OpenApiExample(
                    "Service metadata",
                    summary="Public service information",
                    value=index_response_example,
                    response_only=True,
                ),
            ],
        ),
    },
)

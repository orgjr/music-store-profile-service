from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from docs.api.health import health_schema
from docs.api.index import index_response_example, index_schema

START_TIME = timezone.now()


@index_schema
@api_view(["GET"])
def index(request):
    return Response(index_response_example)


@health_schema
@api_view(["GET"])
def health(request):
    uptime = timezone.now() - START_TIME
    return Response(
        {
            "status": "ok",
            "timestamp": timezone.now(),
            "uptime_seconds": uptime.total_seconds(),
        }
    )

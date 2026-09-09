from rest_framework import status
from rest_framework.exceptions import APIException


class InstanceCreationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

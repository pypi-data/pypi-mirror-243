from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class MonoTokenDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Monobank not added."
    default_code = "Monobank_not_added"


class MonoTokenExistsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Monobank already added."
    default_code = "Monobank_already_added"


class TooManyRequestsExistsException(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

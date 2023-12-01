from rest_framework import status
from rest_framework.exceptions import APIException


class PrivatBankDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Privatbank not added."
    default_code = "Privatbank_not_added."


class PrivatBankExistsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Privatbank already added."
    default_code = "Privatbank_already_added."


class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .serializers import (
    PrivatbankSerializer,
    PrivatbankPaymentSerializer,
    PrivatbankPeriodSerializer,
)
from .exceptions import (
    PrivatBankDoesNotExistsException,
    PrivatBankExistsException,
    UnauthorizedException,
    BadRequestException,
)
from .config import (
    PRIVATBANK_ADDED,
    PRIVATBANK_CHANGED,
)
from .managers import PrivatManager

mng = PrivatManager


class PrivatBankView(GenericAPIView):
    serializer_class = PrivatbankSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            raise PrivatBankExistsException
        
        privat_obj.create(
            privat_token=_["privat_token"],
            iban_UAH=_["iban_UAH"],
            user=request.user
        )
        return Response(PRIVATBANK_ADDED, status.HTTP_201_CREATED)
    
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            privat_obj.update(
                privat_token=_["privat_token"],
                iban_UAH=_["iban_UAH"]
            )
            return Response(PRIVATBANK_CHANGED)
        
        raise PrivatBankDoesNotExistsException
    
    def delete(self, request):
        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            privat_obj.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        
        raise PrivatBankDoesNotExistsException


class PrivatBankCurrencyCashRate(APIView):
    
    def get(self, request):
        _status, payload = mng.get_currency(cashe_rate=True)
        if _status == 200:
            return Response(payload)
        
        raise APIException(detail=payload)
        

class PrivatBankCurrencyNonCashRate(APIView):

    def get(self, request):
        _status, payload = mng.get_currency(cashe_rate=False)
        if _status == 200:
            return Response(payload)
        
        raise APIException(detail=payload)


class PrivatBankInfo(APIView):

    def get(self, request):
        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            _status, payload = mng.get_client_info(
                privat_obj.first().privat_token,
                privat_obj.first().iban_UAH
            )
            if _status == 400:
                raise BadRequestException(detail=payload)
            if _status == 401:
                raise UnauthorizedException(detail=payload)
            
            return Response(payload)

        raise PrivatBankDoesNotExistsException


class BalancePrivatView(APIView):

    def get(self, request):
        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            _status, payload = mng.get_balance(
                privat_obj.first().privat_token,
                privat_obj.first().iban_UAH
            )
            if _status == 400:
                raise BadRequestException(detail=payload)
            if _status == 401:
                raise UnauthorizedException(detail=payload)
            
            return Response(payload)

        raise PrivatBankDoesNotExistsException


class StatementPrivatView(GenericAPIView):
    serializer_class = PrivatbankPeriodSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            period = _["period"]
            limit = _["limit"]
            _status, payload = mng.get_statement(
                privat_obj.first().privat_token,
                privat_obj.first().iban_UAH,
                period,
                limit,
            )
            if _status == 400:
                raise BadRequestException(detail=payload)
            if _status == 401:
                raise UnauthorizedException(detail=payload)
            
            return Response(payload)

        raise PrivatBankDoesNotExistsException


class PaymentPrivatView(GenericAPIView):
    serializer_class = PrivatbankPaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        privat_obj = mng.get_privat_object(request)
        if privat_obj.first() is not None:
            _status, payload = mng.create_payment(
                privat_obj.first().privat_token,
                privat_obj.first().iban_UAH,
                _["recipient"],
                str(_["amount"])
            )
            if _status == 201:
                return Response(payload, status.HTTP_201_CREATED)
            if _status == 400:
                raise BadRequestException(detail=payload)
            if _status == 401:
                raise UnauthorizedException(detail=payload)
            
        raise PrivatBankDoesNotExistsException

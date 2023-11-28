from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .managers import MonoManager
from .serializers import(
    MonoTokenSerializer,
    WebhookSerializer,
    PeriodSerializer,
)
from .exceptions import(
    BadRequestException,
    MonoTokenExistsException,
    MonoTokenDoesNotExistsException,
    ForbiddenException,
    TooManyRequestsExistsException,
)
from .config import (
    MONO_ADDED,
    MONO_CHANGED,
)

mng = MonoManager


class MonoView(GenericAPIView):
    serializer_class = MonoTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            raise MonoTokenExistsException

        mono_obj.create(
            mono_token=_["mono_token"],
            user=request.user
        )
        return Response(MONO_ADDED, status.HTTP_201_CREATED)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            mono_obj.update(mono_token=_["mono_token"])
            return Response(MONO_CHANGED)

        raise MonoTokenDoesNotExistsException
    
    def delete(self, request):
        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            mono_obj.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        
        raise MonoTokenDoesNotExistsException


class CurrencyView(APIView):

    def get(self, request):
        _status, payload = mng.get_currency()
        if _status == 429:
            raise TooManyRequestsExistsException(detail=payload)
        
        return Response(payload)


class ClientInfoView(APIView):

    def get(self, request):
        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            _status, payload = mng.get_client_info_mono(
                mono_obj.first().mono_token
            )
            if _status == 403:
                raise ForbiddenException(detail=payload)
            if _status == 429:
                raise TooManyRequestsExistsException(detail=payload)

            return Response(payload)
        
        raise MonoTokenDoesNotExistsException
    

class BalanceView(APIView):

    def get(self, request):
        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            _status, payload = mng.get_balance_mono(
                mono_obj.first().mono_token
            )
            if _status == 403:
                raise ForbiddenException(detail=payload)
            if _status == 429:
                raise TooManyRequestsExistsException(detail=payload)
            
            return Response(payload)

        raise MonoTokenDoesNotExistsException
    

class StatementView(GenericAPIView):
    serializer_class = PeriodSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            _status, payload = mng.get_statement_mono(
                mono_obj.first().mono_token,
                _["period"],
            )
            if _status == 403:
                raise ForbiddenException(detail=payload)
            if _status == 429:
                raise TooManyRequestsExistsException(detail=payload)
            
            return Response(payload)
        
        raise MonoTokenDoesNotExistsException


class CreateWebhook(GenericAPIView):
    serializer_class = WebhookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _ = serializer.validated_data

        mono_obj = mng.get_mono_object(request)
        if mono_obj.first() is not None:
            _status, payload = mng.create_webhook(
                mono_obj.first().mono_token,
                _["webHookUrl"]
            )
            if _status == 400:
                raise BadRequestException(detail=payload)
            if _status == 403:
                raise ForbiddenException(detail=payload)
            if _status == 429:
                raise TooManyRequestsExistsException(detail=payload)
            
            return Response(payload)
        
        raise MonoTokenDoesNotExistsException

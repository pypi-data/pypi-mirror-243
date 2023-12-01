from rest_framework.serializers import *
from .models import Privatbank


class PrivatbankSerializer(ModelSerializer):
    class Meta:
        model = Privatbank
        fields = ['privat_token', 'iban_UAH']
        extra_kwargs = {"privat_token": {"write_only": True}}


class PrivatbankPaymentSerializer(Serializer):
    amount = FloatField(min_value=0.01)
    recipient = CharField(max_length=16)


class PrivatbankPeriodSerializer(Serializer):
    period = IntegerField(min_value=0)
    limit = IntegerField(default=100, min_value=0, max_value=500)
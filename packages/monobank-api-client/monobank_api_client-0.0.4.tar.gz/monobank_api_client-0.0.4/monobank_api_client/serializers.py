from rest_framework.serializers import *
from .models import Mono


class MonoTokenSerializer(ModelSerializer):
    class Meta:
        model = Mono
        fields = ['mono_token']
        extra_kwargs = {"mono_token": {"write_only": True}}


class PeriodSerializer(Serializer):
    period = IntegerField(min_value=0, max_value=31)


class WebhookSerializer(Serializer):
    webHookUrl = URLField()

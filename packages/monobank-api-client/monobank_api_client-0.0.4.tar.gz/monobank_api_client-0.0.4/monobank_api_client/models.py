from django.db.models import *
from django.utils import timezone


class Mono(Model):
    mono_token = CharField(
        max_length=44,
        blank=False,
        unique=True,
    )
    user_id = CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True
    )
    date_joined = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_id

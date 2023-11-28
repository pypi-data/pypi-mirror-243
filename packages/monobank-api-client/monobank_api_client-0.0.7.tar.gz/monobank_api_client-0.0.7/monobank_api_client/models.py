from django.db.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Mono(Model):
    mono_token = CharField(
        max_length=44,
        blank=False,
        unique=True,
    )
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        unique=True
    )
    date_joined = DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.email

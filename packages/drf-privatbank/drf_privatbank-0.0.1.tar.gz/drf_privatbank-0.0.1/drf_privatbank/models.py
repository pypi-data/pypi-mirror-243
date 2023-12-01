from django.db.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Privatbank(Model):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        blank=False,
        unique=True,
    )
    privat_token = CharField(
        max_length=292,
        blank=False,
        unique=True,
    )
    iban_UAH = CharField(
        max_length=29,
        blank=False,
        unique=True,
    )
    date_joined = DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.email
from django.contrib import admin
from .models import Privatbank


@admin.register(Privatbank)
class PrivatbankAdmin(admin.ModelAdmin):
    list_display = ("user", "privat_token", "iban_UAH", "date_joined",)

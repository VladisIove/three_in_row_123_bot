from django.contrib import admin
from .models import TelegramUser

# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "referral", "balance")
from django.contrib import admin
from .models import TelegramUser, AIChat


class ChatInline(admin.TabularInline):
    model = AIChat
    extra = 0  
    can_delete = False
    readonly_fields = ('rate', 'feedback', 'conversation')
    fields = ('rate', 'feedback', 'conversation')
    
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", )
    inlines = [ChatInline]
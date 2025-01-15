from django.contrib import admin
from .models import TelegramUser, AIChat
import json
from django.utils.html import format_html

class ChatInline(admin.TabularInline):
    model = AIChat
    extra = 0  
    can_delete = False
    readonly_fields = ('rate', 'feedback', 'conversation')
    fields = ('rate', 'feedback', 'conversation')

    def formatted_conversation(self, instance):
        if not instance.conversation:
            return "No conversation available"
        try:
            conversation_data = json.loads(instance.conversation)
            formatted = []
            for entry in conversation_data:
                role = entry.get("role", "unknown").capitalize()
                content = entry.get("content", "")
                formatted.append(f"<strong>{role}:</strong> {content}")
            return format_html("<br>".join(formatted))
        except json.JSONDecodeError:
            return "Invalid conversation format"
    formatted_conversation.short_description = "Conversation"
    
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", )
    inlines = [ChatInline]
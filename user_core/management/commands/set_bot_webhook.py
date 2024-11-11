import logging
from django.core.management.base import BaseCommand
from telebot import TeleBot
from django.conf import settings

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
WEBHOOK_URL = 'https://5cc6-91-225-122-12.ngrok-free.app/webhook/telegram/'  # Replace with your webhook URL

bot = settings.TELEGRAM_BOT

class Command(BaseCommand):
    help = 'Sets the Telegram bot webhook'

    def handle(self, *args, **options):
        try:
            # Remove any existing webhook
            bot.remove_webhook()
            # Set the new webhook
            success = bot.set_webhook(url=WEBHOOK_URL)
            if success:
                self.stdout.write(self.style.SUCCESS(f'Successfully set webhook to {WEBHOOK_URL}'))
            else:
                self.stdout.write(self.style.ERROR('Failed to set webhook'))
        except Exception as e:
            logging.error("Error setting webhook", exc_info=e)
            self.stdout.write(self.style.ERROR(f'Error setting webhook: {e}'))

from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django import http
from django.conf import settings
from django.forms.models import model_to_dict

from user_core.models import TelegramUser
from user_core.integrations.openai.client import ClientOpenAI
from typing import Any
from django.http import HttpResponse, JsonResponse
from pathlib import Path
import base64 
from django.core.cache import cache
from uuid import uuid4
from pydub import AudioSegment

bot = settings.TELEGRAM_BOT

class MainPageWebApp(TemplateView):
    template_name = 'index.html'

class AIChat(View):
    @staticmethod
    def save_to_mp3(bytes_io_object, output_path):
        bytes_io_object.seek(0)

        # Open the file in binary write mode and save the content
        with open(output_path, "wb") as f:
            f.write(bytes_io_object.read())
        try:
            audio = AudioSegment.from_file(f.name, "mp4")
        except:
            audio =  AudioSegment.from_file(f.name, "mp3")
        audio.export('input.ogg', format='ogg')
        
    def post(self, request: http.HttpRequest):
        promt = request.POST.get('promt')
        cache_key = request.POST.get('cache_key')
        messages = cache.get(cache_key)
        self.save_to_mp3(request.FILES['audioFile'], 'input.mp3')
        audio, messages = ClientOpenAI().speech_to_speech_chat(Path(__file__).parent.parent / 'input.ogg', promt, messages)
        if not cache_key:
            cache_key = str(uuid4())
        cache.set(cache_key, messages, timeout=60*60)  # Timeout in seconds
        response = HttpResponse(audio)
        response['X-CACHE-KEY'] = cache_key
        return response

class GetOrCreateUser(View):

    @transaction.atomic
    def get_or_create(self, tg_id, referral_token = None):
        user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        if user:
            user_data = model_to_dict(user)
            user_data['share_url'] = settings.REFFERAL_LINK_TEXT.format(user.referral_token)
            return user_data
        if referral_token and referral_token != "undefined":
            referral = TelegramUser.objects.filter(referral_token=referral_token).first()
        else: 
            referral = None

        user = TelegramUser()
        user.telegram_id = tg_id
        if isinstance(referral, TelegramUser):
            user.referral = referral
        user.save()
        user_data = model_to_dict(user)
        if isinstance(referral, TelegramUser):
            bot.send_message(referral.pk, "Some one register by you refferal link")
            referral.balance += 1
            user.balance += 1
            referral.save()
            user.save()
        user_data = model_to_dict(user)
        user_data['share_url'] = settings.REFFERAL_LINK_TEXT.format(user.referral_token, user.referral_token)
        return user_data

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        tg_id, referral_token  = request.GET.get("tg_id"), request.GET.get("referral_token") 
        data = self.get_or_create(tg_id, referral_token)
        return JsonResponse(data)
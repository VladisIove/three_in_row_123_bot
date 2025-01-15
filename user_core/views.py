from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django import http
from django.conf import settings
from django.forms.models import model_to_dict
import os 
import json
from user_core.models import TelegramUser, AIChat as  AIChatModel
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


class FeedbackView(View):
    def post(self, request: http.HttpRequest):
        chat_id = request.POST.get('chat_id')
        tg_id = request.POST.get('tg_id')
        rate = request.POST.get('rate')
        feedback = request.POST.get('feedback')
        
        ai_chat = AIChatModel.objects.filter(id=chat_id, tg_user_id=tg_id).first()
        if ai_chat:
            ai_chat.rate = rate 
            ai_chat.feedback = feedback 
            ai_chat.save()
            
        return HttpResponse('ok')

class AIChat(View):
    @staticmethod
    def save_to_mp3(bytes_io_object, suffix: str = ''):
        output_path = f'input_{suffix}.mp3'
        bytes_io_object.seek(0)

        # Open the file in binary write mode and save the content
        with open(output_path, "wb") as f:
            f.write(bytes_io_object.read())
            
        try:
            audio = AudioSegment.from_file(f.name, "mp4")
        except:
            try:
                audio =  AudioSegment.from_file(f.name, "mp3")
            except: 
                try: 
                    audio = AudioSegment.from_file(f.name, codec="opus")
                except:
                    audio =  AudioSegment.from_file(f.name)
                
        audio.export(f'input_{suffix}.ogg', format='ogg')
        
    @staticmethod
    def _clean(suffix: str = ''):
        formats = ['mp3', 'ogg']
        for format in formats:
            file = f'input_{suffix}.{format}'
            os.remove(file)
    
    @staticmethod
    def _get_chat_information(chat_id: str, tg_id: str) -> AIChatModel:
        
        ai_chat = None    
        if chat_id:
            ai_chat = AIChatModel.objects.filter(id=chat_id, tg_user_id=tg_id).first()
        
        if not ai_chat: 
            ai_chat = AIChatModel.objects.create(tg_user = TelegramUser.objects.get(telegram_id=tg_id))
            ai_chat.save()
        
        return ai_chat
            
        
    def post(self, request: http.HttpRequest):
        chat_id = request.POST.get('chat_id')
        tg_id = request.POST.get('tg_id')
        
        ai_chat = self._get_chat_information(chat_id, tg_id)  
        suffix = f"{ai_chat.id}_{tg_id}"  
                
        self.save_to_mp3(request.FILES['audioFile'], suffix)
        messages = json.loads(ai_chat.conversation) if ai_chat.conversation else []
        audio, messages = ClientOpenAI().speech_to_speech_chat(Path(__file__).parent.parent / f'input_{suffix}.ogg', settings.OPENAI_PROMT, messages)
        
        ai_chat.conversation = json.dumps(messages)
        ai_chat.save()
        
        self._clean(suffix)
        
        response = HttpResponse(audio)
        response['X-CACHE-KEY'] = ai_chat.id
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
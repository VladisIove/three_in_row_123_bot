from django.views.generic import TemplateView
from django.views import View
from django import http
from django.forms.models import model_to_dict

from user_core.models import TelegramUser

from typing import Any

class MainPageWebApp(TemplateView):
    template_name = 'index.html'
    

class GetOrCreateUser(View):
    
    def get_or_create(self, tg_id, referral_token = None):
        user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        if user: 
            return model_to_dict(user)
        referral = referral_token or TelegramUser.objects.filter(referral_token=referral_token).first()
        
        user = TelegramUser()
        user.telegram_id = tg_id
        user.referral = referral 
        user.save()
        return model_to_dict(user)
        
    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        
        data = request.data 
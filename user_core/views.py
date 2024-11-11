from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django import http
from django.conf import settings
from django.forms.models import model_to_dict

from user_core.models import TelegramUser

from typing import Any

bot = settings.TELEGRAM_BOT

class MainPageWebApp(TemplateView):
    template_name = 'inde1x.html'


class GetOrCreateUser(View):

    @transaction.atomic
    def get_or_create(self, tg_id, referral_token = None):
        user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        if user:
            user_data = model_to_dict(user)
            user_data['share_url'] = settings.REFFERAL_LINK_TEXT.format(user.referral_token)
            return user_data
        if referral_token and referral_token != "null":
            referral = TelegramUser.objects.filter(referral_token=referral_token).first()

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
        user_data['share_url'] = settings.REFFERAL_LINK_TEXT.format(user.referral_token)
        return user_data

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        tg_id, referral_token  = request.GET.get("tg_id"), request.GET.get("referral_token") 
        data = self.get_or_create(tg_id, referral_token)
        return JsonResponse(data)
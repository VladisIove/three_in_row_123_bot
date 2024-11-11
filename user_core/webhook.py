# views.py
import telebot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

bot = settings.TELEGRAM_BOT

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'}, status=400)



@bot.message_handler(commands=['start'])
def send_open_link(message):
    link = (
        'https://t.me/three_in_row_123_bot?startapp=rp_1365932&text=%F0%9F%92%B0Catizen%3A%20Unleash%2C%20Play%2C%20Earn%20-'
        '%20Where%20Every%20Game%20Leads%20to%20an%20Airdrop%20Adventure!%0A'
        '%F0%9F%8E%81Let%27s%20play-to-earn%20airdrop%20right%20now!'
    )
    bot.send_message(message.chat.id, f"Click to join the airdrop adventure: [Open Link]({link})", parse_mode='Markdown')

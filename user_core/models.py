from django.db import models
import uuid 
# Create your models here.

class TelegramUser(models.Model):
    
    telegram_id = models.IntegerField(primary_key=True)
    referral_token = models.UUIDField(default = uuid.uuid4)
    referral = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.SET_NULL) 
    balance = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "telegram_user" 
        ordering = ["telegram_id"]

    def __str__(self) -> str:
        return str(self.telegram_id)
from django.db import models

from accounts.models import CustomUser


class BotUser(CustomUser):
    personality = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Bot User"
        verbose_name_plural = "Bot Users"

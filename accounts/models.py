import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_tied = models.IntegerField(default=0)
    games_abandoned = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("userprofile_detail", args=[str(self.id)])

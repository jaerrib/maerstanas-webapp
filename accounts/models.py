import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_tied = models.IntegerField(default=0)
    games_abandoned = models.IntegerField(default=0)
    rating = models.FloatField(default=1000)
    is_bot = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("userprofile_detail", args=[str(self.id)])

    @property
    def games_played(self):
        games_won = self.games_won or 0
        games_lost = self.games_lost or 0
        games_tied = self.games_tied or 0
        return games_won + games_lost + games_tied

    @property
    def win_percentage(self):
        total_games = self.games_played
        winning_games = self.games_won or 0
        if total_games == 0:
            return 0.0
        return (winning_games / total_games) * 100

    @property
    def display_rating(self):
        return int(self.rating)

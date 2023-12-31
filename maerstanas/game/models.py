from django.db import models
from .game_logic.game import Game
from users.models import User
# from maerstanas.users.models import User


# Create your models here.
class SessionGame(models.Model):
    game_name = models.CharField(max_length=45)
    game = Game()
    player_one = models.ForeignKey(
        User,
        related_name="hosted_games",
        on_delete=models.CASCADE
    )
    player_two = models.ForeignKey(
        User,
        related_name="joined_games",
        on_delete=models.CASCADE,
        null=True
    )
    protected = models.BooleanField(False)
    password = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game_name

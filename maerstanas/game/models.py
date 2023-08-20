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
    password = models.CharField(max_length=255, blank=True)
    # status 0 is active, status 1 or 2 indicates which player won, 3 is a tie
    status = models.IntegerField()
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game_name

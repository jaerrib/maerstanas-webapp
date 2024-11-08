import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.urls import reverse


def default_array():
    return {"data": []}


class Game(models.Model):
    RESULT_CHOICES = [
        ("Player 1", "Player 1"),
        ("Player 2", "Player 2"),
        ("Tie", "Tie"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    gameboard = models.JSONField(default=default_array)
    played_moves_list = models.JSONField(default=default_array)
    moves_left_list = models.JSONField(default=default_array)

    player1 = models.ForeignKey(
        get_user_model(), related_name="hosted_games", on_delete=models.CASCADE
    )

    player2 = models.ForeignKey(
        get_user_model(),
        related_name="joined_games",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    score_p1 = models.IntegerField(default=0)
    score_p2 = models.IntegerField(default=0)

    active_player = models.IntegerField(default=1)

    using_special_stones = models.BooleanField(default=True)
    using_standard_scoring = models.BooleanField(default=True)

    game_over = models.BooleanField(default=False)
    result = models.CharField(
        max_length=10, choices=RESULT_CHOICES, blank=True, null=True
    )

    p1_has_thunder_stone = models.BooleanField(default=True)
    p1_has_woden_stone = models.BooleanField(default=True)
    p2_has_thunder_stone = models.BooleanField(default=True)
    p2_has_woden_stone = models.BooleanField(default=True)
    is_archived_for_p1 = models.BooleanField(default=False)
    is_archived_for_p2 = models.BooleanField(default=False)

    password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, raw_password):
        if raw_password:
            self.password = make_password(raw_password)
        else:
            self.password = ""

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("game_detail", args=[str(self.id)])

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.forms import JSONField
from django.urls import reverse


class GameBoard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()

    def __str__(self):
        return f"Gameboard {self.id}"


class PlayedMovesList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()

    def __str__(self):
        return f"Played moves List {self.id}"


class MovesLeftList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()

    def __str__(self):
        return f"Moves Left List {self.id}"


class Game(models.Model):
    RESULT_CHOICES = [
        ("Player 1", "Player 1"),
        ("Player 2", "Player 2"),
        ("Tie", "Tie"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    gameboard = models.OneToOneField(
        GameBoard, related_name="game_boards", on_delete=models.CASCADE
    )

    played_moves_list = models.OneToOneField(
        PlayedMovesList, related_name="move_lists", on_delete=models.CASCADE
    )

    moves_left_list = models.OneToOneField(
        MovesLeftList, related_name="moves_left", on_delete=models.CASCADE
    )

    player1 = models.ForeignKey(
        get_user_model(), related_name="hosted_games", on_delete=models.CASCADE
    )

    player2 = models.ForeignKey(
        get_user_model(),
        related_name="joined_games",
        on_delete=models.CASCADE,
        null=True,
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("game_detail", args=[str(self.id)])

from django.contrib.auth import get_user_model
from django.test import TestCase

from .logic import game_rules
from .models import Game, GameBoard, PlayedMovesList, MovesLeftList


class GamesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.player1 = get_user_model().objects.create_user(
            username="player1",
            email="player1@email.com",
            password="testpass123",
        )

        cls.player2 = get_user_model().objects.create_user(
            username="player2",
            email="player2@email.com",
            password="testpass123",
        )

        cls.gameboard = GameBoard.objects.create()
        cls.played_moves_list = PlayedMovesList.objects.create()
        cls.moves_left_list = MovesLeftList.objects.create()

        cls.game = Game.objects.create(
            name="Test Game",
            player1=cls.player1,
            gameboard=cls.gameboard,
            played_moves_list=cls.played_moves_list,
            moves_left_list=cls.moves_left_list,
        )

    def test_game_setup(self):
        self.game = game_rules.initialize_game(self.game)
        self.assertEqual(self.game.gameboard.data[0][0], [3, 3])
        self.assertIn([1, 1], self.game.moves_left_list.data)
        self.assertNotIn([0, 1], self.game.moves_left_list.data)

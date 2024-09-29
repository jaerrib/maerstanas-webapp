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
        cls.game = game_rules.initialize_game(cls.game)

    def test_game_setup(self):
        # Test correct assignment of values when initializing with game_rules
        self.assertEqual(self.game.gameboard.data[0][0], [3, 3])
        self.assertEqual(self.game.gameboard.data[1][1], [0, 0])
        self.assertIn([1, 1], self.game.moves_left_list.data)
        self.assertNotIn([0, 1], self.game.moves_left_list.data)
        # Test basic game fields
        self.assertEqual(self.game.name, "Test Game")
        self.assertEqual(self.game.player1.username, "player1")
        self.assertEqual(self.game.score_p1, 0)
        self.assertEqual(self.game.score_p2, 0)
        self.assertEqual(self.game.active_player, 1)
        self.assertTrue(self.game.using_special_stones, True)
        self.assertTrue(self.game.using_standard_scoring, True)
        self.assertFalse(self.game.game_over, False)
        self.assertIsNone(self.game.result)
        self.assertTrue(self.game.p1_has_thunder_stone, True)
        self.assertTrue(self.game.p2_has_thunder_stone, True)
        self.assertTrue(self.game.p1_has_woden_stone, True)
        self.assertTrue(self.game.p2_has_woden_stone, True)

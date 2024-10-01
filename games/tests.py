from django.contrib.auth import get_user_model
from django.test import TestCase

from .logic import game_rules
from .models import Game, GameBoard, PlayedMovesList, MovesLeftList


class GamesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
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

    @classmethod
    def tearDownClass(cls):
        cls.player1.delete()
        cls.player2.delete()

    def setUp(self):
        self.gameboard = GameBoard.objects.create()
        self.played_moves_list = PlayedMovesList.objects.create()
        self.moves_left_list = MovesLeftList.objects.create()

        self.game = Game.objects.create(
            name="Test Game",
            player1=self.player1,
            gameboard=self.gameboard,
            played_moves_list=self.played_moves_list,
            moves_left_list=self.moves_left_list,
        )
        self.game = game_rules.initialize_game(self.game)

        self.game.gameboard.data = [
            [[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3]],
            [[3, 3], [1, 1], [1, 1], [0, 0], [1, 1], [2, 1], [0, 0], [2, 1], [3, 3]],
            [[3, 3], [0, 0], [1, 1], [1, 1], [1, 1], [2, 1], [2, 1], [2, 1], [3, 3]],
            [[3, 3], [0, 0], [1, 1], [1, 1], [0, 0], [0, 0], [2, 1], [0, 0], [3, 3]],
            [[3, 3], [1, 1], [0, 0], [2, 2], [0, 0], [2, 1], [1, 1], [1, 1], [3, 3]],
            [[3, 3], [0, 0], [1, 1], [2, 1], [2, 1], [0, 0], [0, 0], [0, 0], [3, 3]],
            [[3, 3], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [0, 0], [0, 0], [3, 3]],
            [[3, 3], [2, 1], [2, 1], [0, 0], [1, 1], [2, 1], [1, 1], [0, 0], [3, 3]],
            [[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3]],
        ]

    def test_game_setup(self):
        # Test correct assignment of values when initializing with game_rules
        self.assertEqual(self.game.gameboard.data[0][0], [3, 3])
        self.assertEqual(self.game.gameboard.data[1][6], [0, 0])
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

    def test_find_adjacent(self):
        adjacent_positions = game_rules.find_adjacent(1, 1)
        self.assertEqual(adjacent_positions, [[0, 1], [1, 0], [1, 2], [2, 1]])

    def test_check_player_hinges(self):
        hinges = game_rules.check_player_hinges(
            gameboard=self.game.gameboard.data, row_number=1, col_number=3
        )
        self.assertEqual(hinges, True)
        hinges = game_rules.check_player_hinges(
            gameboard=self.game.gameboard.data, row_number=6, col_number=7
        )
        self.assertEqual(hinges, False)
        hinges = game_rules.check_player_hinges(
            gameboard=self.game.gameboard.data, row_number=6, col_number=7
        )
        self.assertEqual(hinges, False)
        hinges = game_rules.check_player_hinges(
            gameboard=self.game.gameboard.data, row_number=7, col_number=7
        )
        self.assertEqual(hinges, False)

    def test_hinge_check(self):
        hinges = game_rules.hinge_check(
            self.game.gameboard.data, row_number=1, col_number=1
        )
        self.assertEqual(hinges, 3)
        hinges = game_rules.hinge_check(
            self.game.gameboard.data, row_number=7, col_number=6
        )
        self.assertEqual(hinges, 2)
        hinges = game_rules.hinge_check(
            self.game.gameboard.data, row_number=4, col_number=5
        )
        self.assertEqual(hinges, 1)

    def test_check_adjacent_stones(self):
        position = game_rules.check_adjacent_stones(
            self.game.gameboard.data, row_number=5, col_number=6
        )
        self.assertEqual(position, True)
        position = game_rules.check_adjacent_stones(
            self.game.gameboard.data, row_number=6, col_number=5
        )
        self.assertEqual(position, True)
        position = game_rules.check_adjacent_stones(
            self.game.gameboard.data, row_number=3, col_number=1
        )
        self.assertEqual(position, False)

    def test_change_player(self):
        self.game = game_rules.change_player(self.game)
        self.assertEqual(self.game.active_player, 2)
        self.game = game_rules.change_player(self.game)
        self.assertEqual(self.game.active_player, 1)

    def test_check_default_stone(self):
        self.assertEqual(
            game_rules.check_default_stone(self.game.gameboard.data, row=10, col=6),
            False,
        )
        self.assertEqual(
            game_rules.check_default_stone(self.game.gameboard.data, row=1, col=1),
            False,
        )
        self.assertEqual(
            game_rules.check_default_stone(self.game.gameboard.data, row=3, col=7),
            False,
        )
        self.assertEqual(
            game_rules.check_default_stone(self.game.gameboard.data, row=5, col=6),
            False,
        )
        self.assertEqual(
            game_rules.check_default_stone(self.game.gameboard.data, row=6, col=7), True
        )

    def test_check_thunder_stone(self):
        self.assertEqual(
            game_rules.check_thunder_stone(self.game.gameboard.data, row=10, col=10),
            False,
        )
        self.assertEqual(
            game_rules.check_thunder_stone(self.game.gameboard.data, row=1, col=1),
            False,
        )
        self.assertEqual(
            game_rules.check_thunder_stone(self.game.gameboard.data, row=3, col=1), True
        )
        self.assertEqual(
            game_rules.check_thunder_stone(self.game.gameboard.data, row=3, col=7), True
        )

    def test_check_woden_stone(self):
        self.assertEqual(
            game_rules.check_woden_stone(
                self.game.gameboard.data, active_player=1, row=10, col=10
            ),
            False,
        )
        self.assertEqual(
            game_rules.check_woden_stone(
                self.game.gameboard.data, active_player=1, row=1, col=1
            ),
            False,
        )
        self.assertEqual(
            game_rules.check_woden_stone(
                self.game.gameboard.data, active_player=1, row=3, col=1
            ),
            False,
        )
        self.assertEqual(
            game_rules.check_woden_stone(
                self.game.gameboard.data, active_player=1, row=3, col=6
            ),
            True,
        )

    def test_is_valid_move(self):
        # Test standard stones
        self.assertTrue(
            game_rules.is_valid_move(self.game, played_stone=1, row=3, col=1), True
        )
        self.assertFalse(
            game_rules.is_valid_move(self.game, played_stone=1, row=1, col=6), False
        )
        # Test thunder stones
        self.assertTrue(
            game_rules.is_valid_move(self.game, played_stone=2, row=4, col=4), True
        )
        self.assertFalse(
            game_rules.is_valid_move(self.game, played_stone=2, row=2, col=5), False
        )
        # Test Woden stones
        self.assertTrue(
            game_rules.is_valid_move(self.game, played_stone=3, row=7, col=1), True
        )
        self.assertFalse(
            game_rules.is_valid_move(self.game, played_stone=3, row=7, col=3), False
        )

    def test_check_score(self):
        # test with default / standard scoring
        self.game.using_standard_scoring = True
        score_p1 = game_rules.check_score(self.game, 1)
        score_p2 = game_rules.check_score(self.game, 2)
        self.assertEqual(score_p1, 19)
        self.assertEqual(score_p2, 16)
        # test with simple scoring
        self.game.using_standard_scoring = False
        score_p1 = game_rules.check_score(self.game, 1)
        score_p2 = game_rules.check_score(self.game, 2)
        self.assertEqual(score_p1, 11)
        self.assertEqual(score_p2, 8)

    def test_possible_thunder_stone_moves(self):
        thunder_stone_moves = game_rules.possible_thunder_stone_moves(self.game)
        self.assertIn([1, 3], thunder_stone_moves)
        self.assertNotIn([4, 3], thunder_stone_moves)

    def test_possible_woden_stone_moves(self):
        woden_stone_moves = game_rules.possible_woden_stone_moves(self.game)
        self.assertIn([1, 5], woden_stone_moves)
        self.assertNotIn([4, 6], woden_stone_moves)

    def test_remaining_moves(self):
        self.assertEqual(
            game_rules.remaining_moves(self.game.gameboard.data),
            [[3, 1], [4, 4], [5, 1], [5, 5], [5, 7], [6, 6], [6, 7], [7, 7]],
        )

    def test_update_score(self):
        self.game.using_standard_scoring = True
        self.assertEqual(self.game.score_p1, 0)
        self.assertEqual(self.game.score_p2, 0)
        self.game = game_rules.update_score(self.game)
        self.assertEqual(self.game.score_p1, 19)
        self.assertEqual(self.game.score_p2, 16)

    def test_determine_winner(self):
        self.assertEqual(
            game_rules.determine_winner(score_p1=20, score_p2=15), "player 1"
        )
        self.assertEqual(
            game_rules.determine_winner(score_p1=15, score_p2=20), "player 2"
        )
        self.assertEqual(game_rules.determine_winner(score_p1=20, score_p2=20), "tie")
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=20, score_p2=15), "player 2"
        )
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=20, score_p2=15), "tie"
        )
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=15, score_p2=20), "player 1"
        )
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=15, score_p2=20), "tie"
        )
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=20, score_p2=20), "player 1"
        )
        self.assertNotEqual(
            game_rules.determine_winner(score_p1=20, score_p2=20), "player 2"
        )

    def test_thunder_attack(self):
        self.game.gameboard.data = game_rules.thunder_attack(
            self.game.gameboard.data, row=1, col=6
        )
        self.assertEqual(
            self.game.gameboard.data,
            [
                [
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [1, 1],
                    [1, 1],
                    [0, 0],
                    [1, 1],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [0, 0],
                    [1, 1],
                    [1, 1],
                    [1, 1],
                    [2, 1],
                    [0, 0],
                    [2, 1],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [0, 0],
                    [1, 1],
                    [1, 1],
                    [0, 0],
                    [0, 0],
                    [2, 1],
                    [0, 0],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [1, 1],
                    [0, 0],
                    [2, 2],
                    [0, 0],
                    [2, 1],
                    [1, 1],
                    [1, 1],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [0, 0],
                    [1, 1],
                    [2, 1],
                    [2, 1],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [0, 0],
                    [1, 1],
                    [0, 0],
                    [1, 1],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [2, 1],
                    [2, 1],
                    [0, 0],
                    [1, 1],
                    [2, 1],
                    [1, 1],
                    [0, 0],
                    [3, 3],
                ],
                [
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                    [3, 3],
                ],
            ],
        )

    # def test_assign_move(self):
    #     self.game.gameboard.data = self.GAMEBOARD_TEST_STATE
    #     self.game = game_rules.assign_move(self.game, active_stone=1, row=5, col=7)
    #     # self.assertEqual(self.game.gameboard.data[5][7], [1, 1])
    #     print(self.game.gameboard.data)

    def is_game_over(self):
        self.game.moves_left_list = MovesLeftList(
            game_rules.remaining_moves(self.game.gameboard.data)
        )
        game_rules.is_game_over(self.game)

    def test_player_must_pass(self):
        pass

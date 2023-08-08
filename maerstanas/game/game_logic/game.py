from .board import  Board
from .game_logic import remaining_moves


class Game:

    def __init__(self):
        self.board = Board()
        self.move_list = []
        self.moves_left = remaining_moves(self.board.data)
        self.score_p1 = 0
        self.score_p2 = 0
        self.result = ""
        self.active_player = 1

import secrets
import string

from games.logic import game_rules


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for i in range(length))
    return password


def play_computer_move(game_state):
    if not game_state.game_over and game_rules.player_must_pass(game_state):
        game_state = game_rules.pass_player_turn(game_state)
    else:
        comp_move = secrets.choice(game_state.moves_left_list)
        row, col = comp_move[0], comp_move[1]
        stone = 1
        game_state = game_rules.assign_move(game_state, stone, row, col)
        game_state.moves_left_list = game_rules.remaining_standard_moves(
            game_state.gameboard["data"]
        )
        game_state = game_rules.change_player(game_state)
        game_state.game_over = game_rules.is_game_over(game_state)
    return game_state

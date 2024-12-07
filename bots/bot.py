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
        match game_state.player2.username:
            case "Oswin":
                move = play_random_move(game_state)
            # placeholder for other bots
            # case "Aelfric":
            #     move = play_random_move(game_state)
            # placeholder for other bots
            # case "Aethelstan":
            #     move = play_random_move(game_state)
            case _:
                move = play_random_move(game_state)
        game_state = game_rules.assign_move(
            game_state, move["stone"], move["row"], move["col"]
        )
        game_state.moves_left_list = game_rules.remaining_standard_moves(
            game_state.gameboard["data"]
        )
        game_state = game_rules.change_player(game_state)
        game_state.game_over = game_rules.is_game_over(game_state)
    return game_state


def play_random_move(game_state):
    comp_move = secrets.choice(game_state.moves_left_list)
    move = {"row": comp_move[0], "col": comp_move[1], "stone": 1}
    return move

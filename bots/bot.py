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
    moves = get_available_moves(game_state)
    comp_move = secrets.choice(moves["possible"])
    if comp_move in moves["woden"] and comp_move not in moves["standard"]:
        stone = 3
    elif comp_move in moves["thunder"] and comp_move not in moves["standard"]:
        stone = 2
    else:
        stone = 1
    move = {"row": comp_move[0], "col": comp_move[1], "stone": stone}
    return move


def possible_thunder_stone_moves(board):
    possible_moves = []
    for row in range(1, 9):
        for col in range(1, 9):
            if game_rules.check_thunder_stone(board, row, col):
                possible_moves.append([row, col])
    return possible_moves


def possible_woden_stone_moves(board, active_player):
    possible_moves = []
    for row in range(1, 9):
        for col in range(1, 9):
            if game_rules.check_woden_stone(board, active_player, row, col):
                possible_moves.append([row, col])
    return possible_moves


def get_available_moves(temp_game):
    board = temp_game.gameboard["data"]
    active_player = temp_game.active_player
    standard_moves = temp_game.moves_left_list
    thunder_moves = []
    woden_moves = []
    player_has_thunder_stone = "p" + str(active_player) + "_has_thunder_stone"
    if getattr(temp_game, player_has_thunder_stone, False):
        thunder_moves.append(possible_thunder_stone_moves(board))
    player_has_woden_stone = "p" + str(active_player) + "_has_woden_stone"
    if getattr(temp_game, player_has_woden_stone, False):
        woden_moves.append(possible_woden_stone_moves(board, active_player))
    thunder_moves = [item for sublist in thunder_moves for item in sublist]
    woden_moves = [item for sublist in woden_moves for item in sublist]
    possible_moves = standard_moves + thunder_moves + woden_moves
    moves = {
        "standard": standard_moves,
        "thunder": thunder_moves,
        "woden": woden_moves,
        "possible": possible_moves,
    }
    return moves

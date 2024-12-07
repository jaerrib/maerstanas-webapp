import secrets
import string
from copy import deepcopy

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
            case "Aelfric":
                move = get_best_move(game_state)
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


def get_best_move(game_state, sim_num=10, depth=49):
    temp_game = deepcopy(game_state)
    # Using -100000 simply ensures that losses and ties are scored
    # better than the initial assignment
    best_score = -100000
    players = ["Computer", "Computer"]
    for x in range(0, sim_num):
        returned_score, first_stone, first_row, first_col = sim_game_loop(
            temp_game, players, depth
        )
        if returned_score >= best_score:
            best_score = returned_score
            best_row = first_row
            best_col = first_col
            best_stone = first_stone
    move = {"row": best_row, "col": best_col, "stone": best_stone}
    return move


def sim_game_loop(data, players, depth):
    temp_game = deepcopy(data)
    comparison_player = deepcopy(temp_game.active_player)
    active_player = 3 - temp_game.active_player
    first_move = True
    moves = get_available_moves(temp_game)
    depth_counter = min(depth, len(moves["possible"]))
    while depth_counter >= 1:
        if players[active_player - 1] == "Computer":
            if not game_rules.is_game_over(
                    temp_game
            ) and not game_rules.player_must_pass(temp_game):
                moves = get_available_moves(temp_game)
                if len(moves["possible"]) >= 1:
                    ai_stone, ai_row, ai_col = weighted_computer_move(temp_game)
                if first_move:
                    first_row = ai_row
                    first_col = ai_col
                    first_stone = ai_stone
                    first_move = False
                temp_game = game_rules.assign_move(temp_game, ai_stone, ai_row,
                                                   ai_col)
            if game_rules.player_must_pass(temp_game):
                change_player(temp_game)
        depth_counter -= 1

    temp_game.result = game_rules.determine_winner(
        temp_game.score_p1, temp_game.score_p2
    )
    if comparison_player == 1:
        weighted_score = assign_result_value(temp_game)
    else:
        weighted_score = -(assign_result_value(temp_game))
    return weighted_score, first_stone, first_row, first_col


def weighted_computer_move(temp_game):
    moves = assign_weights(get_available_moves(temp_game), temp_game)
    max_weight = -100000
    move_choices = []
    for move in moves["standard"]:
        if move[2] > max_weight:
            max_weight = move[0]
            move_choices.append(move)
    for move in moves["woden"]:
        if move[2] > max_weight:
            max_weight = move[2]
            move_choices.append(move)
    for move in moves["thunder"]:
        if move[2] > max_weight:
            max_weight = move[2]
            move_choices.append(move)
    comp_move = secrets.choice(move_choices)
    row, col = comp_move[0], comp_move[1]
    if comp_move in moves["woden"] and comp_move not in moves["standard"]:
        stone = 3
    elif comp_move in moves["thunder"] and comp_move not in moves["standard"]:
        stone = 2
    else:
        stone = 1
    return stone, row, col


def edge_hinge_count(move, board):
    row, col = move[0], move[1]
    adjacent_positions = find_adjacent(row, col)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = board[row_to_check][col_to_check]
        if position_check[0] == 3:
            hinges += 1
    return hinges


def is_corner(move, board):
    return edge_hinge_count(move, board) == 2


def is_edge(move, board):
    return edge_hinge_count(move, board) == 1


def hinges_created(move, board, active_player):
    row, col = move[0], move[1]
    adjacent_positions = find_adjacent(row, col)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = board[row_to_check][col_to_check]
        if position_check[0] == active_player:
            hinges += 1
    return hinges


def stones_blocked(move, board, active_player):
    row, col = move[0], move[1]
    adjacent_positions = find_adjacent(row, col)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = board[row_to_check][col_to_check]
        if position_check[0] == 3 - active_player:
            hinges += 1
    return hinges


def stones_removed(move, board, active_player):
    friendly = 0
    opponent = 0
    row, col = move[0], move[1]
    adjacent_positions = find_adjacent(row, col)
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = board[row_to_check][col_to_check]
        if position_check[0] == active_player:
            friendly += 1
        if position_check[0] == 3 - active_player:
            opponent += 1
    return friendly, opponent


def assign_weights(move_dict, temp_game):
    personality = {
        "corner_weight": 8,
        "edge_weight": 4,
        "scoring": 3,
        "blocking": 1,
        "woden": 1,
        "thunder": 2,
        "sacrifice": 1,
    }
    board = temp_game.gameboard["data"]
    active_player = temp_game.active_player
    for move in move_dict["standard"]:
        weight = 0
        if is_corner(move, board):
            weight += personality["corner_weight"]
        elif is_edge(move, board):
            weight += personality["edge_weight"]
        weight += personality["scoring"] * hinges_created(move, board,
                                                          active_player)
        weight += personality["blocking"] * stones_blocked(move, board,
                                                           active_player)
        move.append(weight)

    for move in move_dict["woden"]:
        weight = 0
        if is_corner(move, board):
            weight += personality["corner_weight"]
        elif is_edge(move, board):
            weight += personality["edge_weight"]
        weight += personality["scoring"] * hinges_created(move, board,
                                                          active_player)
        weight += personality["blocking"] * stones_blocked(move, board,
                                                           active_player)
        weight += personality["woden"]
        move.append(weight)

    for move in move_dict["thunder"]:
        weight = 0
        if is_corner(move, board):
            weight += personality["corner_weight"]
        elif is_edge(move, board):
            weight += personality["edge_weight"]
        friendly_stones, opponent_stones = stones_removed(move, board,
                                                          active_player)
        weight += personality["thunder"]
        if friendly_stones + opponent_stones != 0:
            weight += (personality["sacrifice"] * friendly_stones) - (
                    personality["sacrifice"] * opponent_stones
            )
        move.append(weight)
    return move_dict


def assign_result_value(current_game):
    game_value = 0
    score_p1 = game_rules.check_score(game_state=current_game, player=1)
    score_p2 = game_rules.check_score(game_state=current_game, player=2)
    if current_game.result == "tie":
        game_value = 1
    elif current_game.result == "player 1":
        game_value = 4
    elif current_game.result == "player 2":
        game_value = -2
    difference = abs(score_p1 - score_p2)
    adjustment = 48 - len(current_game.moves_left_list)
    game_value = game_value * difference * adjustment
    return game_value


def change_player(data):
    data.active_player = 3 - data.active_player
    return data


def find_adjacent(row_number, col_number):
    """
    Returns a list of positions adjacent to a given board position.
    """
    return [
        [row_number - 1, col_number],
        [row_number, col_number - 1],
        [row_number, col_number + 1],
        [row_number + 1, col_number],
    ]

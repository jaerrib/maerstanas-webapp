from copy import deepcopy
from .game_logic import remaining_moves,assign_move, determine_winner, check_score
import secrets


def assign_result_value(current_game):
    game_value = 0
    score_p1 = check_score(current_game["board"], player=1)
    score_p2 = check_score(current_game["board"], player=2)
    if current_game["result"] == "tie":
        game_value = 1
    elif current_game["result"] == "player 1":
        game_value = 4
    elif current_game["result"] == "player 2":
        game_value = -2
    difference = abs(score_p1 - score_p2)
    adjustment = 48 - len(current_game["move_list"])
    game_value = game_value * difference * adjustment
    return game_value


def computer_move(moves_left):
    comp_move = secrets.choice(moves_left)
    row, col = comp_move[0], comp_move[1]
    return row, col


def sim_game_loop(data, players, depth):
    temp_game = deepcopy(data)
    comparison_player = deepcopy(temp_game["active_player"])
    if temp_game["active_player"] == 1:
        active_player = 1
    else:
        active_player = 2
    first_move = True
    temp_game["moves_left"] = remaining_moves(temp_game["board"])
    depth_counter = min(depth, len(temp_game["moves_left"]))
    while depth_counter >= 1:
        if players[active_player - 1] == "Computer":
            if len(temp_game["moves_left"]) >= 1:
                ai_row, ai_col = computer_move(temp_game["moves_left"])
                if first_move:
                    first_row = ai_row
                    first_col = ai_col
                    first_move = False
        temp_game = assign_move(temp_game, ai_row, ai_col)
        depth_counter -= 1

    temp_game["result"] = determine_winner(temp_game["score_p1"], temp_game["score_p2"])
    if comparison_player == 1:
        weighted_score = assign_result_value(temp_game)
    else:
        weighted_score = -(assign_result_value(temp_game))
    return weighted_score, first_row, first_col


def get_best_move(data, sim_num, depth):
    temp_game = deepcopy(data)
    # Using -1000 simply ensures that losses and ties are scored
    # better than the initial assignment
    best_score = -1000
    players = ["Computer", "Computer"]

    for x in range(0, sim_num):
        returned_score, first_row, first_col = sim_game_loop(temp_game,
                                                             players,
                                                             depth)
        if returned_score >= best_score:
            best_score = returned_score
            best_row = first_row
            best_col = first_col
    print(best_score)
    return best_row, best_col
def convert_num_to_row(num):
    rows = ["A", "B", "C", "D", "E", "F", "G"]
    return rows[num - 1]


def find_adjacent(row_number, col_number):
    """
    Returns assigned value for positions adjacent to a given board position
    """
    adjacent_positions = [
        [row_number - 1, col_number],
        [row_number, col_number - 1],
        [row_number, col_number + 1],
        [row_number + 1, col_number]
    ]
    return adjacent_positions


def check_player_hinges(data, row_number, col_number):
    """
    Evaluates the number of hinges a player move would have
    if played at a given board position
    """
    adjacent_positions = find_adjacent(row_number, col_number)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = data[row_to_check][col_to_check]
        if position_check != 0:
            hinges += 1
    if hinges > 3:
        return True
    else:
        return False


def hinge_check(data, row_number, col_number):
    """
    Counts the number of hinges a stone at a given position has
    """
    adjacent_positions = find_adjacent(row_number, col_number)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = data[row_to_check][col_to_check]
        if position_check == 3:
            hinges += 1
        elif position_check == 1 or position_check == 2:
            hinges += 1
    return hinges


def check_adjacent_stones(data, row_number, col_number):
    """
    Determines if a move made at a given board position would cause any
    adjacent stones to have more than 3 hinges. Edge and empty/vacant board
    positions are ignored as they would zero hinges.
    """
    adjacent_positions = find_adjacent(row_number, col_number)
    # Counts the number of hinges each adjacent stone has
    # Open (value 0) and edge (value 3) positions are ignored
    for i in range(0, len(adjacent_positions)):
        row_position = int(adjacent_positions[i][0])
        col_position = int(adjacent_positions[i][1])
        board_value = data[row_position][col_position]
        if board_value == 3 or board_value == 0:
            pass
        elif board_value == 1 or board_value == 2:
            if hinge_check(data, row_position, col_position) >= 3:
                return True
    return False


def change_player(game):
    if game.active_player == 1:
        game.active_player = 2
    elif game.active_player == 2:
        game.active_player = 1
    return game


def change_guest_player(guest_game):
    if guest_game["active_player"] == 1:
        guest_game["active_player"] = 2
    elif guest_game["active_player"] == 2:
        guest_game["active_player"] = 1
    return guest_game


def valid_move(data, row, col):
    """
    Determines if a potential move would be valid by doing the following:
    (1) Checking if the coordinates are within the confines of the board
    (2) Checking if the position is occupied
    (3) Checking if the move would create 4 immediate hinges
    (4) Checking if the move would cause any adjacent stones to have more
    than 3 hinges
    """
    if 1 <= row < 9 and 1 <= col < 9:
        player_move = data[row][col]
    else:
        # Invalid move - outside board confines
        return False
    if player_move != 0:
        # Invalid move - space occupied
        return False
    else:
        if check_player_hinges(data, row, col):
            # Invalid move - move would cause 4 immediate hinges
            return False
        elif check_adjacent_stones(data, row, col):
            # Invalid move - an adjacent stone would have 4 hinges
            return False
        else:
            return True


def check_score(data, player):
    """
    Evaluates the score of current board positions, first looping through the
    vertical hinges then the horizontal ones.
    """
    calculated_score: int = 0

    for row_index in range(1, 9):
        for col_index in range(0, 9):
            board_position = data[row_index][col_index]
            comparison_position = data[row_index - 1][col_index]
            if comparison_position == player \
                    and board_position == player:
                calculated_score += 1
            elif comparison_position == 3 and board_position == player:
                calculated_score += 1
            elif board_position == 3 and comparison_position == player:
                calculated_score += 1

    for row_index in range(1, 9):
        for col_index in range(0, 9):
            board_position = data[row_index][col_index]
            comparison_position = data[row_index][col_index - 1]
            if comparison_position == player \
                    and board_position == player:
                calculated_score += 1
            elif comparison_position == 3 and board_position == player:
                calculated_score += 1
            elif board_position == 3 and comparison_position == player:
                calculated_score += 1
    return calculated_score


def viable_moves(data):
    """
    Cycles through board positions starting at A1 (1,1). If a position is
    valid, viable_moves is True and play is allowed to continue. If a
    position is not valid, the next position is assessed until the entire
    board has been checked.
    """
    for row_index in range(1, 9):
        for col_index in range(1, 9):
            if data[row_index][col_index] != 0:
                pass
            else:
                if check_player_hinges(data, row_index, col_index):
                    pass
                elif check_adjacent_stones(data, row_index, col_index):
                    pass
                else:
                    return True


def remaining_moves(data):
    """
    Cycles through board positions starting at A1 (1,1). If a position is
    a potentially valid move, it is appended to an array which is then used
    when the pseudo AI randomly selects its move.
    """
    possible_moves = []
    for row_index in range(1, 9):
        for col_index in range(1, 9):
            if data[row_index][col_index] != 0:
                pass
            else:
                if check_player_hinges(data, row_index, col_index):
                    pass
                elif check_adjacent_stones(data, row_index, col_index):
                    pass
                else:
                    possible_moves.append([row_index, col_index])
    return possible_moves


def update_score(game):
    game.score_p1 = check_score(game.board.data, player=1)
    game.score_p2 = check_score(game.board.data, player=2)
    return game


def update_guest_score(guest_game):
    guest_game["score_p1"] = check_score(guest_game["board"], player=1)
    guest_game["score_p2"] = check_score(guest_game["board"], player=2)
    return guest_game


def determine_winner(score_p1, score_p2):
    if score_p1 == score_p2:
        result = "tie"
    elif score_p1 > score_p2:
        result = "player 1"
    else:
        result = "player 2"
    return result


def assign_move(game, row, col):
    game.board.data[row][col] = game.active_player
    game.move_list.append(
        (len(game.move_list) + 1,
            game.active_player,
            convert_num_to_row(col)+str(row)
         ))
    game = update_score(game)
    game = change_player(game)
    game.moves_left = remaining_moves(game.board.data)
    return game


def assign_guest_move(guest_game, row, col):
    guest_game["board"][row][col] = guest_game["active_player"]
    guest_game["move_list"].append(
        (len(guest_game["move_list"]) + 1,
            guest_game["active_player"],
            convert_num_to_row(col)+str(row)
         ))
    guest_game = update_guest_score(guest_game)
    guest_game = change_guest_player(guest_game)
    guest_game["moves_left"] = remaining_moves(guest_game["board"])
    return guest_game

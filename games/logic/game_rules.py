def initialize_game(game_state):
    SIZE = 9
    EMPTY = [0, 0]
    EDGE = [3, 3]

    game_state.gameboard["data"] = [[EMPTY] * SIZE for _ in range(SIZE)]
    for col_num in range(SIZE):
        game_state.gameboard["data"][0][col_num] = EDGE
        game_state.gameboard["data"][8][col_num] = EDGE
    for row_num in range(1, SIZE - 1):
        game_state.gameboard["data"][row_num][0] = EDGE
        game_state.gameboard["data"][row_num][8] = EDGE

    game_state.played_moves_list["data"] = []
    game_state.moves_left_list["data"] = remaining_standard_moves(
        game_state.gameboard["data"]
    )

    return game_state


def convert_num_to_row(num):
    return chr(ord("A") + num - 1)


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


def check_player_hinges(gameboard, row_number, col_number):
    """
    Evaluates the number of hinges a player move would have
    if played at a given board position
    """
    adjacent_positions = find_adjacent(row_number, col_number)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = gameboard[row_to_check][col_to_check]
        if position_check[0] != 0:
            hinges += 1
    if hinges > 3:
        return True
    else:
        return False


def hinge_check(gameboard, row_number, col_number):
    """
    Counts the number of hinges a stone at a given position has
    """
    adjacent_positions = find_adjacent(row_number, col_number)
    hinges = 0
    for position in range(0, len(adjacent_positions)):
        row_to_check = adjacent_positions[position][0]
        col_to_check = adjacent_positions[position][1]
        position_check = gameboard[row_to_check][col_to_check]
        if position_check[0] in [1, 2, 3]:
            hinges += 1
    return hinges


def check_adjacent_stones(gameboard, row_number, col_number):
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
        board_value = gameboard[row_position][col_position]
        if (
            board_value[0] in [1, 2]
            and hinge_check(gameboard, row_position, col_position) >= 3
        ):
            return True
    return False


def change_player(game_state):
    game_state.active_player = 3 - game_state.active_player
    return game_state


def check_default_stone(gameboard, row, col):
    """
    Determines if a potential move would be valid by doing the following:
    (1) Checking if the coordinates are within the confines of the board
    (2) Checking if the position is occupied
    (3) Checking if the move would create 4 immediate hinges
    (4) Checking if the move would cause any adjacent stones to have more
        than 3 hinges
    """
    if not (1 <= row < 9 and 1 <= col < 9):
        # Invalid move - outside board confines
        return False

    player_move = gameboard[row][col]
    if player_move[0] != 0:
        # Invalid move - space occupied
        return False

    if check_player_hinges(gameboard, row, col) or check_adjacent_stones(
        gameboard, row, col
    ):
        # Invalid move - either 4 immediate hinges or adjacent stone with 4 hinges
        return False

    return True


def check_thunder_stone(gameboard, row, col):
    """
    Determines if a potential move would be valid by doing the following:
    (1) Checking if the coordinates are within the confines of the board
    (2) Checking if the position is occupied
    """
    if 1 <= row < 9 and 1 <= col < 9:
        player_move = gameboard[row][col]
    else:
        # Invalid move - outside board confines
        return False
    # Return if the chosen space is occupied
    return player_move[0] == 0


def check_woden_stone(gameboard, active_player, row, col):
    """
    Determines if a potential move would be valid by doing the following:
    (1) Checking if the coordinates are within the confines of the board
    (2) Checking if the position is occupied by an opponent's stone
    """
    if 1 <= row < 8 and 1 <= col < 8:
        player_move = gameboard[row][col]
    else:
        # Invalid move - outside board confines
        return False
    # Return if the chosen space is occupied by opponent's stone
    return player_move[1] != 0 and player_move[0] != active_player


def is_valid_move(game_state, played_stone, row, col):
    match played_stone:
        case 1:
            return check_default_stone(game_state.gameboard["data"], row, col)
        case 2:
            return check_thunder_stone(game_state.gameboard["data"], row, col)
        case 3:
            return check_woden_stone(
                game_state.gameboard["data"], game_state.active_player, row, col
            )


def check_score(game_state, player):
    """
    Evaluates the score of current board positions, first looping through the
    vertical hinges then the horizontal ones.
    """
    score_modifier = 1 if game_state.using_standard_scoring else 0
    calculated_score: int = 0
    for row_index in range(1, 9):
        for col_index in range(0, 9):
            board_position = game_state.gameboard["data"][row_index][col_index]
            # Check vertical hinges
            position_above = game_state.gameboard["data"][row_index - 1][col_index]
            if position_above[0] == player and board_position[0] == player:
                calculated_score += 1
            elif position_above[0] == 3 and board_position[0] == player:
                calculated_score += score_modifier
            elif position_above[0] == player and board_position[0] == 3:
                calculated_score += score_modifier
            # Check horizontal hinges
            position_to_left = game_state.gameboard["data"][row_index][col_index - 1]
            if position_to_left[0] == player and board_position[0] == player:
                calculated_score += 1
            elif position_to_left[0] == 3 and board_position[0] == player:
                calculated_score += score_modifier
            elif position_to_left[0] == player and board_position[0] == 3:
                calculated_score += score_modifier
    return calculated_score


def possible_thunder_stone_moves(game_state):
    possible_moves = []
    for row in range(1, 9):
        for col in range(1, 9):
            if check_thunder_stone(game_state.gameboard["data"], row, col):
                possible_moves.append([row, col])
    return possible_moves


def possible_woden_stone_moves(game_state):
    possible_moves = []
    for row in range(1, 9):
        for col in range(1, 9):
            if check_woden_stone(
                game_state.gameboard["data"], game_state.active_player, row, col
            ):
                possible_moves.append([row, col])
    return possible_moves


def remaining_standard_moves(gameboard):
    """
    Cycles through board positions starting at A1 (1,1). If a position is
    a potentially valid move, it is appended to an array which is then used
    when the pseudo AI randomly selects its move.
    """
    possible_moves = []
    for row_index in range(1, 9):
        for col_index in range(1, 9):
            if gameboard[row_index][col_index][0] != 0:
                pass
            else:
                if check_player_hinges(gameboard, row_index, col_index):
                    pass
                elif check_adjacent_stones(gameboard, row_index, col_index):
                    pass
                else:
                    possible_moves.append([row_index, col_index])
    return possible_moves


def update_score(game_state):
    game_state.score_p1 = check_score(game_state, player=1)
    game_state.score_p2 = check_score(game_state, player=2)
    return game_state


def determine_winner(score_p1, score_p2):
    if score_p1 == score_p2:
        result = "tie"
    elif score_p1 > score_p2:
        result = "player 1"
    else:
        result = "player 2"
    return result


def thunder_attack(gameboard, row, col):
    adjacent_positions = find_adjacent(row, col)
    for position in adjacent_positions:
        if gameboard[position[0]][position[1]] != [3, 3]:
            gameboard[position[0]][position[1]] = [0, 0]
    return gameboard


def assign_move(game_state, active_stone, row, col):
    if active_stone == 2:
        thunder_attack(game_state.gameboard["data"], row, col)
    if active_stone == 2:
        field_name = f"p{game_state.active_player}_has_thunder_stone"
        setattr(game_state, field_name, False)
    elif active_stone == 3:
        field_name = f"p{game_state.active_player}_has_woden_stone"
        setattr(game_state, field_name, False)
    game_state.gameboard["data"][row][col] = [game_state.active_player, active_stone]
    stones = ["standard stone", "thunder-stone", "Woden-stone"]
    played_stone = stones[active_stone - 1]
    game_state.played_moves_list["data"].append(
        (
            game_state.active_player,
            convert_num_to_row(row) + str(col) + " - " + played_stone,
        )
    )
    return game_state


def is_game_over(game_state):
    player1_has_special_stones = (
        game_state.p1_has_thunder_stone or game_state.p1_has_woden_stone
    )
    player2_has_special_stones = (
        game_state.p2_has_thunder_stone or game_state.p2_has_woden_stone
    )
    default_moves_are_left = game_state.moves_left_list["data"] != []
    return (
        not player1_has_special_stones
        and not player2_has_special_stones
        and not default_moves_are_left
    )


def player_must_pass(game_state):
    thunder_field = f"p{game_state.active_player}_has_thunder_stone"
    has_thunder_stone = getattr(game_state, thunder_field)
    woden_field = f"p{game_state.active_player}_has_woden_stone"
    has_woden_stone = getattr(game_state, woden_field)
    must_pass = (
        not (has_thunder_stone and has_woden_stone)
        and game_state.moves_left_list["data"] == []
    )
    return must_pass

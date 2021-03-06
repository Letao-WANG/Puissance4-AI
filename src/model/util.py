import math
from board import *

INFINITY = math.inf


def rollout_policy(possible_moves):
    """
    :param possible_moves:
    :return: choose randomly a move
    """
    return possible_moves[np.random.randint(len(possible_moves))]


def rollout(board):
    """
    Get the result of current Board
    :return: the result of board, 1, -1, 0 or None
    """
    current_rollout_board = board
    while not current_rollout_board.is_game_over():
        possible_moves = current_rollout_board.get_legal_actions()
        action = rollout_policy(possible_moves)
        current_rollout_board = current_rollout_board.move(action)
    return current_rollout_board.game_result


def get_next_move(board):
    """
    get the next best action (Move)
    :param board: class Board
    :return: class Move
    """
    return alpha_beta_search(board)


def heuristic(board):
    """
    Evaluate function 1, judge the situation of board
    :param board: class Board
    :return: the possibility of winning for the player who just finished its (or his, her) turn
    """
    win_count = 0
    for _ in range(100):
        result = rollout(board)
        if result == 1:
            win_count += 1
    return win_count / 100.0


def heuristic2(board):
    """
    Evaluate function 2, judge the situation of board
    :param board: class Board
    :return: general score
    """
    horizontal_score = 0
    vertical_score = 0
    diagonal1_score = 0
    diagonal2_score = 0

    # Vertical
    # Check each column for vertical score
    #
    # 3 possible situations per column
    #  0  1  2  3  4  5  6
    # [x][ ][ ][ ][ ][ ][ ] 0
    # [x][x][ ][ ][ ][ ][ ] 1
    # [x][x][x][ ][ ][ ][ ] 2
    # [x][x][x][ ][ ][ ][ ] 3
    # [ ][x][x][ ][ ][ ][ ] 4
    # [ ][ ][x][ ][ ][ ][ ] 5

    for row in range(board.row - 3):
        for column in range(board.col):
            score = score_position(board, row, column, 1, 0)
            vertical_score += score

        # Horizontal
        # Check each row's score
        #
        # 4 possible situations per row
        #  0  1  2  3  4  5  6
        # [x][x][x][x][ ][ ][ ] 0
        # [ ][x][x][x][x][ ][ ] 1
        # [ ][ ][x][x][x][x][ ] 2
        # [ ][ ][ ][x][x][x][x] 3
        # [ ][ ][ ][ ][ ][ ][ ] 4
        # [ ][ ][ ][ ][ ][ ][ ] 5

    for row in range(board.row):
        for column in range(board.col - 3):
            score = score_position(board, row, column, 0, 1)
            horizontal_score += score

    # Diagonal points 1 (negative-slope)
    #
    #
    #  0  1  2  3  4  5  6
    # [x][ ][ ][ ][ ][ ][ ] 0
    # [ ][x][ ][ ][ ][ ][ ] 1
    # [ ][ ][x][ ][ ][ ][ ] 2
    # [ ][ ][ ][x][ ][ ][ ] 3
    # [ ][ ][ ][ ][ ][ ][ ] 4
    # [ ][ ][ ][ ][ ][ ][ ] 5

    for row in range(board.row - 3):
        for column in range(board.col - 3):
            score = score_position(board, row, column, 1, 1)
            diagonal1_score += score

        # Diagonal points 2 (positive slope)
        #
        #
        #  0  1  2  3  4  5  6
        # [ ][ ][ ][x][ ][ ][ ] 0
        # [ ][ ][x][ ][ ][ ][ ] 1
        # [ ][x][ ][ ][ ][ ][ ] 2
        # [x][ ][ ][ ][ ][ ][ ] 3
        # [ ][ ][ ][ ][ ][ ][ ] 4
        # [ ][ ][ ][ ][ ][ ][ ] 5

    for row in range(3, board.row):
        for column in range(board.col - 3):
            score = score_position(board, row, column, -1, 1)
            diagonal2_score += score

    return horizontal_score + vertical_score + diagonal1_score + diagonal2_score


def score_position(board, row, column, delta_row, delta_col):
    """
    Heuristic evaluation for current state +1000, +100, +10, +1 for
    4-,3-,2-,1-in-a-line for AI player -1000, -100,
    -10, -1 for 4-,3-,2-,1-in-a-line for human player 0 otherwise
    """

    human_score = 0
    ai_score = 0
    human_points = 0
    ai_points = 0
    for i in range(4):
        current_chip = board.get_chip(row, column)
        if current_chip == board.x:  # if current chip is AI
            ai_points += 1
        elif current_chip == board.o:  # player chip
            human_points += 1
        # empty otherwise
        row += delta_row
        column += delta_col

    if human_points == 1:
        human_score = -1  # -1 point
    elif human_points == 2:
        human_score = -10  # -10 points
    elif human_points == 3:
        human_score = -100  # -100 points
    elif human_points == 4:
        human_score = -1000  # -1000 points
    # otherwise

    if ai_points == 1:
        ai_score = 1  # 1 point
    elif ai_points == 2:
        ai_score = 10  # 10 points
    elif ai_points == 3:
        ai_score = 100  # 100 points
    elif ai_points == 4:
        ai_score = 1000  # 1000 points
    # otherwise
    return human_score + ai_score


def alpha_beta_search(board):
    """
    Gives the best move that leads to the best minmax value = best value possible against the best move of the enemy
    Because max will choose the biggest value and min the smallest value, we don't have to visit all the branches. We
    can cut some of them that are never going to be chosen L'??lagage alpha beta n'affecte pas le r??sultat final
    Args:
        board: current state of the game for the current player

    Returns: the possible action from the current state that maximizes min_value along the path to state
    """
    board.current_depth = 0  # initialise the depth of the current node that we are visiting
    scores = []
    best_action = None
    v = -INFINITY
    alpha = -INFINITY
    beta = INFINITY
    maxi_value = -INFINITY
    actions = board.get_legal_actions()
    for action in actions:
        board.move2(action)  # add the chip
        v = min_value(board, alpha, beta)
        scores.append(v)
        if v > maxi_value:
            best_action = action
            maxi_value = v
            alpha = max(alpha, maxi_value)
        board.current_depth -= 1  # go back to the parent
        board.remove_chip(action.x_coor, action.y_coor)  # remove the chip
    if len(scores) == 1:
        best_action = actions[0]
    return best_action


def max_value(board, alpha, beta):
    """
        Gives an utility score
        Args:
            board: current state of the game for the current player
            alpha: value of the best alternative for max along the path to state
            beta: value of the best alternative for min along the path to state

        Returns: the biggest utility score

        """
    board.current_depth += 1
    # all the actions possibles from the current state
    actions = board.get_legal_actions()
    if not actions or board.current_depth >= board.depth:  # if list of next moves is empty or reached max depth
        score = heuristic2(board)  # predict the utility of one branch that we cannot develop
        return score
    else:
        v = -INFINITY
        for action in actions:
            board.move2(action)  # add the chip
            v = max(v, min_value(board, alpha, beta))
            if v >= beta:
                board.current_depth -= 1  # go back to the parent
                board.remove_chip(action.x_coor, action.y_coor)  # remove the chip we added to simulate it's utility
                return v
            alpha = max(v, alpha)
            board.current_depth -= 1  # go back to the parent
            board.remove_chip(action.x_coor, action.y_coor)  # remove the chip we added to simulate it's utility
        return v


def min_value(board, alpha, beta):
    """
    Gives an utility score
    Args:
        board: current state of the game for the current player
        alpha: value of the best alternative for max along the path to state
        beta: value of the best alternative for min along the path to state

    Returns: the smallest utility score

    """
    board.current_depth += 1
    # all the actions possibles from the current state
    actions = board.get_legal_actions()
    if not actions or board.current_depth >= board.depth:  # if list of next moves is empty or reached max depth
        score = heuristic2(board)  # predict the utility of one branch that we cannot develop
        return score
    else:
        v = INFINITY
        for action in actions:
            board.move2(action)  # add the chip
            v = min(v, max_value(board, alpha, beta))
            if v <= alpha:
                board.current_depth -= 1
                board.remove_chip(action.x_coor, action.y_coor)  # remove the chip we added to simulate it's utility
                return v
            beta = min(v, beta)
            board.current_depth -= 1
            board.remove_chip(action.x_coor, action.y_coor)  # remove the chip we added to simulate it's utility
        return v

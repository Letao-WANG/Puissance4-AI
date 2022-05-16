import numpy as np

from move import Move


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


def heuristic(board):
    """
    Evaluate function, judge the situation of board
    :param board: class Board
    :return: the possibility of winning for the player who just finished its (or his, her) turn
    """
    win_count = 0
    for _ in range(100):
        result = rollout(board)
        if result == 1:
            win_count += 1
    return win_count/100.0


def get_next_move(board):
    can_add, row = board.can_add_chip(int(0))
    move = Move(row, int(0), board.next_to_move)
    return move

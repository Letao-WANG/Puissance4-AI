import numpy as np


def rollout_policy(possible_moves):
    return possible_moves[np.random.randint(len(possible_moves))]


def rollout(board):
    """
    Get the result of current Board of Node
    :return: the result of board, 1, -1, 0 or None
    """
    current_rollout_board = board
    while not current_rollout_board.is_game_over():
        possible_moves = current_rollout_board.get_legal_actions()
        action = rollout_policy(possible_moves)
        current_rollout_board = current_rollout_board.move(action)
    return current_rollout_board.game_result

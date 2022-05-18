import numpy as np
import sys
import os

root_dir = os.getcwd().replace("controller", "")
sys.path.append(root_dir + "controller")
sys.path.append(root_dir + "model")
sys.path.append(root_dir + "view")

from board import Board
from graphics import get_action, graphics, judge


if __name__ == "__main__":

    # Initialization
    init_state = np.zeros((6, 7))
    board = Board(state=init_state, next_to_move=1)

    # Play round
    while not board.game_result:
        graphics(board.state)
        move = get_action(board)
        board = board.move(move)

        if judge(board) == 1:
            break

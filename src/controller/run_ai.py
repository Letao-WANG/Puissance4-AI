import numpy as np
import sys
import os

root_dir = os.getcwd().replace("controller", "")
sys.path.append(root_dir + "controller")
sys.path.append(root_dir + "model")
sys.path.append(root_dir + "view")

from board import Board
from util import get_next_move
from graphics import get_action, graphics, judge

if __name__ == "__main__":
    init_state = np.zeros((6, 7))
    board = Board(state=init_state, next_to_move=-1)

    while True:
        try:
            level = int(input("Enter difficulty from 1(easy) to 3(difficult) : "))
            if level > 3 or level < 1:
                raise ValueError
            break
        except ValueError:
            print("Entrez un entier entre 1 et 3")

    board.set_difficulty(level*2)

    while not board.game_result:
        # human part
        graphics(board.state)
        move = get_action(board)
        board = board.move(move)

        # ai part
        graphics(board.state)
        print("AI part, wait... ")
        move = get_next_move(board)
        board = board.move(move)

        if judge(board) == 1:
            break

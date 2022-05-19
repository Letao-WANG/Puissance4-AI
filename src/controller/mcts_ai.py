import numpy as np
import os
import sys

root_dir = os.getcwd().replace("controller", "")
sys.path.append(root_dir + "controller")
sys.path.append(root_dir + "model")
sys.path.append(root_dir + "view")

from mcts import TreeSearch, TreeNode
from board import Board
from graphics import graphics, get_action, judge

"""
Playing game with MCTS
"""

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

    number_visit = level * 500

    while not board.game_result:
        # human part
        graphics(board.state)
        move = get_action(board)
        board = board.move(move)

        # ai part
        graphics(board.state)
        print("AI part, wait... ")

        ini_board = board
        init_root = TreeNode(ini_board)
        init_mcts = TreeSearch(init_root)
        init_best_node = init_mcts.best_action(number_visit)
        board = init_best_node.board

        if judge(board) == 1:
            break



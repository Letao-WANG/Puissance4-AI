import numpy as np
import os
import sys

from mcts import TreeSearch, TreeNode
from board import Board
from graphics import graphics, get_action, judge

root_dir = os.getcwd().replace("controller", "")
sys.path.append(root_dir + "controller")
sys.path.append(root_dir + "model")
sys.path.append(root_dir + "view")

"""
Playing game with MCTS
"""


def init_board():
    """
    Initialize game board class
    :return:
    """
    init_state = np.zeros((6, 7))
    ini_board = Board(state=init_state, next_to_move=1)
    init_root = TreeNode(ini_board)
    init_mcts = TreeSearch(init_root)
    init_best_node = init_mcts.best_action(500)
    c_board = init_best_node.board
    return c_board


board = init_board()
graphics(board.state)

while True:
    move1 = get_action(board)
    board = board.move(move1)

    root = TreeNode(board)
    mcts = TreeSearch(root)
    best_node = mcts.best_action(500)
    board = best_node.board

    graphics(board.state)
    if judge(board) == 1:
        break

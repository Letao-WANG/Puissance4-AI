import numpy as np

from mcts import TreeSearch, TreeNode
from board import Board
from util import heuristic

# init_state = np.array([[0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0],
#                        [1, 0, 0, 0, 0, 0, 0],
#                        [0, 1, 0, 0, 0, 0, 0],
#                        [0, 0, 1, 0, 0, 0, 0],
#                        [0, 0, 0, 1, 0, 0, 0]])
# print(board.is_winner(1))
# print(board.check_adjacent(1, 4, 2, -1, 1))


def test_value_mcts():
    init_state = np.zeros((6, 7))
    board = Board(state=init_state, next_to_move=1)
    init_root = TreeNode(board)
    init_mcts = TreeSearch(init_root)
    init_best_node = init_mcts.best_action(5000)

    for i in range(7):
        print(str(i) + ' ' + str(init_root.children[i]))


test_value_mcts()


def test_heuristic():
    init_state = np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, -1, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0]])
    board = Board(state=init_state, next_to_move=-1)
    print(heuristic(board))


# test_heuristic()

import numpy as np

from src.mcts.model.TreeNode import TreeNode
from src.mcts.model.TreeSearch import TreeSearch
from src.mcts.model.board import Board
from src.mcts.view.graphics import get_action, graphics, judge

init_state = np.zeros((6, 7))
board = Board(state=init_state, next_to_move=1)
init_root = TreeNode(board)
init_mcts = TreeSearch(init_root)
init_best_node = init_mcts.best_action(100)

print(init_root.children[0])

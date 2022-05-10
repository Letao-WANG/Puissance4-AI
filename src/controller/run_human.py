import numpy as np

from src.model.board import Board
from src.view.graphics import get_action, graphics, judge

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

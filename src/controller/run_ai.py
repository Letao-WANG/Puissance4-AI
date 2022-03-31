import numpy as np

from src.model.board import Board
from src.model.util import get_next_move
from src.view.graphics import get_action, graphics, judge

init_state = np.zeros((6, 7))
board = Board(state=init_state, next_to_move=1)

while not board.game_result:
    graphics(board.state)

    # human part
    move = get_action(board)
    board = board.move(move)

    # ai part
    move = get_next_move(board)
    board = board.move(move)

    if judge(board) == 1:
        break

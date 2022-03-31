import numpy as np

from src.mcts.model.board import Board
from src.mcts.view.graphics import get_action, graphics, judge

init_state = np.zeros((6, 7))
board = Board(state=init_state, next_to_move=1)

while not board.game_result:
    graphics(board.state)
    move = get_action(board, board.next_to_move)
    board = board.move(move)

    if judge(board) == 1:
        break

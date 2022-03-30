import numpy
import numpy as np

from src.mcts.model.move import Move


class Board(object):
    x = 1
    o = -1

    def __init__(self, state: numpy.ndarray, next_to_move=1):
        self.row = state.shape[0]
        self.col = state.shape[1]
        self.state = state
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        row_sum = np.sum(self.state, 0)
        col_sum = np.sum(self.state, 1)
        diag_sum_tl = self.state.trace()
        diag_sum_tr = self.state[::-1].trace()

        if any(row_sum == 4) or any(col_sum == 4) or diag_sum_tl == 4 or diag_sum_tr == 4:
            return 1
        elif any(row_sum == -4) or any(col_sum == -4) or diag_sum_tl == -4 or diag_sum_tr == -4:
            return -1

        elif np.all(self.state != 0):
            return 0
        else:
            return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        if move.value != self.next_to_move:
            print("board.next_to_move: " + str(self.next_to_move) + " move.value: " + str(move.value))
            return False

        x_in_range = self.row > move.x_coor >= 0
        if not x_in_range:
            return False

        y_in_range = self.col > move.y_coor >= 0
        if not y_in_range:
            return False

        return self.state[move.x_coor, move.y_coor] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.state + " is not legal")
        new_state = np.copy(self.state)
        new_state[move.x_coor, move.y_coor] = move.value

        if self.next_to_move == Board.x:
            next_to_move = Board.o
        else:
            next_to_move = Board.x

        return Board(new_state, next_to_move)

    def can_add_chip(self, col):
        """
        Check if there is room to add in a chip return row if chip can be added
        """
        for i in range((self.row - 1), -1, -1):  # from 5 to 0
            if self.state[i][col] == 0:
                return True, i
        return False, -1

    def get_legal_actions(self):
        """
        :return: list of class Move
        """
        moves = []
        for col in range(self.col):
            can_add, row = self.can_add_chip(col)
            if can_add:
                moves.append(Move(row, col, self.next_to_move))
        return moves



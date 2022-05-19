import numpy as np
from move import Move


class Board(object):
    """
    This class stores information of state.

    x = 1: first player, use board.x (AI)
    o = -1: second player, use board.o (human)

    Attributes:
        row: number of rows in the board
        col: number of cols in the board
        state: information about the position of the chess
        next_to_move: the next player who play the chess
        depth: profondeur maximale pour la recherche (root)
        depth: profondeur actuelle
    """
    x = 1
    o = -1

    def __init__(self, state: np.ndarray, next_to_move=1):
        self.row = state.shape[0]
        self.col = state.shape[1]
        self.state = state
        self.next_to_move = next_to_move
        self.depth = 0
        self.current_depth = 0

    def set_difficulty(self, difficulty):
        self.depth = difficulty

    @property
    def game_result(self):
        """
        0: draw,
        None: not finished,
        Board.x: x won
        Board.o: o won
        :return: result of the game
        """
        if len(self.get_legal_actions()) == 0:
            return 0
        if self.is_winner(Board.o):
            return Board.o
        elif self.is_winner(Board.x):
            return Board.x
        return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        """
        if this move is valid
        :param move:
        :return: result of move validation
        """
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
        """
        play a chess in the board, get next situation of board
        :param move:
        :return: next board (Class Board)
        """
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.state + " is not legal")
        new_state = np.copy(self.state)
        new_state[move.x_coor, move.y_coor] = move.value

        if self.next_to_move == Board.x:
            next_to_move = Board.o
        else:
            next_to_move = Board.x

        return Board(new_state, next_to_move)

    def move2(self, move):
        """
        play a chess in the board, get next situation of board
        :param move:
        :return: next board (Class Board)
        """
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.state + " is not legal")
        new_state = np.copy(self.state)
        new_state[move.x_coor, move.y_coor] = move.value

        if self.next_to_move == Board.x:
            next_to_move = Board.o
        else:
            next_to_move = Board.x
        self.state = new_state
        self.next_to_move = next_to_move

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

    def remove_chip(self, row, column):
        """
        removes a chip from the board of the player
        :param row: row index
        :param column: column index
        
        """
        new_state = np.copy(self.state)
        new_state[row, column] = 0
        if self.next_to_move == Board.x:
            next_to_move = Board.o
        else:
            next_to_move = Board.x
        self.state = new_state
        self.next_to_move = next_to_move
        # return Board(new_state, next_to_move)

    def get_chip(self, row, column):
        """
        gets the value of the matrix wich represents the board of the current player
        :param row: row index of the chip
        :param column: column index of the chip
        :return: 1 if this player placed his chip on this row and column index, 0 otherwise
        """
        return self.state[row, column]

    def is_winner(self, chip):
        """
        verify if the player has won
        :param chip: Board.x or Board.o, the player
        :return:
        """
        ticks = 0
        # vertical
        for row in range(self.row - 3):
            for column in range(self.col):
                ticks = self.check_adjacent(chip, row, column, 1, 0)
                if ticks == 4:
                    return True
        # horizontal
        for row in range(self.row):
            for column in range(self.col - 3):
                ticks = self.check_adjacent(chip, row, column, 0, 1)
                if ticks == 4:
                    return True
        # positive slope diagonal, like \
        for row in range(self.row - 3):
            for column in range(self.col - 3):
                ticks = self.check_adjacent(chip, row, column, 1, 1)
                if ticks == 4:
                    return True
        # negative slope diagonal like /
        for row in range(3, self.row):
            for column in range(self.col - 3):
                ticks = self.check_adjacent(chip, row, column, -1, 1)
                if ticks == 4:
                    return True
        return False

    def check_adjacent(self, chip, row, column, delta_row, delta_col):
        """
        Get the adjacent chip number
        :param chip: chip to verify
        :param row: row index
        :param column: col index
        :param delta_row: row difference
        :param delta_col: col difference
        :return: the number of adjacent chip
        """
        count = 0
        for i in range(4):
            current_chip = self.get_chip(row, column)
            if current_chip == chip:
                count += 1
            row += delta_row
            column += delta_col
        return count




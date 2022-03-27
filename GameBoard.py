class GameBoard:
    board = []
    board_width = 7
    board_height = 6

    def __init__(self):
        self.set_board()

    def set_board(self):
        for row in range(self.board_height):
            self.board.append([])
            for column in range(self.board_width):
                self.board[row].append('-')

    def reset_board(self):
        for row in range(self.board_height):
            for column in range(self.board_width):
                self.board[row][column] = '-'

    def print_board(self):
        for i in range(self.board_height):
            print("| ", end="")
            print(*self.board[i], sep=" | ", end="")
            print(" |\n")

    def is_valid_column(self, column):
        return False if column < 0 or column >= self.board_width else True

    def get_chip(self, row, column):
        return self.board[row][column]

    def can_add_chip(self, column):
        """
        Check if there is room to add in a chip return row if chip can be added
        """
        for i in range((self.board_height - 1), -1, -1):  # from 5 to 0
            if self.board[i][column] == '-':
                return True, i
        return False, -1

    def add_chip(self, chip, row, column):
        """
        check if there is room for a chip to add starting from bottom, return true if spot empty,
        false otherwise
        """
        self.board[row][column] = chip

    def remove_chip(self, row, column):
        self.board[row][column] = '-'

    def is_winner(self, chip):
        ticks = 0
        # vertical
        for row in range(self.board_height - 3):
            for column in range(self.board_width):
                ticks = self.check_adjacent(chip, row, column, 1, 0)
                if ticks == 4:
                    return True
        # horizontal
        for row in range(self.board_height):
            for column in range(self.board_width - 3):
                ticks = self.check_adjacent(chip, row, column, 0, 1)
                if ticks == 4:
                    return True
        # positive slope diagonal
        for row in range(self.board_height - 3):
            for column in range(self.board_width - 3):
                ticks = self.check_adjacent(chip, row, column, 1, 1)
                if ticks == 4:
                    return True
        # negative slope diagonal
        for row in range(3, self.board_height):
            for column in range(self.board_width - 5):
                ticks = self.check_adjacent(chip, row, column, -1, 1)
                if ticks == 4:
                    return True
        return False

    def check_adjacent(self, chip, row, column, delta_row, delta_col):
        count = 0
        for i in range(4):
            current_chip = self.get_chip(row, column)
            if current_chip == chip:
                count += 1
            row += delta_row
            column += delta_col
        return count

import sys
from abc import ABC, ABCMeta, abstractmethod


# abstract class for human and AI players
class Player(metaclass=ABCMeta):
    chip = ""  # 'O' or 'X'

    def __init__(self, chip):
        self.chip = chip

    @abstractmethod
    def play_turn(self, board):
        pass


class Human(Player):
    def __init__(self, chip):
        super(Human, self).__init__(chip)

    def play_turn(self, board):
        column = int(input("Pick a column (enter -1 to quit playing) > "))
        if column == -1:
            sys.exit()
        column -= 1
        while True:
            if board.is_valid_column(column):
                row = board.can_add_chip(column)  # tuple (can add chip[bool], row)
                if row[0]:
                    # attempt to add chip, ask input if failed
                    board.add_chip(self.chip, row[1], column)
                    break
            column = int(input("That column did not work. Try a different column > "))
            column -= 1
        return row[1], column

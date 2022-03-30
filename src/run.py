from player import Human
from ai import AI
from board import GameBoard


class GameClient:
    board = None
    human = None
    ai = None
    winner_found = False
    humans_turn = True
    current_round = 1
    MAX_ROUNDS = 42  # max number of turns before game board is full

    def __init__(self):
        self.board = GameBoard()
        self.human = Human('O')
        difficulty = int(
            input("Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
        show_scores = input("Show scores? (y/n)> ")
        self.ai = AI('X', difficulty, show_scores)

    def play(self):
        print("Playing game...")
        self.board.print_board()
        winner_res = "It's a DRAW!"
        while self.current_round <= self.MAX_ROUNDS and not self.winner_found:
            if self.humans_turn:
                print("Player's turn...")
                played_chip = self.human.play_turn(self.board)
                self.winner_found = self.board.is_winner(self.human.chip)
                if self.winner_found:
                    winner_res = "PLAYER wins!"
                self.humans_turn = False
                print("Player played chip at column ", played_chip[1] + 1)
            else:
                print("AI's turn...")
                played_chip = self.ai.play_turn(self.board)
                self.winner_found = self.board.is_winner(self.ai.chip)
                if self.winner_found:
                    winner_res = "AI wins!"
                self.humans_turn = True
                print("AI played chip at column ", played_chip[1] + 1)
            self.current_round += 1
            self.board.print_board()
        return winner_res

    def reset(self):
        # reset variables
        self.current_round = 1
        self.winner_found = False
        self.humans_turn = True
        self.board.reset_board()
        difficulty = int(
            input("Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
        self.ai.set_difficulty(difficulty)


def end_game(winner_res):
    print(winner_res, end=" ")
    user_input = input("Play again? (y/n)\n")
    return True if user_input == 'y' else False


if __name__ == "__main__":
    gameClient = GameClient()
    winner = gameClient.play()
    playAgain = end_game(winner)
    while playAgain:
        gameClient.reset()
        winner = gameClient.play()
        playAgain = end_game(winner)

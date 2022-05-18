from board import Board
from move import Move

"""
This file is about user interface
"""


def graphics(state):
    """
    print the board
    state: param state: np.array() which is the state of board
    """

    for i in range(state.shape[0]):
        print("\t\t\t")
        for j in range(state.shape[1]):
            if state[i][j] == 0:
                print('_'.center(8), end='')
            if state[i][j] == 1:
                print('X'.center(8), end='')
            if state[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("--------"*state.shape[1])
    print("   ", end='')
    for i in range(state.shape[1]):
        print(str(i) + '   |   ', end='')
    print("")


def get_action(board: Board):
    while True:
        try:
            col = int(input("Your move: "))
            if col>6 or col<0:
                raise ValueError
            break
        except ValueError:
            print("Please input integer between 0 and 6")

    can_add, row = board.can_add_chip(col)
    if can_add:
        move = Move(row, col, board.next_to_move)
    else:
        print("Can not add it")
        move = get_action(board)
    return move



def judge(board):
    if board.is_game_over():
        graphics(board.state)
        if board.game_result == -1: #AI a gagné
            print("You lose!")
        if board.game_result == 0:
            print("Tie!")
        if board.game_result == 1:
            print("You win!") #Humain a gagné
        return 1
    else:
        return -1

from src.model.board import Board
from src.model.move import Move


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
    print("----"*14)
    print("\t")
    for i in range(state.shape[0]+1):
        print(str(i) + '   |   ', end='')
    print("")


def get_action(board: Board):
    col = input("Your move: ")
    can_add, row = board.can_add_chip(int(col))
    if can_add:
        move = Move(row, int(col), board.next_to_move)
    else:
        print("Can not add it:")
        move = get_action(board)
    return move


def judge(board):
    if board.is_game_over():
        graphics(board.state)
        if board.game_result == -1:
            print("You lose!")
        if board.game_result == 0:
            print("Tie!")
        if board.game_result == 1:
            print("You Win!")
        return 1
    else:
        return -1

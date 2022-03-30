from src.mcts.model.board import Board
from src.mcts.model.move import Move
from src.mcts.model.TreeNode import TreeNode
from src.mcts.model.TreeSearch import TreeSearch
import numpy as np


def graphics(state):
    """
    :param state: np.array() which is the state of board
    """
    for i in range(state.shape[0]):
        print("")
        print("{0:3}".format(i).center(8) + "|", end='')
        for j in range(state.shape[1]):
            if state[i][j] == 0:
                print('_'.center(8), end='')
            if state[i][j] == 1:
                print('X'.center(8), end='')
            if state[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def get_action(board: Board, next_to_move):
    move = -1
    col = input("Your move: ")
    can_add, row = board.can_add_chip(int(col))
    if can_add:
        move = Move(row, int(col), next_to_move)
    else:
        print("Can not add it:")
        move = get_action(board, next_to_move)
    return move


def judge(board):
    if board.is_game_over():
        if board.game_result == 1:
            print("You lose!")
        if board.game_result == 0:
            print("Tie!")
        if board.game_result == -1:
            print("You Win!")
        return 1
    else:
        return -1

from util import rollout
from board import *
from collections import defaultdict


class TreeNode(object):
    """
    MCTS node
    """
    def __init__(self, board: Board, parent=None):
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self.board = board
        self.parent = parent
        self.children = []

    def __repr__(self):
        value = (self.q / self.n) + 1.4 * np.sqrt((2 * np.log(self.parent.n) / self.n))
        return "n: " + str(self.n) + ", q: " + str(self.q) + ", value: " + str(value)

    @property
    def untried_actions(self):
        """list of Move"""
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.board.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.board.next_to_move]
        loses = self._results[-1 * self.parent.board.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        """
        expand one child node
        :return: child node
        """
        action = self.untried_actions.pop()
        next_board = self.board.move(action)
        child_node = TreeNode(next_board, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """
        :return: if the game has overed
        """
        return self.board.is_game_over()

    def backpropagate(self, result):
        """
        :param result: result of board
        :return:
        """
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        """
        Get the child node which has the biggest value with parameter 1.4.
        c_param, it represents the will to visit (or select) the nodes on average.
        For example, if the current node's c_param value is large (100),
        all its child nodes have the same visit count value.

        :param c_param: constant, by default 1.4
        :return: child node with the biggest value
        """
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]


class TreeSearch:
    """
    MCTS tree, set of MCTS nodes
    """
    def __init__(self, node: TreeNode):
        self.root = node

    def best_action(self, simulations_number):
        """
        Get the best child node, which means the child node that have the biggest value
        :param simulations_number: suggest 500 to 5000.
                The higher the number, the better the result and the slower the speed.
        :return: the best child which has the biggest value with parameter 0.
        """
        for _ in range(0, simulations_number):
            v = self.tree_policy()  # v is a node
            result = rollout(v.board)
            v.backpropagate(result)
        # exploitation only
        return self.root.best_child(c_param=0)

    def tree_policy(self):
        """
        MCTS Selection and Expansion
        :return: self or new node
        """
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

from src.model.TreeNode import TreeNode
from src.model.util import rollout


class TreeSearch:
    """
    MCTS tree, set of MCTS nodes
    """
    def __init__(self, node: TreeNode):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            v = self.tree_policy()  # v is a node
            result = rollout(v.board)
            v.backpropagate(result)
        # exploitation only
        return self.root.best_child(c_param=0)

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

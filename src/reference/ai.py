import math
from player import Player

INFINITY = math.inf


class AI(Player):
    depth = 0
    current_depth = 0
    show_scores = False

    def __init__(self, chip='X', difficulty=1, show_scores='n'):
        super(AI, self).__init__(chip)
        self.set_difficulty(difficulty)
        self.log_scores(show_scores)

    def set_difficulty(self, difficulty):
        self.depth = difficulty

    def log_scores(self, show_scores):
        if show_scores == 'y':
            self.show_scores = True

    def play_turn(self, board):
        move = self.alpha_beta_search(board)
        board.add_chip(self.chip, move[0], move[1])
        return move

    # returns tuple of (row, column)
    def generate_moves(self, board):
        possible_moves = []  # list of possible positions
        for column in range(board.board_width):
            move = board.can_add_chip(column)
            if move[0]:  # if chip can be added
                possible_moves.append((move[1], column))  # (row, column)
        return possible_moves

    def evaluate_heuristic(self, board):

        horizontal_score = 0
        vertical_score = 0
        diagonal1_score = 0
        diagonal2_score = 0

        # Vertical
        # Check each column for vertical score
        #
        # 3 possible situations per column
        #  0  1  2  3  4  5  6
        # [x][ ][ ][ ][ ][ ][ ] 0
        # [x][x][ ][ ][ ][ ][ ] 1
        # [x][x][x][ ][ ][ ][ ] 2
        # [x][x][x][ ][ ][ ][ ] 3
        # [ ][x][x][ ][ ][ ][ ] 4
        # [ ][ ][x][ ][ ][ ][ ] 5

        for row in range(board.board_height - 3):
            for column in range(board.board_width):
                score = self.score_position(board, row, column, 1, 0)
                vertical_score += score

            # Horizontal
            # Check each row's score
            #
            # 4 possible situations per row
            #  0  1  2  3  4  5  6
            # [x][x][x][x][ ][ ][ ] 0
            # [ ][x][x][x][x][ ][ ] 1
            # [ ][ ][x][x][x][x][ ] 2
            # [ ][ ][ ][x][x][x][x] 3
            # [ ][ ][ ][ ][ ][ ][ ] 4
            # [ ][ ][ ][ ][ ][ ][ ] 5
        for row in range(board.board_height):
            for column in range(board.board_width - 3):
                score = self.score_position(board, row, column, 0, 1)
                horizontal_score += score

        # Diagonal points 1 (negative-slope)
        #
        #
        #  0  1  2  3  4  5  6
        # [x][ ][ ][ ][ ][ ][ ] 0
        # [ ][x][ ][ ][ ][ ][ ] 1
        # [ ][ ][x][ ][ ][ ][ ] 2
        # [ ][ ][ ][x][ ][ ][ ] 3
        # [ ][ ][ ][ ][ ][ ][ ] 4
        # [ ][ ][ ][ ][ ][ ][ ] 5
        for row in range(board.board_height - 3):
            for column in range(board.board_width - 3):
                score = self.score_position(board, row, column, 1, 1)
                diagonal1_score += score

            # Diagonal points 2 (positive slope)
            #
            #
            #  0  1  2  3  4  5  6
            # [ ][ ][ ][x][ ][ ][ ] 0
            # [ ][ ][x][ ][ ][ ][ ] 1
            # [ ][x][ ][ ][ ][ ][ ] 2
            # [x][ ][ ][ ][ ][ ][ ] 3
            # [ ][ ][ ][ ][ ][ ][ ] 4
            # [ ][ ][ ][ ][ ][ ][ ] 5
        for row in range(3, board.board_height):
            for column in range(board.board_width - 3):
                score = self.score_position(board, row, column, -1, 1)
                diagonal2_score += score

        return horizontal_score + vertical_score + diagonal1_score + diagonal2_score

    def score_position(self, board, row, column, delta_row, delta_col):
        """
        Heuristic evaluation for current state +1000, +100, +10, +1 for
        4-,3-,2-,1-in-a-line for AI player -1000, -100,
        -10, -1 for 4-,3-,2-,1-in-a-line for human player 0 otherwise
        """

        human_score = 0
        ai_score = 0
        human_points = 0
        ai_points = 0
        for i in range(4):
            current_chip = board.get_chip(row, column)
            if current_chip == self.chip:  # if current chip is AI
                ai_points += 1
            elif current_chip == 'O':  # player chip
                human_points += 1
            # empty otherwise
            row += delta_row
            column += delta_col

        if human_points == 1:
            human_score = -1  # -1 point
        elif human_points == 2:
            human_score = -10  # -10 points
        elif human_points == 3:
            human_score = -100  # -100 points
        elif human_points == 4:
            human_score = -1000  # -1000 points
        # otherwise

        if ai_points == 1:
            ai_score = 1  # 1 point
        elif ai_points == 2:
            ai_score = 10  # 10 points
        elif ai_points == 3:
            ai_score = 100  # 100 points
        elif ai_points == 4:
            ai_score = 1000  # 1000 points
        # otherwise

        return human_score + ai_score

    def alpha_beta_search(self, state):
        self.current_depth = 0
        scores = []
        best_action = None
        v = max_value = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        actions = self.generate_moves(state)
        for action in actions:
            state.add_chip(self.chip, action[0], action[1])
            v = self.min_value(state, alpha, beta)
            scores.append(v)
            if self.show_scores:
                print("SCORE: ", v)
            print("action: " + str(best_action))
            print("v: " + str(v))
            print("maxi_value: " + str(max_value))
            if v > max_value:
                best_action = action
                max_value = v
                alpha = max(alpha, max_value)
            self.current_depth -= 1
            state.remove_chip(action[0], action[1])
        if len(scores) == 1:
            best_action = actions[0]
        return best_action

    def max_value(self, state, alpha, beta):
        self.current_depth += 1
        actions = self.generate_moves(state)
        if not actions or self.current_depth >= self.depth:  # if list of next moves is empty or reached root
            score = self.evaluate_heuristic(state)
            return score
        else:
            v = -INFINITY
            for action in actions:
                state.add_chip(self.chip, action[0], action[1])
                v = max(v, self.min_value(state, alpha, beta))
                if v >= beta:
                    self.current_depth -= 1
                    state.remove_chip(action[0], action[1])
                    return v
                alpha = max(v, alpha)
                self.current_depth -= 1
                state.remove_chip(action[0], action[1])
            return v

    def min_value(self, state, alpha, beta):
        self.current_depth += 1
        actions = self.generate_moves(state)
        if not actions or self.current_depth >= self.depth:  # if list of next moves is empty or reached root
            score = self.evaluate_heuristic(state)
            return score
        else:
            v = INFINITY
            for action in actions:
                state.add_chip('O', action[0], action[1])
                v = min(v, self.max_value(state, alpha, beta))
                if v <= alpha:
                    self.current_depth -= 1
                    state.remove_chip(action[0], action[1])
                    return v
                beta = min(v, beta)
                self.current_depth -= 1
                state.remove_chip(action[0], action[1])
            return v

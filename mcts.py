import math
import random


class TreeNode():
    def __init__(self, board, parent):
        self.board = board
        if self.board.is_over_deploy():
            self.is_terminal = True
        else:
            self.is_terminal = False
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}


class MCTS():
    def search(self, initial_state):
        self.root = TreeNode(initial_state, None)
        for iteration in range(250):
            node = self.select(self.root)
            score = self.rollout(node.board)
            self.backpropagate(node, score)
        try:
            return self.get_best_move(self.root, 0)

        except:
            pass

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        states = node.board.generate_states()
        for state in states:
            if str(state.position) not in node.children:
                new_node = TreeNode(state, node)
                node.children[str(state.position)] = new_node
                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

        print('Should not get here!!!')

    def rollout(self, board):
        while not board.is_over_deploy():
            board = random.choice(board.generate_states())
        score = 0

        # rollout also for score if only r and n or only b and n are in continent

        # North America
        if all(board.position[i, 0] == 'b' for i in range(4)) \
                and all(board.position[i, 1] == 'b' for i in range(4)) \
                and board.position[0, 2] == 'b':
            score -= 5
        elif all(board.position[i, 0] == 'r' for i in range(4)) \
                and all(board.position[i, 1] == 'r' for i in range(4)) \
                and board.position[0, 2] == 'r':
            score += 5

        if (any(board.position[i, 0] == 'b' for i in range(4))
            or any(board.position[i, 1] == 'b' for i in range(4))
            or board.position[0, 2] == 'b') \
                and (all(board.position[i, 0] != 'r' for i in range(4))
                     and all(board.position[i, 1] != 'r' for i in range(4))
                     and board.position[0, 2] != 'r'):
            score -= 2.5
        elif (any(board.position[i, 0] == 'r' for i in range(4))
              or any(board.position[i, 1] == 'r' for i in range(4))
              or board.position[0, 2] == 'r') \
                and (all(board.position[i, 0] != 'b' for i in range(4))
                     and all(board.position[i, 1] != 'b' for i in range(4))
                     and board.position[0, 2] != 'b'):
            score += 2.5

        # South America
        if all(board.position[i, 0] == 'b' for i in range(4, 6)) \
                and all(board.position[i, 1] == 'b' for i in range(4, 6)):
            score -= 2
        elif all(board.position[i, 0] == 'r' for i in range(4, 6)) \
                and all(board.position[i, 1] == 'r' for i in range(4, 6)):
            score += 2

        if (any(board.position[i, 0] == 'b' for i in range(4, 6))
            or any(board.position[i, 1] == 'b' for i in range(4, 6))) \
                and (all(board.position[i, 0] != 'r' for i in range(4, 6))
                     and all(board.position[i, 1] != 'r' for i in range(4, 6))):
            score -= 1
        elif (any(board.position[i, 0] == 'r' for i in range(4, 6))
              or any(board.position[i, 1] == 'r' for i in range(4, 6))) \
                and (all(board.position[i, 0] != 'b' for i in range(4, 6))
                     and all(board.position[i, 1] != 'b' for i in range(4, 6))):
            score += 1

        # Europe
        if all(board.position[i, 2] == 'b' for i in range(1, 4)) \
                and all(board.position[i, 3] == 'b' for i in range(4)):
            score -= 5
        elif all(board.position[i, 2] == 'r' for i in range(1, 4)) \
                and all(board.position[i, 3] == 'r' for i in range(4)):
            score += 5

        if (any(board.position[i, 2] == 'b' for i in range(1, 4))
            or any(board.position[i, 3] == 'b' for i in range(4))) \
                and (all(board.position[i, 2] != 'r' for i in range(1, 4))
                     and all(board.position[i, 3] != 'r' for i in range(4))):
            score -= 2.5
        elif (any(board.position[i, 2] == 'r' for i in range(1, 4))
              or any(board.position[i, 3] == 'r' for i in range(4))) \
                and (all(board.position[i, 2] != 'b' for i in range(1, 4))
                     and all(board.position[i, 3] != 'b' for i in range(4))):
            score += 2.5

        # Africa
        if all(board.position[4, i] == 'b' for i in range(2, 5)) \
                and all(board.position[5, i] == 'b' for i in range(2, 5)):
            score -= 3
        elif all(board.position[4, i] == 'r' for i in range(2, 5)) \
                and all(board.position[5, i] == 'r' for i in range(2, 5)):
            score += 3

        if (any(board.position[4, i] == 'b' for i in range(2, 5))
            or any(board.position[5, i] == 'b' for i in range(2, 5))) \
                and (all(board.position[4, i] != 'r' for i in range(2, 5))
                     and all(board.position[5, i] != 'r' for i in range(2, 5))):
            score -= 1.5
        elif (any(board.position[4, i] == 'r' for i in range(2, 5))
              or any(board.position[5, i] == 'r' for i in range(2, 5))) \
                and (all(board.position[4, i] != 'b' for i in range(2, 5))
                     and all(board.position[5, i] != 'b' for i in range(2, 5))):
            score += 1.5

        # Asia
        if all(board.position[i, 4] == 'b' for i in range(4)) \
                and all(board.position[i, 5] == 'b' for i in range(4)) \
                and all(board.position[i, 6] == 'b' for i in range(4)):
            score -= 7
        elif all(board.position[i, 4] == 'r' for i in range(4)) \
                and all(board.position[i, 5] == 'r' for i in range(4)) \
                and all(board.position[i, 6] == 'r' for i in range(4)):
            score += 7

        if (any(board.position[i, 4] == 'b' for i in range(4))
            or any(board.position[i, 5] == 'b' for i in range(4))
            or any(board.position[i, 6] == 'b' for i in range(4))) \
                and (all(board.position[i, 4] != 'r' for i in range(4))
                     and all(board.position[i, 5] != 'r' for i in range(4))
                     and all(board.position[i, 6] != 'r' for i in range(4))):
            score -= 3.5
        elif (any(board.position[i, 4] == 'r' for i in range(4))
              or any(board.position[i, 5] == 'r' for i in range(4))
              or any(board.position[i, 6] == 'r' for i in range(4))) \
                and (all(board.position[i, 4] != 'b' for i in range(4))
                     and all(board.position[i, 5] != 'b' for i in range(4))
                     and all(board.position[i, 6] != 'b' for i in range(4))):
            score += 3.5

        # Australia
        if all(board.position[i, 5] == 'b' for i in range(4, 6)) \
                and all(board.position[i, 6] == 'b' for i in range(4, 6)):
            score -= 2
        elif all(board.position[i, 5] == 'r' for i in range(4, 6)) \
                and all(board.position[i, 6] == 'r' for i in range(4, 6)):
            score += 2

        if (any(board.position[i, 5] == 'b' for i in range(4, 6))
            or any(board.position[i, 6] == 'b' for i in range(4, 6))) \
                and (all(board.position[i, 5] != 'r' for i in range(4, 6))
                     and all(board.position[i, 6] != 'r' for i in range(4, 6))):
            score -= 1
        elif (any(board.position[i, 5] == 'r' for i in range(4, 6))
            or any(board.position[i, 6] == 'r' for i in range(4, 6))) \
                and (all(board.position[i, 5] != 'b' for i in range(4, 6))
                     and all(board.position[i, 6] != 'b' for i in range(4, 6))):
            score += 1

        return score

    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            if child_node.board.player_2 == 'r':
                current_player = 1
            elif child_node.board.player_2 == 'b':
                current_player = -1

            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(
                math.log(node.visits / child_node.visits))

            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            elif move_score == best_score:
                best_moves.append(child_node)

        return random.choice(best_moves)

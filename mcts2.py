import math
import random
from copy import deepcopy

class TreeNode():
    def __init__(self, board, parent):
        self.board = board
        if self.board.is_over():
            self.is_terminal = True
        else:
            self.is_terminal = False
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}

class MCTS2():
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
            if str(state.count) not in node.children:
                new_node = TreeNode(state, node)
                node.children[str(state.count)] = new_node
                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                return new_node
        print('Should not get here!!!')

    def rollout(self, board):
        while not board.is_over():
            board = random.choice(board.generate_states())
        score = 0

        simboard = deepcopy(board)
        def attack_territory(board, row, col, targets):
            if board.position[row, col] == 'b' or board.position[row, col] == 'r':
                player = board.position[row, col]
                if board.count[row, col] > 1:
                    attacker = bool(random.getrandbits(1))
                    if attacker:
                        target_row, target_col = random.choice(targets)
                        if board.position[target_row, target_col] != player:
                            odds = 0.5 ** (board.count[row, col] - 1 - board.count[target_row, target_col])
                            if odds < 1:
                                if random.randint(0, 100) > 100 - (0.5 * odds * 100):
                                    # print('loser majority')
                                    board.count[row, col] = 1
                                    for i in range(board.count[target_row, target_col] - 1):
                                        if random.randint(0, 100) < 100 - (0.5 * odds * 100):
                                            board.count[target_row, target_col] -= 1
                                else:
                                    # print('victory majority')
                                    for i in range(board.count[target_row, target_col]):
                                        if random.randint(0, 100) < 100 - ((0.5 ** board.count[target_row, target_col]) * 100):
                                            board.count[row, col] -= 1
                                    board.count[row, col] -= 1
                                    board.position[target_row, target_col] = player
                                    board.count[target_row, target_col] = 1
                                    for i in range(board.count[row, col] - 1):
                                        if random.randint(0, 100) >= 50:
                                            board.count[row, col] -= 1
                                            board.count[target_row, target_col] += 1
                            if odds >= 1:
                                if random.randint(0, 100) > 100 - ((1 / odds) * 100):
                                    # print('victory minority')
                                    board.position[target_row, target_col] = player
                                    for i in range(board.count[row, col] - 2):
                                        if random.randint(0, 100) < 100 - (0.5 * odds * 100):
                                            board.count[row, col] -= 1
                                    board.position[target_row, target_col] = player
                                    board.count[row, col] -= 1
                                    board.count[target_row, target_col] = 1
                                    for i in range(board.count[row, col] - 1):
                                        if random.randint(0, 100) >= 50:
                                            board.count[row, col] -= 1
                                            board.count[target_row, target_col] += 1
                                else:
                                    # print('loser minority')
                                    for i in range(board.count[row, col] - 1):
                                        if random.randint(0, 100) < 100 - ((0.5 ** board.count[row, col]) * 100):
                                            board.count[target_row, target_col] -= 1
                                    board.count[row, col] = 1

        def randomize_attack_order():
            territories = [
                (0, 0, [[0, 6], [0, 1], [1, 0]]),  # Alaska
                (1, 0, [[0, 1], [0, 2], [1, 1], [2, 0]]),  # Alberta
                (2, 0, [[1, 0], [3, 0], [1, 1], [3, 1]]),  # Western United States
                (3, 0, [[2, 0], [4, 0], [3, 1]]),  # Central America
                (4, 0, [[3, 0], [5, 0], [4, 1]]),  # Venezuela
                (5, 0, [[4, 0], [4, 1], [5, 1]]),  # Peru
                (0, 1, [[0, 0], [1, 0], [1, 1], [0, 2]]),  # Northwest Territory
                (1, 1, [[1, 0], [2, 0], [0, 1], [0, 2], [2, 1], [3, 1]]),  # Ontario
                (2, 1, [[1, 1], [3, 1], [0, 2]]),  # Eastern Canada
                (3, 1, [[3, 0], [4, 0], [1, 1], [2, 1]]),  # Eastern United States
                (4, 1, [[4, 0], [5, 0], [5, 1], [4, 2]]),  # Brazil
                (5, 1, [[5, 0], [4, 1]]),  # Argentina
                (0, 2, [[0, 1], [1, 2], [2, 1], [0, 3]]),  # Greenland
                (1, 2, [[0, 3], [2, 2], [1, 3]]),  # Great Britain
                (2, 2, [[1, 2], [1, 3], [2, 3], [3, 3], [3, 2]]),  # Northern Europe
                (3, 2, [[2, 2], [3, 3], [4, 2]]),  # Western Europe
                (4, 2, [[4, 1], [3, 2], [3, 3], [4, 3], [5, 2], [4, 4]]),  # North Africa
                (5, 2, [[4, 2], [5, 3], [4, 4]]),  # Central Africa
                (0, 3, [[0, 2], [1, 2], [1, 3]]),  # Iceland
                (1, 3, [[0, 3], [2, 3], [1, 2], [2, 2]]),  # Scandinavia
                (2, 3, [[1, 3], [3, 3], [2, 2], [1, 4], [2, 4], [3, 4]]),  # Russia
                (3, 3, [[2, 3], [4, 3], [2, 2], [3, 2], [4, 2], [3, 4]]),  # Southern Europe
                (4, 3, [[3, 3], [4, 2], [3, 4], [4, 4]]),  # Egypt
                (5, 3, [[5, 2], [5, 4], [4, 4]]),  # South Africa
                (0, 4, [[0, 5], [0, 6], [1, 5]]),  # Yakutsk
                (1, 4, [[2, 3], [2, 4], [2, 5], [1, 5]]),  # Ural
                (2, 4, [[2, 3], [2, 5], [1, 4], [3, 4], [3, 5]]),  # Afghanistan
                (3, 4, [[4, 4], [2, 4], [2, 3], [3, 3], [4, 3], [3, 5]]),  # Middle East
                (4, 4, [[4, 2], [5, 2], [4, 3], [5, 3], [3, 4], [5, 4]]),  # East Africa
                (5, 4, [[4, 4], [5, 3]]),  # Madagascar
                (0, 5, [[0, 4], [0, 6], [2, 6]]),  # Irkutsk
                (1, 5, [[0, 4], [1, 4], [2, 6]]),  # Siberia
                (2, 5, [[1, 4], [2, 4], [2, 6], [3, 6], [3, 5]]),  # China
                (3, 5, [[2, 4], [3, 4], [2, 5], [3, 6]]),  # India
                (4, 5, [[3, 6], [5, 5], [4, 6]]),  # Indonesia
                (5, 5, [[4, 5], [4, 6], [5, 6]]),  # Western Australia
                (0, 6, [[1, 6], [2, 6], [0, 0], [0, 4], [0, 5]]),  # Kamchatka
                (1, 6, [[0, 6], [2, 6]]),  # Japan
                (2, 6, [[0, 5], [0, 6], [1, 5], [1, 6], [2, 5]]),  # Mongolia
                (3, 6, [[2, 5], [3, 5], [4, 5]]),  # Southeast Asia
                (4, 6, [[4, 5], [5, 5], [5, 6]]),  # New Guinea
                (5, 6, [[4, 6], [5, 4]]),  # Eastern Australia
            ]
            random.shuffle(territories)

            for territory in territories:
                attack_territory(simboard, *territory)
        randomize_attack_order()

        # North America
        if all(simboard.position[i, 0] == 'b' for i in range(4)) \
                and all(simboard.position[i, 1] == 'b' for i in range(4)) \
                and simboard.position[0, 2] == 'b':
            score -= 5
        elif all(simboard.position[i, 0] == 'r' for i in range(4)) \
                and all(simboard.position[i, 1] == 'r' for i in range(4)) \
                and simboard.position[0, 2] == 'r':
            score += 5

        if (any(simboard.position[i, 0] == 'b' for i in range(4))
            or any(simboard.position[i, 1] == 'b' for i in range(4))
            or simboard.position[0, 2] == 'b') \
                and (all(simboard.position[i, 0] != 'r' for i in range(4))
                     and all(simboard.position[i, 1] != 'r' for i in range(4))
                     and simboard.position[0, 2] != 'r'):
            score -= 2.5
        elif (any(simboard.position[i, 0] == 'r' for i in range(4))
              or any(simboard.position[i, 1] == 'r' for i in range(4))
              or simboard.position[0, 2] == 'r') \
                and (all(simboard.position[i, 0] != 'b' for i in range(4))
                     and all(simboard.position[i, 1] != 'b' for i in range(4))
                     and simboard.position[0, 2] != 'b'):
            score += 2.5

        # South America
        if all(simboard.position[i, 0] == 'b' for i in range(4, 6)) \
                and all(simboard.position[i, 1] == 'b' for i in range(4, 6)):
            score -= 2
        elif all(simboard.position[i, 0] == 'r' for i in range(4, 6)) \
                and all(simboard.position[i, 1] == 'r' for i in range(4, 6)):
            score += 2

        if (any(simboard.position[i, 0] == 'b' for i in range(4, 6))
            or any(simboard.position[i, 1] == 'b' for i in range(4, 6))) \
                and (all(simboard.position[i, 0] != 'r' for i in range(4, 6))
                     and all(simboard.position[i, 1] != 'r' for i in range(4, 6))):
            score -= 1
        elif (any(simboard.position[i, 0] == 'r' for i in range(4, 6))
              or any(simboard.position[i, 1] == 'r' for i in range(4, 6))) \
                and (all(simboard.position[i, 0] != 'b' for i in range(4, 6))
                     and all(simboard.position[i, 1] != 'b' for i in range(4, 6))):
            score += 1

        # Europe
        if all(simboard.position[i, 2] == 'b' for i in range(1, 4)) \
                and all(simboard.position[i, 3] == 'b' for i in range(4)):
            score -= 5
        elif all(simboard.position[i, 2] == 'r' for i in range(1, 4)) \
                and all(simboard.position[i, 3] == 'r' for i in range(4)):
            score += 5

        if (any(simboard.position[i, 2] == 'b' for i in range(1, 4))
            or any(simboard.position[i, 3] == 'b' for i in range(4))) \
                and (all(simboard.position[i, 2] != 'r' for i in range(1, 4))
                     and all(simboard.position[i, 3] != 'r' for i in range(4))):
            score -= 2.5
        elif (any(simboard.position[i, 2] == 'r' for i in range(1, 4))
              or any(simboard.position[i, 3] == 'r' for i in range(4))) \
                and (all(simboard.position[i, 2] != 'b' for i in range(1, 4))
                     and all(simboard.position[i, 3] != 'b' for i in range(4))):
            score += 2.5

        # Africa
        if all(simboard.position[4, i] == 'b' for i in range(2, 5)) \
                and all(simboard.position[5, i] == 'b' for i in range(2, 5)):
            score -= 3
        elif all(simboard.position[4, i] == 'r' for i in range(2, 5)) \
                and all(simboard.position[5, i] == 'r' for i in range(2, 5)):
            score += 3

        if (any(simboard.position[4, i] == 'b' for i in range(2, 5))
            or any(simboard.position[5, i] == 'b' for i in range(2, 5))) \
                and (all(simboard.position[4, i] != 'r' for i in range(2, 5))
                     and all(simboard.position[5, i] != 'r' for i in range(2, 5))):
            score -= 1.5
        elif (any(simboard.position[4, i] == 'r' for i in range(2, 5))
              or any(simboard.position[5, i] == 'r' for i in range(2, 5))) \
                and (all(simboard.position[4, i] != 'b' for i in range(2, 5))
                     and all(simboard.position[5, i] != 'b' for i in range(2, 5))):
            score += 1.5

        # Asia
        if all(simboard.position[i, 4] == 'b' for i in range(4)) \
                and all(simboard.position[i, 5] == 'b' for i in range(4)) \
                and all(simboard.position[i, 6] == 'b' for i in range(4)):
            score -= 7
        elif all(simboard.position[i, 4] == 'r' for i in range(4)) \
                and all(simboard.position[i, 5] == 'r' for i in range(4)) \
                and all(simboard.position[i, 6] == 'r' for i in range(4)):
            score += 7

        if (any(simboard.position[i, 4] == 'b' for i in range(4))
            or any(simboard.position[i, 5] == 'b' for i in range(4))
            or any(simboard.position[i, 6] == 'b' for i in range(4))) \
                and (all(simboard.position[i, 4] != 'r' for i in range(4))
                     and all(simboard.position[i, 5] != 'r' for i in range(4))
                     and all(simboard.position[i, 6] != 'r' for i in range(4))):
            score -= 3.5
        elif (any(simboard.position[i, 4] == 'r' for i in range(4))
              or any(simboard.position[i, 5] == 'r' for i in range(4))
              or any(simboard.position[i, 6] == 'r' for i in range(4))) \
                and (all(simboard.position[i, 4] != 'b' for i in range(4))
                     and all(simboard.position[i, 5] != 'b' for i in range(4))
                     and all(simboard.position[i, 6] != 'b' for i in range(4))):
            score += 3.5

        # Australia
        if all(simboard.position[i, 5] == 'b' for i in range(4, 6)) \
                and all(simboard.position[i, 6] == 'b' for i in range(4, 6)):
            score -= 2
        elif all(simboard.position[i, 5] == 'r' for i in range(4, 6)) \
                and all(simboard.position[i, 6] == 'r' for i in range(4, 6)):
            score += 2

        if (any(simboard.position[i, 5] == 'b' for i in range(4, 6))
            or any(simboard.position[i, 6] == 'b' for i in range(4, 6))) \
                and (all(simboard.position[i, 5] != 'r' for i in range(4, 6))
                     and all(simboard.position[i, 6] != 'r' for i in range(4, 6))):
            score -= 1
        elif (any(simboard.position[i, 5] == 'r' for i in range(4, 6))
              or any(simboard.position[i, 6] == 'r' for i in range(4, 6))) \
                and (all(simboard.position[i, 5] != 'b' for i in range(4, 6))
                     and all(simboard.position[i, 6] != 'b' for i in range(4, 6))):
            score += 1

        for row in range(6):
            for col in range(7):
                if simboard.position[row, col] == 'b':
                    score -= 0.1
                elif simboard.position[row, col] == 'r':
                    score += 0.1
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
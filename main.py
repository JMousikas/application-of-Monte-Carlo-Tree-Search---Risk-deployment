from copy import deepcopy
from mcts import *
from mcts2 import *
import random


class Board():
    def __init__(self, board=None):
        self.player_1 = 'r'
        self.player_2 = 'b'
        self.player_n = 'n'
        self.empty_square = '.'
        self.position = {}
        self.count = {}
        self.player_1_count = 0
        self.player_2_count = 0
        self.player_n_count = 0
        self.occupy = False
        self.init_board()
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for row in range(6):
            for col in range(7):
                self.position[row, col] = self.empty_square
                self.count[row, col] = 1
                self.player_1_count = 0
                self.player_2_count = 0
                self.player_n_count = 0
                self.occupy = False

    def make_move(self, row, col):
        board = Board(self)
        board.position[row, col] = self.player_1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        return board

    def reinforce(self, row, col):
        board = Board(self)
        board.count[row, col] += 1
        board.player_1_count += 1
        (board.player_1, board.player_2) = (board.player_2, board.player_1)
        (board.player_1_count, board.player_2_count) = (board.player_2_count, board.player_1_count)
        return board

    def is_over(self):
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
            if self.player_1_count < 26 and self.player_2_count < 27:
                return False
        return True

    def is_over_deploy(self):
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False

        return True

    def generate_states(self):
        actions = []
        self.occupy = all(self.position[j, i] != '.' for i in range(7) for j in range(6))
        for row in range(6):
            for col in range(7):
                if self.occupy == False:
                    if self.position[row, col] == self.empty_square:
                        actions.append(self.make_move(row, col))
                elif self.occupy == True:
                    if self.position[row, col] == self.player_1:
                        actions.append(self.reinforce(row, col))
        return actions

    def game_loop(self, results, TroopCounts):
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        print(self)
        mcts = MCTS()
        mcts2 = MCTS2()
        while True:
            self.occupy = all(self.position[j, i] != '.' for i in range(7) for j in range(6))
            user_input = str(random.randint(1, 7)) + ',' + str(random.randint(1, 6))
            # user_input = input('> ')
            if user_input == 'exit': break
            if user_input == '': continue
            try:
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1
                if self.occupy == False:
                    if self.position[row, col] != self.empty_square:
                        print(' Illegal move!')
                        continue
                elif self.occupy == True:
                    if self.position[row, col] != self.player_1:
                        print(' Illegal move!')
                        continue
                if self.occupy == True:
                    self = self.reinforce(row, col)
                else:
                    self = self.make_move(row, col)
                print(self)
                if self.occupy == False:
                    best_move = mcts.search(self)
                    try:
                        self = best_move.board
                    except:
                        pass
                elif self.occupy == True:
                    best_move = mcts2.search(self)
                    try:
                        self = best_move.board
                    except:
                        pass
                print(self)
                if self.is_over():
                    results += [mcts2.rollout(self)]

                    #  double for loop, add whenever position belongs to ai player
                    Troops = {'NorthAmerica': 0, 'SouthAmerica': 0, 'Europe': 0, 'Africa': 0, 'Asia': 0, 'Australia': 0}

                    for row in range(6):
                        for col in range(7):
                            if self.position[row, col] == 'b':
                                if row == 0:
                                    if col == 0 or col == 1 or col == 2:
                                        Troops['NorthAmerica'] += self.count[row, col]
                                    elif col == 3:
                                        Troops['Europe'] += self.count[row, col]
                                    elif col == 4 or col == 5 or col == 6:
                                        Troops['Asia'] += self.count[row, col]
                                if row == 1:
                                    if col == 0 or col == 1:
                                        Troops['NorthAmerica'] += self.count[row, col]
                                    elif col == 2 or col == 3:
                                        Troops['Europe'] += self.count[row, col]
                                    elif col == 4 or col == 5 or col == 6:
                                        Troops['Asia'] += self.count[row, col]
                                if row == 2:
                                    if col == 0 or col == 1:
                                        Troops['NorthAmerica'] += self.count[row, col]
                                    elif col == 2 or col == 3:
                                        Troops['Europe'] += self.count[row, col]
                                    elif col == 4 or col == 5 or col == 6:
                                        Troops['Asia'] += self.count[row, col]
                                if row == 3:
                                    if col == 0 or col == 1:
                                        Troops['NorthAmerica'] += self.count[row, col]
                                    elif col == 2 or col == 3:
                                        Troops['Europe'] += self.count[row, col]
                                    elif col == 4 or col == 5 or col == 6:
                                        Troops['Asia'] += self.count[row, col]
                                if row == 4:
                                    if col == 0 or col == 1:
                                        Troops['SouthAmerica'] += self.count[row, col]
                                    elif col == 2 or col == 3 or col == 4:
                                        Troops['Africa'] += self.count[row, col]
                                    elif col == 5 or col == 6:
                                        Troops['Australia'] += self.count[row, col]
                                if row == 5:
                                    if col == 0 or col == 1:
                                        Troops['SouthAmerica'] += self.count[row, col]
                                    elif col == 2 or col == 3 or col == 4:
                                        Troops['Africa'] += self.count[row, col]
                                    elif col == 5 or col == 6:
                                        Troops['Australia'] += self.count[row, col]

                    TroopCounts += [Troops]
                    print('Game is over!\n')
                    break
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format [r,b]: 1,2 where 1 is column and 2 is row')

    def __str__(self):
        board_string = ''
        for row in range(6):
            for col in range(7):
                board_string += ' %s ' % self.position[row, col]
                board_string += '-'
                board_string += ' %s ' % self.count[row, col]
            board_string += '\n'

        if self.player_1 == 'r':
            board_string = '\n--------------\n "r" to move:\n--------------\n\n' + board_string

        elif self.player_1 == 'b':
            board_string = '\n--------------\n "b" to move:\n--------------\n\n' + board_string

        return board_string


if __name__ == '__main__':
    board = Board()

    results = []
    TroopCounts = []
    import time

    st = time.time()
    for i in range(50):
        board.init_board()
        k = 0
        while k < 14:
            posrow = random.randint(0, 5)
            poscol = random.randint(0, 6)
            if board.position[posrow, poscol] == '.':
                board.position[posrow, poscol] = 'n'
                k += 1

        while board.player_n_count < 26:
            posrow = random.randint(0, 5)
            poscol = random.randint(0, 6)
            if board.position[posrow, poscol] == 'n':
                board.count[posrow, poscol] += 1
                board.player_n_count += 1
        print(i)
        board.game_loop(results, TroopCounts)
    print(results)
    print(TroopCounts)

    TroopAverage = {'NorAme': 0, 'SouAme': 0, 'Asia': 0, 'Europe': 0, 'Africa': 0, 'Austra': 0}
    for j in TroopCounts:
        TroopAverage['NorAme'] += j['NorthAmerica']
        TroopAverage['SouAme'] += j['SouthAmerica']
        TroopAverage['Asia'] += j['Asia']
        TroopAverage['Europe'] += j['Europe']
        TroopAverage['Africa'] += j['Africa']
        TroopAverage['Austra'] += j['Australia']

    print(TroopAverage)
    print('Average Result:', sum(results) / float(len(results)))
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

# Regionen untersuchen
# MCTS 2 effektivität prüfen

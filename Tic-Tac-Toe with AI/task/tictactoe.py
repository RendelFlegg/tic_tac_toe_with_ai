import random


class TicTacToe:
    def __init__(self):
        self.board = {(x, y): ' ' for x in range(1, 4) for y in range(1, 4)}
        self.status = 'Game not finished'
        self.current_move = 'user'

    def show_board(self):
        print("---------")
        for x in range(1, 4):
            line = []
            for y in range(1, 4):
                line.append(self.board[x, y])
            print('|', ' '.join(line), '|')
        print("---------")

    def make_board(self, initial_state):
        self.board = {(x, y): '_' for x in range(1, 4) for y in range(1, 4)}
        for cell, initial_move in zip(self.board, initial_state):
            self.board[cell] = initial_move
        self.show_board()

    def get_coordinates(self):
        while True:
            try:
                coordinates = input('Enter the coordinates: ')
                x, y = coordinates.split()
                x, y = int(x), int(y)
                assert x in range(1, 4) and y in range(1, 4)
                if self.board[x, y] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    return x, y
            except ValueError:
                print('You should enter numbers!')
            except AssertionError:
                print('Coordinates should be from 1 to 3!')

    def choose_turn(self):
        crosses = zeroes = 0
        for value in self.board.values():
            if value == 'X':
                crosses += 1
            if value == 'O':
                zeroes += 1
        if crosses == zeroes:
            return 'X'
        else:
            return 'O'

    def check_row(self, row, column, mark):
        if self.board[row, column] != mark:
            return False
        else:
            if column == 3:
                return True
            return self.check_row(row, column + 1, mark)

    def check_rows(self, row, column, mark):
        if row == 4:
            return self.check_columns(row - 3, column, mark)
            # return False
        else:
            if self.check_row(row, column, mark):
                return True
            else:
                return self.check_rows(row + 1, column, mark)

    def check_column(self, row, column, mark):
        if self.board[row, column] != mark:
            return False
        else:
            if row == 3:
                return True
            return self.check_column(row + 1, column, mark)

    def check_columns(self, row, column, mark):
        if column == 4:
            return False
        else:
            if self.check_column(row, column, mark):
                return True
            else:
                return self.check_columns(row, column + 1, mark)

    def check_diagonals(self, mark):
        return self.board[1, 1] == self.board[2, 2] == self.board[3, 3] == mark or self.board[1, 3] == self.board[
            2, 2] == self.board[3, 1] == mark

    def check_mark(self, mark):
        return self.check_rows(1, 1, mark) or self.check_diagonals(mark)

    def results(self):
        for mark in ['X', 'O']:
            if self.check_mark(mark):
                return f'{mark} wins'
        if ' ' in self.board.values():
            return 'Game not finished'
        else:
            return 'Draw'

    def random_move(self):
        move_list = [key for key in self.board if self.board[key] == ' ']
        print('Making move level "easy"')
        return random.choice(move_list)

    def make_move(self):
        if self.current_move == 'user':
            self.current_move = 'computer'
            return self.get_coordinates()
        else:
            self.current_move = 'user'
            return self.random_move()

    def game(self):
        self.show_board()
        while self.status == 'Game not finished':
            self.board[self.make_move()] = self.choose_turn()
            self.status = self.results()
            self.show_board()
        print(self.status)


if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    tic_tac_toe.game()

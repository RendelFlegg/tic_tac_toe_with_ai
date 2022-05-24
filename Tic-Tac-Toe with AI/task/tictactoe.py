import random


class TicTacToe:
    def __init__(self):
        self.board = {(x, y): ' ' for x in range(1, 4) for y in range(1, 4)}
        self.status = 'Game not finished'
        self.current_player = 'player_one'
        self.players = {}
        self.ai_dictionary = {}
        self.lines = []
        self.get_lines()

    def drop_board(self):
        self.board = {(x, y): ' ' for x in range(1, 4) for y in range(1, 4)}
        self.status = 'Game not finished'
        self.current_player = 'player_one'
        self.players = {}

    def show_board(self):
        print("---------")
        for x in range(1, 4):
            line = []
            for y in range(1, 4):
                line.append(self.board[x, y])
            print('|', ' '.join(line), '|')
        print("---------")

    def load_board(self, initial_state):
        for cell, initial_move in zip(self.board, initial_state.replace('_', ' ')):
            self.board[cell] = initial_move

    def get_lines(self):
        for x in range(1, 4):
            self.lines.append([(x, y) for y in range(1, 4)])
        for y in range(1, 4):
            self.lines.append([(x, y) for x in range(1, 4)])
        self.lines.append([(n, n) for n in range(1, 4)])
        self.lines.append([(n, 4 - n) for n in range(1, 4)])

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
        return self.players[self.current_player]['mark']

    def read_lines(self, mark, idx):
        counter = 0
        for coord in self.lines[idx]:
            if self.board[coord] == mark:
                counter += 1
        if counter == 3:
            return True
        else:
            if idx == 7:
                return None
            return self.read_lines(mark, idx + 1)

    def check_mark(self, mark):
        return self.read_lines(mark, 0)

    def results(self):
        for mark in ['X', 'O']:
            if self.check_mark(mark):
                return f'{mark} wins'
        if ' ' in self.board.values():
            return 'Game not finished'
        else:
            return 'Draw'

    def switch_player(self):
        players_list = list(self.players.keys())
        if self.current_player == players_list[0]:
            self.current_player = players_list[1]
        else:
            self.current_player = players_list[0]

    def make_move(self):
        player_type = self.players[self.current_player]['type']
        if player_type == 'user':
            return self.get_coordinates()
        else:
            return self.ai_dictionary[player_type].ai_move()

    def game(self):
        self.show_board()
        while self.status == 'Game not finished':
            self.board[self.make_move()] = self.choose_turn()
            self.switch_player()
            self.status = self.results()
            self.show_board()
        print(self.status)
        self.drop_board()

    def get_command(self):
        while True:
            try:
                raw_input = input('Input command: ')
                if raw_input == 'exit':
                    return raw_input
                command, player_one, player_two = raw_input.split()
                assert command == 'start'
                self.players = {'player_one': {'type': player_one, 'mark': 'X'},
                                'player_two': {'type': player_two, 'mark': 'O'}}
                return command
            except (AssertionError, ValueError):
                print('Bad parameters!')

    def menu(self):
        command = self.get_command()
        while command != 'exit':
            self.game()
            command = self.get_command()


class AiBasic:
    def __init__(self, game_object):
        self.game_object = game_object

    def random_move(self):
        move_list = [key for key in self.game_object.board if self.game_object.board[key] == ' ']
        return random.choice(move_list)

    def ai_move(self):
        print('Making move level "easy"')
        return self.random_move()


class AiAdvanced(AiBasic):
    def read_lines(self, mark, idx):
        counter = 0
        move = None
        for coord in self.game_object.lines[idx]:
            if self.game_object.board[coord] == mark:
                counter += 1
            if self.game_object.board[coord] == ' ':
                move = coord
        if counter == 2 and move:
            return move
        else:
            if idx == 7:
                return None
            return self.read_lines(mark, idx + 1)

    def ai_move(self):
        mark = self.game_object.players[self.game_object.current_player]['mark']
        opponent_mark = 'O' if mark == 'X' else 'X'
        print('Making move level "medium"')
        return self.read_lines(opponent_mark, 0) or self.read_lines(mark, 0) or self.random_move()


if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    alpha = AiBasic(tic_tac_toe)
    beta = AiAdvanced(tic_tac_toe)
    tic_tac_toe.ai_dictionary['easy'] = alpha
    tic_tac_toe.ai_dictionary['medium'] = beta
    tic_tac_toe.menu()

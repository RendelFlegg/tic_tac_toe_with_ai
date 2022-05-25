import random


class TicTacToe:
    def __init__(self):
        self.board = {(x, y): ' ' for x in range(1, 4) for y in range(1, 4)}
        self.status = 'Game not finished'
        self.current_player = 'player_one'
        self.players = {}
        self.ai_dictionary = {}
        self.lines = []

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

    def check_mark(self, mark):
        return read_lines(self.board, 3, mark, 0)

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
        # self.load_board('XOO_O__XX')
        # self.load_board('O_XX_X_OO')
        # self.load_board('X_OOO_X_X')
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

    def get_moves(self, v_board=None):
        board = self.game_object.board
        if v_board:
            board = v_board
        return [key for key in board if board[key] == ' ']

    def random_move(self):
        move_list = self.get_moves()
        return random.choice(move_list)

    def ai_move(self):
        print('Making move level "easy"')
        return self.random_move()


class AiAdvanced(AiBasic):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.mark = None
        self.opponent_mark = None

    def update_marks(self):
        self.mark = self.game_object.players[self.game_object.current_player]['mark']
        self.opponent_mark = 'O' if self.mark == 'X' else 'X'

    def defend(self):
        return read_lines(self.game_object.board, 2, self.opponent_mark, 0)

    def attack(self):
        return read_lines(self.game_object.board, 2, self.mark, 0)

    def ai_move(self):
        self.update_marks()
        print('Making move level "medium"')
        return self.defend() or self.attack() or self.random_move()


class AiSupreme(AiAdvanced):
    def ai_move(self):
        self.update_marks()
        print('Making move level "hard"')
        if len(self.get_moves()) == 9:
            return 1, 1
        return self.best_move(self.game_object.board)

    def best_move(self, new_board):
        best_score = -10000
        best_move = None
        move_list = self.get_moves(v_board=new_board)

        for move in move_list:
            new_board[move] = self.mark
            score = self.minimax(new_board, 0, False)
            new_board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, new_board, depth, is_maximising):
        move_list = self.get_moves(v_board=new_board)
        if read_lines(new_board, 3, self.opponent_mark, 0):
            return -1
        elif read_lines(new_board, 3, self.mark, 0):
            return 1
        elif len(move_list) == 0:
            return 0

        if is_maximising:
            best_score = -10000
            for move in move_list:
                new_board[move] = self.mark
                score = self.minimax(new_board, depth + 1, False)
                new_board[move] = ' '
                if score > best_score:
                    best_score = score
            return best_score

        else:
            best_score = 10000
            for move in move_list:
                new_board[move] = self.opponent_mark
                score = self.minimax(new_board, depth + 1, True)
                new_board[move] = ' '
                if score < best_score:
                    best_score = score
            return best_score


def get_lines():
    lines_list = []
    for x in range(1, 4):
        lines_list.append([(x, y) for y in range(1, 4)])
    for y in range(1, 4):
        lines_list.append([(x, y) for x in range(1, 4)])
    lines_list.append([(n, n) for n in range(1, 4)])
    lines_list.append([(n, 4 - n) for n in range(1, 4)])
    return lines_list


def read_lines(board, limit, mark, idx):
    counter = 0
    move = None
    for coord in lines[idx]:
        if board[coord] == mark:
            counter += 1
        if board[coord] == ' ':
            move = coord
    if counter == limit:
        if limit == 3:
            return True
        elif move:
            return move
        else:
            return None
    else:
        if idx == 7:
            return None
        return read_lines(board, limit, mark, idx + 1)


def check_win(board, mark):
    return read_lines(board, 3, mark, 0)


lines = get_lines()

if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    alpha = AiBasic(tic_tac_toe)
    beta = AiAdvanced(tic_tac_toe)
    gamma = AiSupreme(tic_tac_toe)
    tic_tac_toe.ai_dictionary['easy'] = alpha
    tic_tac_toe.ai_dictionary['medium'] = beta
    tic_tac_toe.ai_dictionary['hard'] = gamma
    tic_tac_toe.menu()

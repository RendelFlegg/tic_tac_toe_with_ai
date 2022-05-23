def show_board(dictionary):
    print("---------")
    for x in range(1, 4):
        line = []
        for y in range(1, 4):
            line.append(dictionary[x, y])
        print('|', ' '.join(line), '|')
    print("---------")


def move(dictionary, coordinates):
    if dictionary[coordinates] != '_':
        print('This cell is ocupied! Choose another one!')


def get_coordinates(dictionary):
    while True:
        try:
            coordinates = input('Enter the coordinates: ')
            x, y = coordinates.split()
            x, y = int(x), int(y)
            assert x in range(1, 4) and y in range(1, 4)
            if dictionary[x, y] != ' ':
                print('This cell is occupied! Choose another one!')
            else:
                return x, y
        except ValueError:
            print('You should enter numbers!')
        except AssertionError:
            print('Coordinates should be from 1 to 3!')


def choose_turn(dictionary):
    crosses = zeroes = 0
    for value in dictionary.values():
        if value == 'X':
            crosses += 1
        if value == 'O':
            zeroes += 1
    if crosses == zeroes:
        return 'X'
    else:
        return 'O'


def check_row(dictionary, row, column, mark):
    if dictionary[row, column] != mark:
        return False
    else:
        if column == 3:
            return True
        return check_row(dictionary, row, column + 1, mark)


def check_rows(dictionary, row, column, mark):
    if row == 4:
        return check_columns(dictionary, row - 3, column, mark)
        # return False
    else:
        if check_row(dictionary, row, column, mark):
            return True
        else:
            return check_rows(dictionary, row + 1, column, mark)


def check_column(dictionary, row, column, mark):
    if dictionary[row, column] != mark:
        return False
    else:
        if row == 3:
            return True
        return check_column(dictionary, row + 1, column, mark)


def check_columns(dictionary, row, column, mark):
    if column == 4:
        return False
    else:
        if check_column(dictionary, row, column, mark):
            return True
        else:
            return check_columns(dictionary, row, column + 1, mark)


def check_diagonals(dictionary, mark):
    return dictionary[1, 1] == dictionary[2, 2] == dictionary[3, 3] == mark or dictionary[1, 3] == dictionary[2, 2] == dictionary[3, 1] == mark


def check_mark(dictionary, mark):
    return check_rows(dictionary, 1, 1, mark) or check_diagonals(dictionary, mark)


def results(dictionary):
    for mark in ['X', 'O']:
        if check_mark(dictionary, mark):
            return f'{mark} wins'
    if ' ' in dictionary.values():
        return 'Game not finished'
    else:
        return 'Draw'


dict_keys = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
user_input = input('Enter the cells: ').replace('_', ' ')

board_dict = dict(zip(dict_keys, user_input))

show_board(board_dict)

coordinates = get_coordinates(board_dict)
board_dict[coordinates] = choose_turn(board_dict)

show_board(board_dict)
print(results(board_dict))

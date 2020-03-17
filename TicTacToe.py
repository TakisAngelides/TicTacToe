import random as r

def draw_board(board):
    print('  1 2 3')
    print(f'1 {board[0]} {board[1]} {board[2]}')
    print(f'2 {board[3]} {board[4]} {board[5]}')
    print(f'3 {board[6]} {board[7]} {board[8]}')

def get_user_input(board):
    while True:
        print('It is now your turn. This is the current state of the board.')
        draw_board(board)
        while True:
            row = input('Enter the number 1,2 or 3 for the row you want to place your x or o: ')
            if row == '':
                continue
            if int(row) == 1 or int(row) == 2 or int(row) == 3:
                break
        while True:
            if row == '':
                continue
            col = input('Enter the number 1,2 or 3 for the column you want to place your x or o: ')
            if int(col) == 1 or int(col) == 2 or int(col) == 3:
                break
        while True:
            user_symbol = input('Enter either x or o: ')
            if user_symbol == 'o' or user_symbol == 'x':
                break
        row, col = int(row), int(col)
        if board[(row-1)*3 + (col-1)] == '-':
            break
        else:
            print('The position of your symbol is already taken, please choose another position.')
            continue
    return [row, col, user_symbol]

def update_board(rowcolsymbol_list, board):

    row = rowcolsymbol_list[0] - 1
    col = rowcolsymbol_list[1] - 1
    board[row*3 + col] = rowcolsymbol_list[2]

def get_random_computer_move(board, symbol):
    while True:
        row = r.randint(1, 3)
        col = r.randint(1, 3)

        if board[(row-1)*3 + (col-1)] == '-':
            break
    return [row, col, symbol]

def check_win_on_board(board):
    possible_connect_three = [[board[0],board[1],board[2]],
                                [board[3],board[4],board[5]],
                                [board[6],board[7],board[8]],
                                [board[0],board[3],board[6]],
                                [board[1],board[4],board[7]],
                                [board[2],board[5],board[8]],
                                [board[0],board[4],board[8]],
                                [board[2],board[4],board[6]]]
    end_game = False

    for possibility in possible_connect_three:
        if possibility == ['o','o','o'] or ['x','x','x']:
            if possibility == ['o','o','o']:
                print('The game is over. The player with o has won.')
                end_game = True
            elif possibility == ['x','x','x']:
                print('The game is over. The player with x has won.')
                end_game = True
    return end_game

def get_computer_symbol(board):
    symbol_list = ['o', 'x']
    for i in range(len(board)):
        if board[i] != '-':
            idx = symbol_list.index(board[i])
            symbol = symbol_list[idx - 1]
            break
        else:
            if i != len(board) - 1:
                continue
            else:
                symbol = symbol_list[r.randint(0,1)]

    return symbol

end_game = False
board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
choose_who_starts_list = [True, False]
computers_turn = choose_who_starts_list[r.randint(0,1)]

while not end_game:
    flag = True
    computers_turn = not computers_turn
    if computers_turn:
        if flag:
            symbol = get_computer_symbol(board)
            flag = False
        l = get_random_computer_move(board, symbol)
        update_board(l, board)
        end_game = check_win_on_board(board)
    else:
        l = get_user_input(board)
        update_board(l, board)
        draw_board(board)
        end_game = check_win_on_board(board)

    if end_game:
        draw_board(board)


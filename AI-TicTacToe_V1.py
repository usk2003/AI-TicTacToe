import random

# Constants for player and AI symbols
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '


# Function to print the Tic Tac Toe board
def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('---------')


# Function to check if a player has won
def check_win(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
                all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
            all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


# Function to check if the board is full
def is_board_full(board):
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))


# Minimax algorithm for the AI to choose the best move
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, PLAYER_X):
        return -1
    elif check_win(board, PLAYER_O):
        return 1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    eval_val = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval_val)
                    alpha = max(alpha, eval_val)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    eval_val = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval_val)
                    beta = min(beta, eval_val)
                    if beta <= alpha:
                        break
        return min_eval


# Function for AI to make a move using the minimax algorithm
def ai_move(board):
    best_move = None
    best_eval = float('-inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                move_eval = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = EMPTY
                if move_eval > best_eval:
                    best_eval = move_eval
                    best_move = (i, j)
    return best_move


# Function to play the game against AI
def play_ai_game():
    print('Welcome to Tic Tac Toe (Player vs. AI Mode)!')
    player_name = input('Enter your name: ')
    board = [[EMPTY] * 3 for _ in range(3)]
    player_turn = True  # True for PLAYER_X, False for AI (PLAYER_O)

    while not is_board_full(board):
        print_board(board)
        if player_turn:
            print(f"{player_name}'s turn.")
            while True:
                try:
                    move = int(input('Enter your move (1-9): '))
                    if 1 <= move <= 9:
                        row, col = (move - 1) // 3, (move - 1) % 3
                        if board[row][col] == EMPTY:
                            board[row][col] = PLAYER_X
                            if check_win(board, PLAYER_X):
                                print_board(board)
                                print(f'{player_name} wins!')
                                return
                            player_turn = not player_turn
                            break
                        else:
                            print('Cell already taken. Try again.')
                    else:
                        print('Invalid input. Please enter a number between 1 and 9.')
                except ValueError:
                    print('Invalid input. Please enter a number between 1 and 9.')
        else:
            print('AI\'s turn.')
            ai_row, ai_col = ai_move(board)
            board[ai_row][ai_col] = PLAYER_O
            if check_win(board, PLAYER_O):
                print_board(board)
                print('AI wins!')
                return
            player_turn = not player_turn

    print_board(board)
    print('It\'s a draw!')


# Function to play the multiplayer game
def play_multiplayer_game():
    print('Welcome to Tic Tac Toe (Multiplayer Mode)!')
    player1_name = input('Enter name for Player 1 (X): ')
    player2_name = input('Enter name for Player 2 (O): ')

    board = [[EMPTY] * 3 for _ in range(3)]
    player_turn = True  # True for player X, False for player O

    while not is_board_full(board):
        print_board(board)
        if player_turn:
            print(f"{player1_name}'s turn.")
        else:
            print(f"{player2_name}'s turn.")
        while True:
            try:
                move = int(input('Enter your move (1-9): '))
                if 1 <= move <= 9:
                    row, col = (move - 1) // 3, (move - 1) % 3
                    if board[row][col] == EMPTY:
                        board[row][col] = PLAYER_X if player_turn else PLAYER_O
                        if check_win(board, PLAYER_X if player_turn else PLAYER_O):
                            print_board(board)
                            print(f'{player1_name} wins!' if player_turn else f'{player2_name} wins!')
                            return
                        player_turn = not player_turn
                        break
                    else:
                        print('Cell already taken. Try again.')
                else:
                    print('Invalid input. Please enter a number between 1 and 9.')
            except ValueError:
                print('Invalid input. Please enter a number between 1 and 9.')

    print_board(board)
    print('It\'s a draw!')


if __name__ == '__main__':
    while True:
        print('Welcome to Tic Tac Toe!')
        print('1. Play against AI')
        print('2. Play multiplayer')
        print('3. Quit')
        choice = input('Enter your choice: ')
        if choice == '1':
            play_ai_game()
        elif choice == '2':
            play_multiplayer_game()
        elif choice == '3':
            break
        else:
            print('Invalid choice. Please try again.')

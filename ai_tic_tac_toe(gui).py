import tkinter as tk

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER1_COLOR = "lightcoral"
PLAYER2_COLOR = "lightblue"
WIN_COLOR = "lightgreen"
BACKGROUND_COLOR = "lightgray"
WINDOW_SIZE = "400x500"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND_COLOR)
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        self.is_multiplayer = False
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.stats = {"Player 1": {"wins": 0, "losses": 0, "draws": 0},
                      "Player 2": {"wins": 0, "losses": 0, "draws": 0}}
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.reset_all_state() 
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Welcome to Tic Tac Toe", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=10)
        tk.Button(frame, text="1. Play with AI", command=lambda: self.ask_names(False), width=20).pack(pady=5)
        tk.Button(frame, text="2. Multiplayer", command=lambda: self.ask_names(True), width=20).pack(pady=5)
        tk.Button(frame, text="3. Quit", command=self.quit_game, width=20).pack(pady=5)

    def ask_names(self, multiplayer):
        self.reset_all_state()
        self.is_multiplayer = multiplayer
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame.pack(expand=True, pady=20)

        tk.Label(frame, text="Enter Player Names", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=10)

        tk.Label(frame, text="Player 1 (X): ", bg=BACKGROUND_COLOR).pack()
        player1_entry = tk.Entry(frame)
        player1_entry.pack(pady=5)
        player1_entry.focus()

        player2_entry = None
        if multiplayer:
            tk.Label(frame, text="Player 2 (O): ", bg=BACKGROUND_COLOR).pack()
            player2_entry = tk.Entry(frame)
            player2_entry.pack(pady=5)

        def start_game(event=None):
            self.player1_name = player1_entry.get() or "Player 1"
            self.player2_name = player2_entry.get() if multiplayer else "AI"
            self.create_game_screen()

        player1_entry.bind("<Return>", lambda e: player2_entry.focus() if multiplayer else start_game())
        if multiplayer:
            player2_entry.bind("<Return>", start_game)

        tk.Button(frame, text="Start Game", command=start_game).pack(pady=10)

    def create_game_screen(self):
        self.reset_all_state()
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame.pack(expand=True)

        self.notification_label = tk.Label(frame, text=f"{self.player1_name}'s Turn (X)",
                                           font=("Arial", 14), relief="solid", borderwidth=2, pady=5, bg=BACKGROUND_COLOR)
        self.notification_label.pack(pady=10)

        game_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        game_frame.pack()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    game_frame, text='', font=('Arial', 24), width=5, height=2, bd=2, relief="raised",
                    command=lambda row=i, col=j: self.player_move(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

        tk.Button(frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=5)

    def player_move(self, row, col):
        if self.buttons[row][col]['state'] == "disabled":  # Skip if buttons are disabled
            return

        if self.board[row][col] == EMPTY:
            current_player = PLAYER_X if self.player_turn else PLAYER_O
            self.board[row][col] = current_player
            self.buttons[row][col].config(text=current_player, bg=PLAYER1_COLOR if self.player_turn else PLAYER2_COLOR)

            if check_win(self.board, current_player):
                winner = self.player1_name if self.player_turn else self.player2_name
                self.update_stats(winner)
                self.highlight_win_line(current_player)
                return

            if is_board_full(self.board):
                self.update_stats("draw")
                self.show_stats_screen("It's a draw!")
                return

            self.player_turn = not self.player_turn
            next_turn = self.player1_name if self.player_turn else self.player2_name
            self.notification_label.config(text=f"{next_turn}'s Turn ({'X' if self.player_turn else 'O'})")

            if not self.is_multiplayer and not self.player_turn:
                self.ai_turn()

    def ai_turn(self):
        if all(button['state'] == "disabled" for row in self.buttons for button in row):  # Skip if buttons are disabled
            return
    
        ai_row, ai_col = ai_move(self.board)
        if ai_row is not None and ai_col is not None:
            self.board[ai_row][ai_col] = PLAYER_O
            self.buttons[ai_row][ai_col].config(text=PLAYER_O, bg=PLAYER2_COLOR)

            if check_win(self.board, PLAYER_O):
                self.update_stats("AI")
                self.highlight_win_line(PLAYER_O)
                return

            if is_board_full(self.board):
                self.update_stats("draw")
                self.show_stats_screen("It's a draw!")
                return

            self.player_turn = True
            self.notification_label.config(text=f"{self.player1_name}'s Turn (X)")

    def disable_all_buttons(self):
        """Disable all buttons on the board."""
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]:
                    self.buttons[i][j].config(state="disabled")

    def highlight_win_line(self, player):
        win_line = get_win_line(self.board, player)
        if win_line:
            for row, col in win_line:
                self.buttons[row][col].config(bg=WIN_COLOR)
            
            self.disable_all_buttons()
            self.root.after(2000, self.show_stats_screen, f"{self.player1_name if player == PLAYER_X else self.player2_name} wins!")

    def update_stats(self, winner):
        if winner == self.player1_name:
            self.stats["Player 1"]["wins"] += 1
            self.stats["Player 2"]["losses"] += 1
        elif winner == self.player2_name or winner == "AI":
            self.stats["Player 2"]["wins"] += 1
            self.stats["Player 1"]["losses"] += 1
        else:  # Draw
            self.stats["Player 1"]["draws"] += 1
            self.stats["Player 2"]["draws"] += 1

    def show_stats_screen(self, result_message):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Game Stats", font=("Arial", 16), bg=BACKGROUND_COLOR).pack(pady=10)
        tk.Label(frame, text=result_message, font=("Arial", 14), bg=BACKGROUND_COLOR).pack(pady=5)

        stats_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        stats_frame.pack(pady=10)

        tk.Label(stats_frame, text="Player", font=("Arial", 12, "bold"), bg=BACKGROUND_COLOR, width=10).grid(row=0, column=0)
        tk.Label(stats_frame, text="Wins", font=("Arial", 12, "bold"), bg=BACKGROUND_COLOR, width=10).grid(row=0, column=1)
        tk.Label(stats_frame, text="Losses", font=("Arial", 12, "bold"), bg=BACKGROUND_COLOR, width=10).grid(row=0, column=2)
        tk.Label(stats_frame, text="Draws", font=("Arial", 12, "bold"), bg=BACKGROUND_COLOR, width=10).grid(row=0, column=3)

        tk.Label(stats_frame, text=self.player1_name, font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=1, column=0)
        tk.Label(stats_frame, text=self.stats["Player 1"]["wins"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=1, column=1)
        tk.Label(stats_frame, text=self.stats["Player 1"]["losses"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=1, column=2)
        tk.Label(stats_frame, text=self.stats["Player 1"]["draws"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=1, column=3)

        tk.Label(stats_frame, text=self.player2_name, font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=2, column=0)
        tk.Label(stats_frame, text=self.stats["Player 2"]["wins"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=2, column=1)
        tk.Label(stats_frame, text=self.stats["Player 2"]["losses"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=2, column=2)
        tk.Label(stats_frame, text=self.stats["Player 2"]["draws"], font=("Arial", 12), bg=BACKGROUND_COLOR).grid(row=2, column=3)

        tk.Button(frame, text="Play Again", command=self.reset_game).pack(pady=5)
        tk.Button(frame, text="Back to Main Menu", command=self.back_to_main_menu).pack(pady=5)

    def reset_game(self):
        self.reset_all_state() 
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        self.create_game_screen()

    def back_to_main_menu(self):
        self.show_final_results(reset_stats=True)

    def quit_game(self):
        self.show_final_results(quit_after=True)

    def show_final_results(self, quit_after=False, reset_stats=False):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame.pack(expand=True)

        tk.Label(frame, text="Final Results", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=10)

        stats_frame = tk.Frame(frame, bg=BACKGROUND_COLOR)
        stats_frame.pack(pady=10)

        # Determine the winner
        player1_wins = self.stats['Player 1']['wins']
        player2_wins = self.stats['Player 2']['wins']
        if player1_wins > player2_wins:
            winner_text = f"{self.player1_name} won the game!"
        elif player2_wins > player1_wins:
            winner_text = f"{self.player2_name} won the game!"
        else:
            winner_text = "The game is a draw!"

        # Display winner and stats
        tk.Label(stats_frame, text=winner_text, font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR).pack(pady=5)
        tk.Label(stats_frame, text=f"{self.player1_name} Wins: {player1_wins}", 
                 font=("Arial", 14), bg=BACKGROUND_COLOR).pack(pady=5)
        tk.Label(stats_frame, text=f"{self.player2_name} Wins: {player2_wins}", 
                 font=("Arial", 14), bg=BACKGROUND_COLOR).pack(pady=5)
        tk.Label(stats_frame, text=f"Draws: {self.stats['Player 1']['draws']}", 
                 font=("Arial", 14), bg=BACKGROUND_COLOR).pack(pady=5)

        if not quit_after:
            tk.Button(frame, text="Back to Main Menu", 
                      command=lambda: self.reset_stats_and_return_to_menu(reset_stats)).pack(pady=10)
        else:
            tk.Button(frame, text="Exit Game", command=self.root.quit).pack(pady=10)

    def reset_stats_and_return_to_menu(self, reset_stats):
        if reset_stats:
            self.stats = {"Player 1": {"wins": 0, "losses": 0, "draws": 0},
                          "Player 2": {"wins": 0, "losses": 0, "draws": 0}}
        self.create_welcome_screen()

    def reset_all_state(self):
        """Reset all game state variables."""
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.player_turn = True  # Player 1 starts by default
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.notification_label = None

# Helper Functions
def check_win(board, player):
    return (
        any(all(board[i][j] == player for j in range(3)) for i in range(3)) or  # Horizontal
        any(all(board[j][i] == player for j in range(3)) for i in range(3)) or  # Vertical
        all(board[j][j] == player for j in range(3)) or  # Diagonal \
        all(board[j][2 - j] == player for j in range(3))  # Diagonal /
    )


def get_win_line(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Horizontal
            return [(i, j) for j in range(3)]
        if all(board[j][i] == player for j in range(3)):  # Vertical
            return [(j, i) for j in range(3)]
    if all(board[j][j] == player for j in range(3)):  # Diagonal \
        return [(j, j) for j in range(3)]
    if all(board[j][2 - j] == player for j in range(3)):  # Diagonal /
        return [(j, 2 - j) for j in range(3)]
    return None

def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def ai_move(board):
    best_eval = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                evaluation = minimax(board, 0, False)
                board[i][j] = EMPTY
                if evaluation > best_eval:
                    best_eval = evaluation
                    best_move = (i, j)
    return best_move

def minimax(board, depth, is_maximizing):
    if check_win(board, PLAYER_X):
        return -1
    if check_win(board, PLAYER_O):
        return 1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    evaluation = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_eval = max(best_eval, evaluation)
        return best_eval
    else:
        best_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    evaluation = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_eval = min(best_eval, evaluation)
        return best_eval

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
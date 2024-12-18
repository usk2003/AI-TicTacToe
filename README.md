# Tic Tac Toe Game

A simple graphical Tic Tac Toe game built with Python using the Tkinter library. The game offers both single-player (against AI) and multiplayer modes, and keeps track of player statistics like wins, losses, and draws. It also highlights the winning line when a player wins.

## Features

- **Single-Player Mode**: Play against an AI that uses the Minimax algorithm for optimal moves.
- **Multiplayer Mode**: Play against another player on the same device.
- **Game Stats**: Keeps track of wins, losses, and draws for both players.
- **Winning Line Highlight**: Automatically highlights the winning line after a player wins.
- **Dynamic Interface**: The game interface updates automatically based on player turns and results.
- **Reset Game**: Option to reset the game and start a new match at any time.

## Requirements

- Python 3.x
- Tkinter library (comes pre-installed with Python)

## How to Play

1. **Start the Game**: On the welcome screen, choose either "Play with AI" or "Multiplayer" to start the game.
2. **Choose Player Names**: Enter the names of Player 1 and Player 2 (for multiplayer) or just Player 1 (for AI).
3. **Gameplay**: 
   - Player 1 will always be 'X' and Player 2 will be 'O'.
   - Players take turns clicking the buttons on the grid to place their marks.
4. **Winning**:
   - The first player to align 3 of their marks in a row, column, or diagonal wins.
   - The winning line will be highlighted.
5. **Draw**:
   - If the board is full and there’s no winner, the game ends in a draw.
6. **Statistics**: 
   - The game tracks wins, losses, and draws for each player and displays the stats after each round.

## Gameplay Modes

- **Single-Player (AI)**: You play against the computer, where the AI uses the Minimax algorithm to make optimal moves.
- **Multiplayer**: Two players can play on the same device. Player 1 is 'X' and Player 2 is 'O'.

## AI Algorithm

The AI uses the Minimax algorithm to calculate the best possible move for the computer (Player O). It evaluates the game tree to choose the most optimal move, ensuring the best chances for the computer to win or tie.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and create a pull request. Contributions are welcome!

## Acknowledgments

This project was built using Python and Tkinter.  
Thanks to the open-source community for providing resources to help build this game.

## Clone the Repository

To clone this repository to your local machine, run the following command:

```bash
git clone https://github.com/usk2003/AI-TicTacToe_V2.git


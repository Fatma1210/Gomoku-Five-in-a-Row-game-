# Gomoku Game with AI (Minimax & Alpha-Beta Pruning)

This project is a Python implementation of the classic Gomoku (Five-in-a-Row) board game with AI opponents using the Minimax algorithm and Minimax enhanced with Alpha-Beta pruning.

## Features

- **Game Modes:**  
  - Human vs AI  
  - AI vs AI  

- **AI Logic:**  
  - Uses the Minimax algorithm with a heuristic evaluation function to choose optimal moves.  
  - Alpha-Beta pruning is applied to improve search efficiency during AI vs AI matches.  
  - Valid moves are generated based on a proximity radius around previously played moves to optimize performance.

- **Board and Gameplay:**  
  - The board is represented as a 15x15 grid.  
  - Players take turns placing their markers ('X' for human or AI 1, 'O' for AI 2).  
  - The game checks for wins (five consecutive markers horizontally, vertically, or diagonally) or draws.  

## Code Overview

- **Board Management:**  
  - `CreateBoard()` initializes the board.  
  - `applyMove()` returns a new board state after a player’s move.  
  - `GetValidMoves()` generates all valid moves within a certain radius of played moves for efficiency.

- **Game Logic:**  
  - `isWin()`, `isDraw()`, and `isGameOver()` detect game-ending conditions.  
  - `CountConsecutive()` and `EvaluateHeuristic()` help evaluate board positions to guide AI decisions.

- **AI Algorithms:**  
  - `Minimax()` implements the standard minimax recursive search.  
  - `Minimax_alpha_beta()` improves upon it using alpha-beta pruning to cut off branches and speed up decision-making.  
  - `findBestMove()` and `findBestMove_alpha_beta()` select the optimal move for the AI players.

- **Gameplay Functions:**  
  - `HumanvsAiGame()` handles interactive play between a human player and AI.  
  - `AIvsAIGame()` runs automated matches between two AI players.  

- **Main Entry Point:**  
  - `main()` prompts the user to select the game mode and runs the appropriate function.

## How to Run

1. Make sure you have Python installed (tested with Python 3.7+).
2. Install NumPy if not already installed:

# Ai-Games
Tictactoe with Monte Carlo Tree search and 2048
Here is the README.md for the given code:

```markdown
# Tic Tac Toe with Monte Carlo Tree Search

This repository contains a Python implementation of the Tic Tac Toe game with an AI opponent using Monte Carlo Tree Search (MCTS).

## Features

- Play Tic Tac Toe against an AI opponent
- AI uses Monte Carlo Tree Search for decision making
- Command-line interface for game interaction

## Usage

To play the game, run the script and follow the on-screen instructions:

```
python tic_tac_toe.py
```

Enter moves in the format "x,y" where x and y are coordinates on the 3x3 grid (1-3).

Type 'exit' to quit the game.

## Dependencies

- Python 3.x
- `practice_mcts` module (not included in this snippet)

## Code Structure

- `Board` class: Represents the Tic Tac Toe board and game logic
- `game_loop` method: Handles the main game loop and user interactions
- MCTS implementation is utilized for AI moves

## Note

This code is part of a larger system and may require additional modules or modifications to run independently.
```
# 2048 Game Implementation

This repository contains a Python implementation of the popular 2048 game, along with an AI player using Monte Carlo Tree Search (MCTS).

## Features

- Game board representation and manipulation
- Basic game mechanics (moving tiles, merging, spawning new numbers)
- Console-based user interface for manual play
- AI player using MCTS for automated gameplay

## File Structure

- `Board` class: Implements the game logic and board manipulation
- MCTS implementation (imported from `mcts_random.py`, not included in this snippet)

## Usage

To play the game manually:

```python
board = Board()
board.game_loop()
```

To watch the AI play:

```python
board = Board()
board.game_loop_ai()
```

## Note

This code is a part of a larger system and may require additional files or modifications to run independently.

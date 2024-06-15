# Sudoku Solver and Player

This project is a graphical Sudoku game implemented using Python's Tkinter library. It includes options to clear the board, solve the puzzle using two different algorithms (Backtracking and AC-3), and select different Sudoku puzzles to play with.

## Features

- **Graphical User Interface**: Provides a simple interface for playing Sudoku.
- **Puzzle Loading**: Load puzzles from files.
- **Solve Puzzle**: Solve the puzzle using Backtracking or AC-3 algorithms.
- **Clear Board**: Clear the current board to start over.
- **Algorithm Selection**: Choose between Backtracking and AC-3 algorithms to solve the puzzle.
- **Puzzle Selection**: Choose from predefined puzzles (`debug`, `n00b`, `l33t`, `error`).

## Requirements

- Python 3.x
- Tkinter (Usually comes pre-installed with Python on most systems)
- argparse (Standard library module)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/tahirch0udhary/Soduko-Puzzle-using-AC3-and-Backtracking-Agorithm
    ```

2. **Install dependencies** (if not already available):

    Tkinter should be available by default, but if it's not, you can install it using your package manager:

    - On **Debian-based systems** (e.g., Ubuntu):

      ```bash
      sudo apt-get install python3-tk
      ```

    - On **Red Hat-based systems** (e.g., Fedora):

      ```bash
      sudo dnf install python3-tkinter
      ```

    - On **macOS**:

      ```bash
      brew install python-tk
      ```

    - On **Windows**:

      Tkinter is included with Python's standard installation.

## Usage

1. **Run the application**:

    Navigate to the project directory and execute:

    ```bash
    python3 sudoku_solver.py --board <board_name>
    ```

    Replace `<board_name>` with one of the available puzzles: `debug`, `n00b`, `l33t`, `error`.

2. **Interact with the GUI**:

    - **Load Puzzle**: Select a puzzle from the dropdown menu.
    - **Select Algorithm**: Choose an algorithm (Backtracking or AC-3) from the dropdown menu.
    - **Solve Puzzle**: Click the "Solve puzzle" button to solve the current puzzle.
    - **Clear Board**: Click the "Clear answers" button to clear the current answers on the board.

## File Structure

- **`sudoku_solver.py`**: Main script containing the game logic and Tkinter UI.
- **`<board_name>.sudoku`**: Puzzle files containing the initial state of the Sudoku puzzles.
- **`README.md`**: This readme file.

## Project Structure

- **`SudokuUI` class**: Manages the graphical user interface and user interactions.
- **`SudokuGame` class**: Manages the game state and logic for checking the winning condition.
- **`SudokuBoard` class**: Represents the Sudoku board and initializes it from a file.
- **`solve_sudoku_backtracking` function**: Solves the Sudoku puzzle using a backtracking algorithm.
- **`solve_sudoku_AC3` function**: Solves the Sudoku puzzle using the AC-3 algorithm.

## Sudoku File Format

Each Sudoku puzzle file should contain 9 lines, each with 9 characters. Each character represents a cell in the Sudoku grid, where '0' denotes an empty cell.

Example content for `debug.sudoku`:


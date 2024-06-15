import argparse
from tkinter import Tk, Canvas, Frame, Button, Label, OptionMenu, StringVar, BOTH, TOP, LEFT, RIGHT
import time

# Global variables for Sudoku board size and margins
MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class SudokuError(Exception):
    """
    An application specific error.
    """
    pass

class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1
        self.solve_time = 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(side=LEFT, padx=5)
        solve_button = Button(self,
                              text="Solve puzzle",
                              command=self.__solve_puzzle)
        solve_button.pack(side=LEFT, padx=5)

        # Option menu for puzzle selection
        self.puzzle_var = StringVar(self)
        self.puzzle_var.set("Select Puzzle")  # Default value
        puzzle_menu = OptionMenu(self, self.puzzle_var, "debug", "n00b", "l33t", "error", command=self.__load_puzzle)
        puzzle_menu.pack(side=LEFT, padx=5)

        # Option menu for algorithm selection
        self.algorithm_var = StringVar(self)
        self.algorithm_var.set("Backtracking")  # Default value
        algorithm_menu = OptionMenu(self, self.algorithm_var, "Backtracking", "AC-3")
        algorithm_menu.pack(side=LEFT, padx=5)

        self.time_label = Label(self, text="Time taken: ")
        self.time_label.pack(side=RIGHT, padx=5)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __load_puzzle(self, event=None):
        puzzle_name = self.puzzle_var.get()
        with open('%s.sudoku' % puzzle_name, 'r') as puzzle_file:
            self.game = SudokuGame(puzzle_file)
            self.game.start()
            self.__draw_puzzle()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()

    def __solve_puzzle(self):
        if self.algorithm_var.get() == "Backtracking":
            solve_method = solve_sudoku_backtracking
        elif self.algorithm_var.get() == "AC-3":
            solve_method = solve_sudoku_AC3
        else:
            print("Invalid algorithm selection")
            return

        start_time = time.time()
        solved = solve_method(self.game.puzzle)
        end_time = time.time()
        self.solve_time = end_time - start_time
        print("Time taken to solve the puzzle:", self.solve_time)
        self.time_label.config(text="Time taken: {:.4f} seconds".format(self.solve_time))
        if solved:
            self.__draw_puzzle()
            if self.game.check_win():
                self.__draw_victory()
        else:
            print("Failed to solve the puzzle")

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board

class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board
        self.puzzle = []
        self.game_over = False

    def start(self):
        self.game_over = False
        self.puzzle = [row[:] for row in self.start_puzzle]

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )

# Backtracking Algorithm
def solve_sudoku_backtracking(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    else:
        row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve_sudoku_backtracking(board):
                return True

            board[row][col] = 0

    return False

def is_valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

# AC-3 solving algorithm wrapper
def solve_sudoku_AC3(board):
    # Convert the board to a list of lists of lists (3D list)
    csp = [[[board[i][j] if board[i][j] != 0 else list(range(1, 10)) for j in range(9)] for i in range(9)]]
    if AC3(csp):
        for i in range(9):
            for j in range(9):
                board[i][j] = csp[0][i][j] if len(csp[0][i][j]) == 1 else 0
        return True
    return False

def AC3(csp):
    queue = [(i, j) for i in range(9) for j in range(9)]
    while queue:
        row, col = queue.pop(0)
        if csp[0][row][col] == 0:
            continue
        value = csp[0][row][col]
        if REVISE(csp, row, col, value):
            if all(csp[0][i][j] != 0 for i in range(9) for j in range(9)):
                return True
            for i in range(9):
                for j in range(9):
                    if csp[0][i][j] == 0:
                        queue.append((i, j))
    return False

def REVISE(csp, row, col, value):
    revised = False
    for i in range(9):
        if csp[0][row][i] == value and i != col:
            csp[0][row][i] = 0
            revised = True
        if csp[0][i][col] == value and i != row:
            csp[0][i][col] = 0
            revised = True
    for i in range(row // 3 * 3, row // 3 * 3 + 3):
        for j in range(col // 3 * 3, col // 3 * 3 + 3):
            if csp[0][i][j] == value and (i, j) != (row, col):
                csp[0][i][j] = 0
                revised = True
    return revised

# Parse command line arguments
def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            choices=['debug', 'n00b', 'l33t', 'error'],
                            required=True)
    args = vars(arg_parser.parse_args())
    return args['board']

if __name__ == '__main__':
    board_name = parse_arguments()

    # Load Sudoku board from file
    with open('%s.sudoku' % board_name, 'r') as boards_file:
        game = SudokuGame(boards_file)
        game.start()

        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()

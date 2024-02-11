import tkinter as tk
import time
from tkinter import messagebox


def update_entry(row, col, value, delay=0):
    entry = root.grid_slaves(row=row, column=col)[0]
    entry.delete(0, tk.END)
    entry.insert(0, str(value))
    root.update()
    time.sleep(delay / 1000)


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            # Add delay and update the entry
            update_entry(row, col, i, delay=150)

            if forward_checking(bo, (row, col)) and solve(bo):
                return True

            bo[row][col] = 0
            # Add delay and reset the entry
            update_entry(row, col, 0, delay=150)

    return False


def forward_checking(bo, pos):
    for i in range(len(bo[0])):
        if i != pos[1] and bo[pos[0]][i] == 0:
            if not is_value_possible(bo, pos[0], i):
                return False

    for i in range(len(bo)):
        if i != pos[0] and bo[i][pos[1]] == 0:
            if not is_value_possible(bo, i, pos[1]):
                return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (i, j) != pos and bo[i][j] == 0:
                if not is_value_possible(bo, i, j):
                    return False

    return True


def is_value_possible(bo, row, col):
    for value in range(1, 10):
        if valid(bo, value, (row, col)):
            return True
    return False


class SudokuGUI:
    def __init__(self, root, board):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = board
        self.create_board()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=(
                    'Arial', 18), justify='center', readonlybackground='lightgray')
                entry.grid(row=i, column=j, ipadx=5, ipady=5)
                entry.insert(0, str(self.board[i][j]))
                if self.board[i][j] != 0:
                    entry.config(state='readonly')

        solve_button = tk.Button(
            self.root, text="Solve", command=self.solve_board)
        solve_button.grid(row=10, column=4, columnspan=2)

    def solve_board(self):
        solve(self.board)
        self.update_board()
        # Display a message when the puzzle is solved
        tk.messagebox.showinfo("Sudoku Solver", "Puzzle Solved!")

    def update_board(self):
        for i in range(9):
            for j in range(9):
                entry = self.root.grid_slaves(row=i, column=j)[0]
                entry.delete(0, tk.END)
                entry.insert(0, str(self.board[i][j]))
                if self.board[i][j] != 0:
                    entry.config(state='readonly')


if __name__ == "__main__":
    root = tk.Tk()

    # Example Sudoku board
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    app = SudokuGUI(root, board)
    root.mainloop()

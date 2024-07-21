import random
import time


def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board, row=0, col=0):
    if row == 9 - 1 and col == 9:
        return True
    if col == 9:
        row += 1
        col = 0
    if board[row][col] != 0:
        return solve_sudoku(board, row, col + 1)
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board, row, col + 1):
                return True
            board[row][col] = 0
    return False


def generate_full_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    return board


def generate_sudoku_with_clues(clues=17, seed=None):
    # Use seed to avoid deterministic generation
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())

    # Generate a full Sudoku board
    full_board = generate_full_sudoku()

    # Remove numbers to leave exactly `clues` clues
    sudoku_with_clues = remove_numbers(full_board, clues=clues)

    return sudoku_with_clues

def remove_numbers(board, clues=17):
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    removed = 0

    while removed < 81 - clues:
        row, col = positions.pop()
        if board[row][col] != 0:
            board[row][col] = 0
            removed += 1
        
        # here we don't require the solution 
        # to the board to be unique

    return board


def print_board(board):
    # Outline 3*3 grids
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, cell in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(str(cell) if cell != 0 else '.', end=" ")
        print()



if __name__ == "__main__":
    # Generate a full Sudoku board
    # Remove numbers to leave exactly 17 clues
    sudoku_board_with_17_clues = generate_sudoku_with_clues()

    # Print the generated board
    print("Board generated:")
    print_board(sudoku_board_with_17_clues)

    if solve_sudoku(sudoku_board_with_17_clues):
        print("One solution for this board:")
        print_board(sudoku_board_with_17_clues)
    else:
        print("No solution exists for this board.")
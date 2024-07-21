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


def generate_sudoku(seed=None, initial_number_count=None):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())

    board = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5],
    ]

    def shuffle_numbers():
        for i in range(1, 10):
            n1 = i
            n2 = random.randint(1, 9)
            for y in range(9):
                for x in range(9):
                    if board[y][x] == n1:
                        board[y][x] = n2
                    elif board[y][x] == n2:
                        board[y][x] = n1

    def shuffle_rows():
        for i in range(9):
            block = i // 3
            r2 = block * 3 + random.randint(0, 2)
            board[i], board[r2] = board[r2], board[i]

    def shuffle_cols():
        for i in range(9):
            block = i // 3
            c1 = i
            c2 = block * 3 + random.randint(0, 2)
            for r in range(9):
                board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    def shuffle_3x3_rows():
        for i in range(3):
            r1 = i * 3
            r2 = random.randint(0, 2) * 3
            for j in range(3):
                board[r1 + j], board[r2 + j] = board[r2 + j], board[r1 + j]

    def shuffle_3x3_cols():
        for i in range(3):
            c1 = i * 3
            c2 = random.randint(0, 2) * 3
            for j in range(3):
                for r in range(9):
                    board[r][c1 + j], board[r][c2 + j] = board[r][c2 + j], board[r][c1 + j]

    def remove_numbers():
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        while positions:
            row, col = positions.pop()
            backup = board[row][col]
            board[row][col] = 0
            if count_solutions(board) != 1:
                board[row][col] = backup
    
    def remove_numbers_until(clues=17):
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        removed = 0

        while removed < 81 - clues:
            row, col = positions.pop()
            if board[row][col] != 0:
                board[row][col] = 0
                removed += 1

        return board

    def count_solutions(board):
        solutions = 0

        def solve_and_count(board, row=0, col=0):
            nonlocal solutions
            if row == 9:
                solutions += 1
                return True
            if col == 9:
                return solve_and_count(board, row + 1, 0)
            if board[row][col] != 0:
                return solve_and_count(board, row, col + 1)
            for num in range(1, 10):
                if is_safe(board, row, col, num):
                    board[row][col] = num
                    if solve_and_count(board, row, col + 1):
                        if solutions > 1:
                            return False
                    board[row][col] = 0
            return False

        solve_and_count(board)
        return solutions

    shuffle_numbers()
    shuffle_rows()
    shuffle_cols()
    shuffle_3x3_rows()
    shuffle_3x3_cols()
    if initial_number_count:
        print("here!")
        remove_numbers_until(clues=initial_number_count)
    else:
        remove_numbers()

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
    sudoku_board_with_17_clues = generate_sudoku(initial_number_count=17)

    # Print the generated board
    print("Board generated:")
    print_board(sudoku_board_with_17_clues)

    if solve_sudoku(sudoku_board_with_17_clues):
        print("One solution for this board:")
        print_board(sudoku_board_with_17_clues)
    else:
        print("No solution exists for this board.")

    # Generate a full Sudoku board
    # Remove numbers until the solution is detected to be no longer unique
    sudoku_board = generate_sudoku()

    # Print the generated board
    print("Board generated:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("One solution for this board:")
        print_board(sudoku_board)
    else:
        print("No solution exists for this board.")
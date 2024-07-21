def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


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


if __name__ == "__main__":
    # Initialize the board to a previous failure case
    board = [
        [8, 0, 0, 0, 4, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 9, 0, 6, 7, 0, 0, 3],
        [0, 3, 0, 9, 2, 0, 0, 8, 0],
        [6, 8, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 6],
        [2, 9, 5, 7, 8, 6, 3, 4, 1],
        [7, 6, 8, 1, 3, 4, 5, 9, 2],
        [1, 4, 3, 2, 5, 9, 8, 6, 7]
    ]

    print("Board:")
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))

    solutions_count = count_solutions(board)
    print(f"Number of solutions: {solutions_count}")

import random
import time


def is_safe(board, row, col, num):
    '''Checks if to put <num> at position [rol][col] is valid.'''

    # Check row and column
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    
    # Check corresponding 3*3 block
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(board, row=0, col=0):
    '''
    Tries backtracking to fill up the sudoku board with valid entries.
    Returns a boolean to indicate if a solution can be found.
    '''

    # Check if the board has been successfully filled up
    if row == 9 - 1 and col == 9:
        return True
    
    # Check if we need to move on to the next row
    if col == 9:
        row += 1
        col = 0
    
    # Skip positions that have already been filled
    if board[row][col] != 0:
        return solve_sudoku(board, row, col + 1)
    
    # Try if we can fill in any integer among 1 through 9
    # at the current position
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board, row, col + 1):
                return True
            board[row][col] = 0
    
    return False


def generate_sudoku(seed=None, initial_number_count=None):
    '''
    Generates a solvable sudoku board with some initial numbers filled in.
    The mechanism is to first find a valid full board
    and then delete numbers from positions
    until either there is no unique solution (if no inital_number_count is given)
    or until there is only <initial_number_count> numbers left on board.
    A seed is used for random shuffles.
    '''

    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())

    # This initial full board is a guaranteed solution;
    # we will try to derive another valid solution from it.
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
        '''
        Swap the positions of all <n1> with positions of all <n2>;
        <n1> is from 1 to 9, while <n2> is picked from 1 to 9 randomly.
        '''
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
        '''
        Randomly exchange positions of each row with another row
        within its corresponding row of 3*3 blocks.
        '''
        for i in range(9):
            block = i // 3
            r2 = block * 3 + random.randint(0, 2)
            board[i], board[r2] = board[r2], board[i]

    def shuffle_cols():
        '''
        Randomly exchange positions of each column with another column
        within its corresponding column of 3*3 blocks.
        '''
        for i in range(9):
            block = i // 3
            c1 = i
            c2 = block * 3 + random.randint(0, 2)
            for r in range(9):
                board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    def shuffle_3x3_rows():
        '''Shuffle rows of 3*3 blocks.'''
        for i in range(3):
            r1 = i * 3
            r2 = random.randint(0, 2) * 3
            for j in range(3):
                board[r1 + j], board[r2 + j] = board[r2 + j], board[r1 + j]

    def shuffle_3x3_cols():
        '''Shuffle columns of 3*3 blocks.'''
        for i in range(3):
            c1 = i * 3
            c2 = random.randint(0, 2) * 3
            for j in range(3):
                for r in range(9):
                    board[r][c1 + j], board[r][c2 + j] = board[r][c2 + j], board[r][c1 + j]

    def remove_numbers():
        '''
        Check if the number can be removed without violating the unique-solution constraint
        for all positions in randomized order;
        if so, remove them.
        Ideally there may be only 17 numbers left.
        '''
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        while positions:
            row, col = positions.pop()
            backup = board[row][col]
            board[row][col] = 0
            if count_solutions(board) != 1:
                board[row][col] = backup
    
    def remove_numbers_until(clues=17):
        '''
        Remove numbers in randomized order until there are only <clues> numbers left.
        The solution to the updated board may be non-unique.
        '''
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
        '''
        Tries to fully solve the soduku,
        and count the number of valid solutions in the process.
        Used to examine solution's uniqueness.
        '''
        solutions = 0

        def solve_and_count(board, row=0, col=0):
            nonlocal solutions
            if row == 9:
                solutions += 1
                return
            if col == 9:
                solve_and_count(board, row + 1, 0)
                return
            if board[row][col] != 0:
                solve_and_count(board, row, col + 1)
                return
            for num in range(1, 10):
                if is_safe(board, row, col, num):
                    board[row][col] = num
                    solve_and_count(board, row, col + 1)
                    board[row][col] = 0
                    if solutions > 1:
                        return

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
    '''
    Prints out the current look of the board.
    Dots are used to indicate unfilled positions (with default value 0).
    3*3 blocks are separated. Assume the board size is 9*9.
    '''
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
    print("Board generated with limited initial numbers:")
    print_board(sudoku_board_with_17_clues)

    if solve_sudoku(sudoku_board_with_17_clues):
        print("One solution for this board:")
        print_board(sudoku_board_with_17_clues)
    else:
        print("No solution exists for this board.")

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # Generate a full Sudoku board
    # Remove numbers until the solution is detected to be no longer unique
    sudoku_board = generate_sudoku()

    # Print the generated board
    print("Board generated with a unique solution:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("One solution for this board:")
        print_board(sudoku_board)
    else:
        print("No solution exists for this board.")
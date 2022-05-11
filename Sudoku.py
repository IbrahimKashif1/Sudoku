from dokusan import generators
import numpy as np
import numpy as np

board3 = [
        [0, 1, 0, 0, 0, 2, 0, 0, 8],
        [5, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 9, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 8, 0, 5, 6, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 4],
        [3, 6, 0, 0, 5, 4, 0, 0, 0],
        [2, 0, 8, 0, 0, 0, 0, 5, 3],
        [0, 0, 6, 0, 0, 0, 0, 8, 0],
        [0, 0, 1, 0, 0, 0, 4, 0, 9]
    ]

def random_board(y):
    if y == 1:
        board = np.array(list(str(generators.random_sudoku(avg_rank=40))))
    if y == 2:
        board = np.array(list(str(generators.random_sudoku(avg_rank=150))))
    if y == 3:
        board = np.array(list(str(generators.random_sudoku(avg_rank=450))))
    board5 = board.reshape(9, 9)
    board5 = board5.astype(int)
    return board5


def create_board():
    collumns = 9
    rows = 9
    board = {}
    for x in range(0, collumns):
        board[x] = {}
        for y in range(0, rows):
            print("Enter value between 1 and 9 or enter 0 if it is blank")
            val = int(input())
            board[x][y] = val

    return board


def complete(board):
    board_complete = curr_empty_box(board)
    if not board_complete:
        return True
    else:
        row, col = board_complete

    for i in range(1, 10):
        if valid_sol(board, (row, col), i):
            board[row][col] = i
            if complete(board):
                return True
            board[row][col] = 0
    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def valid_sol(board, position, value):
    x = position[0] // 3
    y = position[1] // 3
    for i in range(len(board[0])):
        if board[position[0]][i] == value and position[1] != i:
            return False

    for i in range(len(board)):
        if board[i][position[1]] == value and position[0] != i:
            return False

    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if board[i][j] == value and (i, j) != position:
                return False

    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end = "")


def curr_empty_box(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def board_impossible(board):
    board_sol = complete(board)
    if board_sol == True:
        print("Solution")
    else:
        print("No Solution exists")

# Asks user for input
print("If you would like random sudoku board press 1.")
print("If you would like to create your own sudoku board press 2.")
print("If you would like pre-made sudoku board press 3.")

# Assigns value to x
x = int(input())

# Checks which sudoku board to play and finds the correct solution
if x == 1:
    while(True):
        print("What difficulty would you like to play easy(1), medium(2) or hard(3).")
        y = int(input())
        if y == 1 or y == 2 or y == 3:
            break
    board1 = random_board(y)
    print("Initial board")
    print_board(board1)
    print("")
if x == 2:
    y = 1
    board1 = random_board(y)
if x == 3:
    y = 1
    board1 = random_board(y)
    print("Initial board")
    print_board(board3)
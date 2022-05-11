import pygame
import time
from Sudoku import complete, valid_sol, x, board1, create_board, print_board

pygame.font.init()

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

if x == 1:
    board4 = board1
elif x == 2:
    board4 = create_board()
    print("Initial board")
    print_board(board4)
elif x == 3:
    board4 = board3


class Grid:
    board = board4

    def __init__(self, rows, columns, width, height, win):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.blocks = [[Block(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]
        self.model = None
        self.selected = None
        self.update_model()
        self.win = win

    def update_model(self):
        self.model = [[self.blocks[i][j].fixedval for j in range(self.columns)] for i in range(self.rows)]

    def place(self, val):
        row, column = self.selected
        if self.blocks[row][column].fixedval == 0:
            self.blocks[row][column].fix_value(val)
            self.update_model()

            if valid_sol(self.model, (row, column), val) and complete(self.model):
                return True
            else:
                self.blocks[row][column].fix_value(0)
                self.blocks[row][column].curr_temp_value(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, column = self.selected
        self.blocks[row][column].curr_temp_value(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Blocks
        for i in range(self.rows):
            for j in range(self.columns):
                self.blocks[i][j].draw(win)

    def select(self, row, column):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.columns):
                self.blocks[i][j].selected = False

        self.blocks[row][column].selected = True
        self.selected = (row, column)

    def clear(self):
        row, column = self.selected
        if int(self.blocks[row][column].value) == 0:
            self.blocks[row][column].curr_temp_value(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[1] // gap
            y = pos[0] // gap
            return (int(x), int(y))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.blocks[i][j].fixedval == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid_sol(self.model, (row, col), i):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid_sol(self.model, (row, col), i):
                self.model[row][col] = i
                self.blocks[row][col].fix_value(i)
                self.blocks[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.blocks[row][col].fix_value(0)
                self.update_model()
                self.blocks[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Block:
    rows = 9
    column = 9

    def __init__(self, value, row, column, width, height):
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.fixedval = value
        self.tempval = 0
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.column * gap
        y = self.row * gap

        if self.fixedval == 0 and self.tempval != 0:
            text = font.render(str(self.tempval), 1, (128, 128, 128))
            win.blit(text, ((x + 5), (y + 5)))
        elif not(self.fixedval == 0):
            text = font.render(str(self.fixedval), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("arial1", 40)

        gap = self.width / 9
        x = self.column * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.fixedval), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def fix_value(self, val):
        self.fixedval = val

    def curr_temp_value(self, val):
        self.tempval = val

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def redraw_window(win, board, time1, wrong):
    win.fill((255, 255, 255))
    # Time elapsed
    font = pygame.font.SysFont("arial", 40)
    text = font.render("Time : " + format_time(time1), 1, (0, 0, 0))
    win.blit(text, (20, 540))
    # No of errors
    text = font.render("Wrong: " + str(wrong), 1, (0, 0, 0))
    win.blit(text, (330, 540))
    # Draws grid
    board.draw(win)

def format_time(secs):
    minute = secs // 60
    hour = minute // 60
    sec = secs % 60

    if minute >= 60:
        minute = minute - (hour * 60)
        time1 = " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    else:
        time1 = " " + str(minute) + ":" + str(sec)
    return time1

def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    con = True
    key = None
    start = time.time()
    wrong = 0
    while con:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                con = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.blocks[i][j].tempval != 0:
                        if board.place(board.blocks[i][j].tempval):
                            print("Correct")
                        elif (board.blocks[i][j].fixedval):
                            print("Error cannot replace value")
                        else:
                            print("Wrong")
                            wrong = wrong + 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            con = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                click = board.click(position)
                if click:
                    board.select(click[0], click[1])
                    key = None

        if key != None and board.selected:
            board.sketch(key)

        redraw_window(win, board, play_time, wrong)
        pygame.display.update()

main()
pygame.quit()

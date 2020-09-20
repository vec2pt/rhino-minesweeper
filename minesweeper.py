import rhinoscriptsyntax as rs

import random

def empty_cells(board):
    cells = []
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:
                cells.append((x, y))
    return cells


def cells_around(r, c, dim):
    cells = []
    if r-1 >= 0: r1 = r-1
    else: r1 = r
    if r+2 <= dim: r2 = r+2
    else: r2 = r+1
    if c-1 >= 0: c1 = c-1
    else: c1 = c
    if c+2 <= dim: c2 = c+2
    else: c2 = c+1
    for x in range(r1, r2):
        for y in range(c1, c2):
            cells.append((x, y))
    return cells


def create_board(dim, mines, scale=10):
    board = [[0 for j in range(dim)] for i in range(dim)]
    mask = [[False for j in range(dim)] for i in range(dim)]
    grid = [[0 for j in range(dim)] for i in range(dim)]
    mines_indexs = []
    for m in range(mines):
        cells = empty_cells(board)
        x, y = random.choice(cells)
        board[x][y], mask[x][y] = 'Mine', True
        mines_indexs.append((x, y))
    for i, j in mines_indexs:
        for x, y in cells_around(i, j, dim):
            if board[x][y] != 'Mine':
                board[x][y] += 1
    for i in range(dim):
        for j in range(dim):
            x = i*scale + scale/2
            y = j*scale + + scale/2
            textdot_id = rs.AddTextDot('', (x, y, 0))
            grid[i][j] = textdot_id
    return board, mask, grid


def check_mask(mask):
    test = 0
    for i in range(len(mask)):
        for j in range(len(mask)):
            if not mask[i][j]:
                test += 1
    return test == 0


def destroy_grid((x, y), grid, scale=10):
    max_dist = scale*4
    for i in range(len(grid)):
        for j in range(len(grid)):
            try:
                p1 = rs.TextDotPoint(grid[x][y])
                p2 = rs.TextDotPoint(grid[i][j])
                dist = rs.Distance(p1, p2)
                if dist < max_dist:
                    dist = (max_dist - dist)/(max_dist/1.5)
                    vect = rs.VectorCreate(p2, p1)
                    vect = rs.VectorScale(vect, dist)
                    rs.MoveObject(grid[i][j], vect)
            except: None


def turn(board, mask, grid):
    test = True
    textdot_id = rs.GetObject("", rs.filter.textdot)
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] == textdot_id:
                i, j = x, y
    if board[i][j] == 'Mine':
        destroy_grid((i, j), grid)
        rs.TextDotText(textdot_id, board[i][j])
        rs.MessageBox("Game over! :(", title='Rhino Minesweeper')
        test = False
    elif board[i][j] == 0:
        board_copy = [row[:] for row in board]
        cells_test = cells_0(i, j, board_copy, [])
        for x, y in cells_test:
            if not mask[x][y]:
                if board[x][y] == 0:
                    rs.DeleteObject(grid[x][y])
                else:
                    rs.TextDotText(grid[x][y], board[x][y])
            mask[x][y] = True
    else:
        rs.TextDotText(textdot_id, board[i][j])
        mask[i][j] = True
    if test and check_mask(mask):
        rs.MessageBox("You win!", title='Rhino Minesweeper')
        return False
    else: return test


def cells_0(i, j, board_copy, cells=[]):
    for x, y in cells_around(i, j, len(board_copy)):
        if board_copy[x][y] == 0:
            board_copy[x][y] = '-'
            cells_0(x, y, board_copy, cells)
        else:
            board_copy[x][y] = '-'
            if (x,y) not in cells:
                cells.append((x,y))
    return cells


def set_level():
    levels = {
        "Easy": (8, 10),
        "Medium": (16, 40),
        "Hard": (24, 99)}
    return levels[rs.ListBox(levels.keys(), 'Select difficulty:', 'Rhino Minesweeper')]


def minesweeper():
    dim, mines = set_level()
    board, mask, grid = create_board(dim, mines, scale=10)
    test = turn(board, mask, grid)
    while test:
        test = turn(board, mask, grid)


if __name__ == "__main__":
    minesweeper()

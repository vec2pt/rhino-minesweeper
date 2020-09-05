import rhinoscriptsyntax as rs

import random


def empty_cells(board):
    cells = []
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                cells.append((r, c))
    return cells


def cells_around(r, c, board):
    cells = []
    if r-1 >= 0: r1 = r-1
    else: r1 = r
    if r+2 <= len(board): r2 = r+2
    else: r2 = r+1
    if c-1 >= 0: c1 = c-1
    else: c1 = c
    if c+2 <= len(board): c2 = c+2
    else: c2 = c+1
    for x in range(r1, r2):
        for y in range(c1, c2):
            cells.append((x, y))
    return cells


def create_board(dim, mines):
    board = [[0 for j in range(dim)] for i in range(dim)]
    mines_indexs = []
    for b in range(mines):
        cells = empty_cells(board)
        r, c = random.choice(cells)
        board[r][c] = 'Mine'
        mines_indexs.append((r, c))
    for r, c in mines_indexs:
        for x, y in cells_around(r, c, board):
            if board[x][y] != 'Mine':
                board[x][y] += 1
    return board

def draw_board(board, scale=10):
    grid = []
    for i in range(len(board)):
        i_list = []
        for j in range(len(board)):
            x = i*scale
            y = j*scale
            temp_o1 = rs.AddRectangle((x, y, 0), scale, scale)
            mid_point = rs.CurveMidPoint(temp_o1)
            temp_o2 = rs.OffsetCurve(temp_o1, mid_point, 0.05*scale)
            temp_o3 = rs.AddLine((x, y, 0), (x, y, 1))
            extrude = rs.ExtrudeCurve(temp_o2, temp_o3)
            rs.CapPlanarHoles(extrude)
            rs.DeleteObjects((temp_o1, temp_o2, temp_o3))
            i_list.append((extrude, (x + scale/2, y + scale/2, 0)))
        grid.append(i_list)
    return grid


def turn(board, grid):
    o = rs.GetObject("", rs.filter.polysurface)
    for i in range(len(board)):
        for j in range(len(board)):
            if o == grid[i][j][0]:
                if board[i][j] == 'Mine':
                    rs.DeleteObject(grid[i][j][0])
                    rs.AddTextDot(str(board[i][j]), grid[i][j][1])
                    rs.MessageBox("Game over! :(")
                    return False
                elif board[i][j] == 0:
                    board_copy = [row[:] for row in board]
                    cells_test = list(set(cells_0(i, j, board_copy, [])))
                    for x, y in cells_test:
                        rs.DeleteObject(grid[x][y][0])
                        if board[x][y] !=0 and board[x][y] !='':
                            rs.AddTextDot(str(board[x][y]), grid[x][y][1])
                        board[x][y] = ''
                    if check_board(board):
                        return True
                    else:
                        rs.MessageBox("You win!")
                        return False
                else:
                    rs.DeleteObject(grid[i][j][0])
                    rs.AddTextDot(str(board[i][j]), grid[i][j][1])
                    board[i][j] = ''
                    if check_board(board):
                        return True
                    else:
                        rs.MessageBox("You win!")
                        return False


def cells_0(i, j, board_copy, cells=[]):
    for x, y in cells_around(i, j, board_copy):
        if board_copy[x][y] == 0:
            board_copy[x][y] = '-'
            cells_0(x, y, board_copy, cells)
        else:
            board_copy[x][y] = '+'
            cells.append((x,y))
    return cells


def set_level():
    levels = {
        "Easy": (8, 10),
        "Medium": (16, 40),
        "Hard": (24, 99)}
    return levels[rs.ListBox(levels.keys())]

def check_board(board):
    test = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 'Mine' and board[i][j] != '':
                test += 1
    if test != 0:
        return True
    else:
        return False


def minesweeper():
    dim, mines = set_level()
    board = create_board(dim, mines)
    grid = draw_board(board)
    player_turn = turn(board, grid)
    while player_turn:
        player_turn = turn(board, grid)


if __name__ == "__main__":
    minesweeper()

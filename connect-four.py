from turtle import *
from state import *
from check_win import is_win

f = open("game.txt","r")

print(f.read())
f = open("game2.txt", "w")
f.write("Now the file has more content!")
f.close()


def line(a, b, x, y):
    up()
    goto(a, b)
    down()
    goto(x, y)


def grid():
    Screen().bgcolor('Blue')
    for x in range(-150, 200, 50):
        line(x, -200, x, 200)

    for x in range(-175, 200, 50):
        for y in range(-175, 200, 50):
            up()
            goto(x, y)
            dot(40, 'white')

    update()


turns = {'red': 'yellow', 'yellow': 'red'}
state = State()


def tap(x, y):
    player = state.player
    slots = state.slots
    grid = state.grid

    slot = int((x + 200) // 50)
    count = slots[slot]

    if count >= len(grid):
        print
        "No more space, match draw"
        return

    x = ((x + 200) // 50) * 50 - 200 + 25
    y = count * 50 - 200 + 25

    up()
    goto(x, y)
    dot(40, player)
    update()

    grid[len(grid) - count - 1][slot] = player
    last_played_cell = [len(grid) - count - 1, slot]
    if is_win(grid, player, last_played_cell, 4):
        print(str(player) + " wins")
        restart()
    slots[slot] = count + 1
    state.player = turns[player]


def restart():
    reset()
    hideturtle()
    grid()
    state.reset()
    Screen().onscreenclick(tap)
    done()


Screen().setup(420, 420, 370, 0)
hideturtle()
Screen().tracer(0, 0)
grid()
Screen().onscreenclick(tap)
done()

def next_cell(cell, offset):
    return [cell[0] + offset[0], cell[1] + offset[1]]


def is_in_grid(grid_height, grid_width, cell):
    return (cell[0] >= 0 and
            cell[0] < grid_height and
            cell[1] >= 0 and
            cell[1] < grid_width)


def count_diagonal(grid, last_played_cell, offset1, offset2):
    cell = last_played_cell
    grid_height = len(grid)
    grid_width = len(grid[0])
    count = 1

    while is_in_grid(grid_height, grid_width, next_cell(cell, [offset1[0], offset1[1]])):
        count += 1
        cell = next_cell(cell, [offset1[0], offset1[1]])
    cell = last_played_cell

    while is_in_grid(grid_height, grid_width, next_cell(cell, [offset2[0], offset2[1]])):
        count += 1
        cell = next_cell(cell, [offset2[0], offset2[1]])

    return count


def is_horizontal_win(grid, player, last_played_cell, win_score):
    score = 0
    for cell in grid[last_played_cell[0]]:
        if cell == player:
            score += 1
            if score >= win_score:
                return True
        else:
            score = 0
    return False


def is_vertical_win(grid, player, last_played_cell, win_score):
    score = 0
    for row in range(0, len(grid)):
        if grid[row][last_played_cell[1]] == player:
            score += 1
            if score >= win_score:
                return True
        else:
            score = 0
    return False


def is_diagonal_win(grid, player, last_played_cell, win_score, offset1, offset2):
    if count_diagonal(grid, last_played_cell, offset1, offset2) < win_score:
        return False

    cell = last_played_cell
    while is_in_grid(len(grid), len(grid[0]), next_cell(cell, offset1)):
        cell = next_cell(cell, offset1)

    score = 0
    for i in range(0, count_diagonal(grid, last_played_cell, offset1, offset2)):
        if grid[cell[0]][cell[1]] == player:
            score += 1
            if score >= win_score:
                return True
        else:
            score = 0
        cell = next_cell(cell, offset2)
    return False


def is_win(grid, player, last_played_cell, win_score):
    if is_horizontal_win(grid, player, last_played_cell, win_score):
        return True
    if is_vertical_win(grid, player, last_played_cell, win_score):
        return True
    # Descending diagonal
    if is_diagonal_win(grid, player, last_played_cell, win_score, [-1, -1], [1, 1]):
        return True
    # Ascending diagonal
    else:
        return is_diagonal_win(grid, player, last_played_cell, win_score, [-1, 1], [1, -1])

    class State:

     def __init__(self):
        self.player = 'yellow'
        self.slots = [0] * 8
        self.grid = [[None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None]]

    def reset(self):
        self.slots = [0] * 8
        self.grid = [[None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None]]

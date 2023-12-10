import pytest
from pathlib import Path

from day10.day10part1 import get_starting_position


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        rows = f.read().split('\n')
    start_char = 'J'

    result = area_enclosed_by_loop(rows, start_char)
    print(f'Day10 part 2: {result}')

def get_char_at(rows: list[str], position: (int, int)) -> str:
    i, j = position
    return rows[i][j]

def set_position(array: list[list[int]], position, value) -> None:
    x, y, = position
    if 0 <= x < len(array) and 0 <= y < len(array[0]):
        array[x][y] = 1 if value else 0

def take_step2(
        rows: list[str],
        current_position: (int, int),
        previous_position: (int, int),
        path,
        blue,
        red
) -> (int, int):
    i, j = current_position
    set_position(path, current_position, True)
    char = rows[i][j]
    next_position = None
    left = i, j - 1
    right = i, j + 1
    up = i - 1, j
    down = i + 1, j
    down_left = i + 1, j - 1
    down_right = i + 1, j + 1
    up_left = i - 1, j - 1
    up_right = i - 1, j + 1
    # blue is region on the left as you travel along the path
    # red is region to the right
    match char:
        case '|':
            if not previous_position or previous_position == down:
                next_position = up
                set_position(blue, left, True)
                set_position(red, right, True)
            else:
                next_position = down  # down
                set_position(red, left, True)
                set_position(blue, right, True)
        case '-':
            if not previous_position or previous_position == left:
                next_position = right
                set_position(blue, up, True)
                set_position(red, down, True)
            else:
                next_position = left
                set_position(red, up, True)
                set_position(blue, down, True)
        case 'L':
            if not previous_position or previous_position == right:
                next_position = up
                set_position(blue, down, True)
                set_position(blue, down_left, True)
                set_position(blue, left, True)
            else:
                next_position = right
                set_position(red, down, True)
                set_position(red, down_left, True)
                set_position(red, left, True)
        case 'J':
            if not previous_position or previous_position == left:
                next_position = up
                set_position(red, down, True)
                set_position(red, down_right, True)
                set_position(red, right, True)
            else:
                next_position = left
                set_position(blue, down, True)
                set_position(blue, down_right, True)
                set_position(blue, right, True)
        case '7':
            if not previous_position or previous_position == down:
                next_position = left
                set_position(red, right, True)
                set_position(red, up_right, True)
                set_position(red, up, True)
            else:
                next_position = down
                set_position(blue, right, True)
                set_position(blue, up_right, True)
                set_position(blue, up, True)
        case 'F':
            if not previous_position or previous_position == down:
                next_position = right
                set_position(blue, left, True)
                set_position(blue, up_left, True)
                set_position(blue, up, True)
            else:
                next_position = down
                set_position(red, up, True)
                set_position(red, up_left, True)
                set_position(red, left, True)
    set_position(path, next_position, True)
    return next_position

def area_enclosed_by_loop(rows: list[str], start_char: str) -> int:
    start_position = get_starting_position(rows)
    i, j = start_position
    rows[i] = rows[i][:j] + start_char + rows[i][j + 1:] if j != 0 else start_char + rows[i][j + 1:]
    current_position = start_position
    previous_position = None
    new_position = None

    is_path = [[0]*len(rows[0]) for _ in rows]
    blue = [[0]*len(rows[0]) for _ in rows] # this could be the inside region or outside, we don't know yet
    red = [[0]*len(rows[0]) for _ in rows] # so could this

    while new_position != start_position:
        new_position = take_step2(rows, current_position, previous_position, is_path, blue, red)
        previous_position = current_position
        current_position = new_position

    mark_path(blue, is_path)
    mark_path(red, is_path)
    blue_is_good, blue_size = expand_and_count_region(blue)
    _, red_size = expand_and_count_region(red)
    return blue_size if blue_is_good else red_size

def mark_path(array, path):
    for i, row in enumerate(array):
        for j, char in enumerate(row):
            if path[i][j]:
                array[i][j] = 8

def get_neighbours(i: int, j: int) -> list[(int, int)]:
    return [ (x, y) for x in range(i - 1, i + 2) for y in range(j - 1, j + 2) if not (x, y) == (i, j) ]

def is_out_of_bounds(position, array) -> bool:
    x, y = position
    return x < 0 or y < 0 or x >= len(array) or y >= len(array[0])

def expand_and_count_region(array) -> (bool, int):
    dirty = True
    total_area = 0
    while dirty:
        dirty = False
        total_area = 0
        for i, row in enumerate(array):
            for j, char in enumerate(row):
                if char == 1:
                    total_area += 1
                    for neighbour in get_neighbours(i, j):
                        if is_out_of_bounds(neighbour, array):
                            return False, -1
                        elif get_char_at(array, neighbour) == 0:
                            set_position(array, neighbour, 1)
                            dirty = True
    return True, total_area



def test_area_enclosed_by_loop():
    rows = [
        '...........',
        '.S-------7.',
        '.|F-----7|.',
        '.||.....||.',
        '.||.....||.',
        '.|L-7.F-J|.',
        '.|..|.|..|.',
        '.L--J.L--J.',
        '...........',
    ]
    start_char = 'F'
    actual = area_enclosed_by_loop(rows, start_char)
    assert actual == 4


if __name__ == '__main__':
    run()

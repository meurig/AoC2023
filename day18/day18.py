import time
from enum import StrEnum
from pathlib import Path

def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result = calc_pit_capacity(lines)
    print(f'Day18 part 1: {result} (in {(time.time() - start_time):.2f}s)')

class Heading(StrEnum):
    RIGHT ='R'
    DOWN = 'D'
    LEFT = 'L'
    UP = 'U'

test_input = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]

test_input2 = [
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
]

def parse_inputs(data: list[str]) -> list[(Heading, int, str)]:
    result = []
    for row in data:
        parts = row.split(' ')
        heading = Heading(parts[0])
        distance = int(parts[1])
        color_code = parts[2]
        result.append((heading, distance, color_code))
    return result

def test_parse_inputs():
    actual = parse_inputs(test_input)
    assert actual[0][0] == Heading.RIGHT
    assert actual[1][1] == 5
    assert actual[2][2] == '(#5713f0)'

def calc_pit_outline(data: list[str]) -> (list[list[bool]], list[list[bool]]):
    steps = parse_inputs(data)
    row_max = row_min = col_max = col_min = 0
    x, y = 0, 0
    for heading, distance, color_code in steps:
        match heading:
            case Heading.RIGHT:
                x , y = x, y + distance
            case Heading.LEFT:
                x, y = x, y - distance
            case Heading.DOWN:
                x, y = x + distance, y
            case Heading.UP:
                x, y = x - distance, y
        col_max = max(col_max, y)
        col_min = min(col_min, y)
        row_max = max(row_max, x)
        row_min = min(row_min, x)

    x, y = 0 - row_min, 0 - col_min
    is_pit = [ [False] * (y + col_max + 1) for _ in range(x + row_max + 1) ]
    is_interior = [[False] * (y + col_max + 1) for _ in range(x + row_max + 1)]
    is_pit[x][y] = True
    for heading, distance, color_code in steps:
        match heading:
            case Heading.RIGHT:
                for j in range(y, y + distance + 1):
                    is_pit[x][j] = True
                    if 0 <= x+1 < len(is_interior):
                        is_interior[x+1][j] = True
                x, y = x, y + distance
            case Heading.LEFT:
                for j in reversed(range(y - distance, y + 1)):
                    is_pit[x][j] = True
                    if 0 <= x-1 < len(is_interior):
                        is_interior[x-1][j] = True
                x, y = x, y - distance
            case Heading.DOWN:
                for i in range(x, x + distance + 1):
                    is_pit[i][y] = True
                    if 0 <= y-1 < len(is_interior[0]):
                        is_interior[i][y-1] = True
                x, y = x + distance, y
            case Heading.UP:
                for i in reversed(range(x - distance, x + 1)):
                    is_pit[i][y] = True
                    if 0 <= y+1 < len(is_interior[0]):
                        is_interior[i][y+1] = True
                x, y = x - distance, y

    return is_pit, is_interior

def calc_pit_capacity(data: list[str]) -> int:
    pit_outline, is_interior = calc_pit_outline(data)
    pit_size = 0

    pit =[ [False]*len(pit_outline[0]) for _ in pit_outline ]
    for i, row in enumerate(pit_outline):
        prev_tile_was_outline = False
        prev_tile_was_interior = False
        for j, tile in enumerate(row):
            if tile:
                pit_size += 1
                pit[i][j] = True
                prev_tile_was_outline = True
                prev_tile_was_interior = False
            else:
                if prev_tile_was_outline and is_interior[i][j] or (
                        not prev_tile_was_outline and prev_tile_was_interior):
                    pit_size += 1
                    pit[i][j] = True
                    prev_tile_was_outline = False
                    prev_tile_was_interior = True
                else:
                    prev_tile_was_outline = False
                    prev_tile_was_interior = False
    return pit_size

def printable_pit(is_pit: list[list[bool]]) -> list[str]:
    return [ ''.join([ '#' if x else '.' for x in row ]) for row in is_pit ]

def test_calc_pit_capacity():
    expected = 62
    actual = calc_pit_capacity(test_input)
    assert actual == expected

def test_calc_pit_capacity2():
    expected = 62
    actual = calc_pit_capacity(test_input2)
    assert actual == expected

if __name__ == '__main__':
    run()
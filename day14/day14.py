import time

import pytest
from pathlib import Path

from day13.day13 import transpose


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result1 = calc_north_load(lines)
    print(f'Day14 part 1: {result1} (in {(time.time() - start_time):.2f}s)')

    start_time = time.time()
    lines, load = cycle(lines, 1000000000)
    print(f'Day14 part 2: {load} (in {(time.time() - start_time):.2f}s)')


test_data = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....',
]

def cycle(lines: list[str], times: int) -> (list[str], int):
    seen: dict[int, int] = {}
    lines = rotate_90_anticlockwise(lines)
    for i in range(times):
        lines = inner_cycle(lines)
        line_hash = hash(get_hashable(lines))
        if line_hash in seen:
            cycle_length = i - seen[line_hash]
            remaining = times - (i + 1)
            can_skip = (remaining // cycle_length) * cycle_length
            cycles_left_after_skip = remaining - can_skip
            for _ in range(cycles_left_after_skip):
                lines = inner_cycle(lines)
            north_load = calc_load(lines)
            return rotate_90_clockwise(lines), north_load
        else:
            seen[line_hash] = i
    north_load = calc_load(lines)
    return rotate_90_clockwise(lines), north_load

def get_hashable(rows: list[str]) -> str:
    result = ''
    for row in rows:
        result += row
    return result

@pytest.mark.parametrize('rows, times, expected', [
    (test_data, 1000000000, 64),
    # (test_data, 20, 64),
])
def test_load_after_cycles(rows, times, expected):
    lines, load = cycle(rows, times)
    assert load == expected

@pytest.mark.parametrize('rows, times, expected', [
    (test_data, 1, [
        '.....#....',
        '....#...O#',
        '...OO##...',
        '.OO#......',
        '.....OOO#.',
        '.O#...O#.#',
        '....O#....',
        '......OOOO',
        '#...O###..',
        '#..OO#....',
    ]),
    (test_data, 2, [
        '.....#....',
        '....#...O#',
        '.....##...',
        '..O#......',
        '.....OOO#.',
        '.O#...O#.#',
        '....O#...O',
        '.......OOO',
        '#..OO###..',
        '#.OOO#...O',
    ]),
    (test_data, 3, [
        '.....#....',
        '....#...O#',
        '.....##...',
        '..O#......',
        '.....OOO#.',
        '.O#...O#.#',
        '....O#...O',
        '.......OOO',
        '#...O###.O',
        '#.OOO#...O',
    ]),
])
def test_cycle(rows, times, expected):
    actual, load = cycle(rows, times)
    assert actual == expected

def inner_cycle(lines) -> list[str]: # takes facing north
    lines = tilt(lines) # north
    lines = rotate_90_clockwise(lines)
    lines = tilt(lines) # west
    lines = rotate_90_clockwise(lines)
    lines = tilt(lines) # south
    lines = rotate_90_clockwise(lines)
    lines = tilt(lines) # east
    lines = rotate_90_clockwise(lines)
    return lines # returns facing north

def calc_north_load(lines: list[str]) -> int:
    return calc_west_load(rotate_90_anticlockwise(lines))

def test_calc_north_load2():
    rows = [
        '.....#....',
        '....#...O#',
        '.....##...',
        '..O#......',
        '.....OOO#.',
        '.O#...O#.#',
        '....O#...O',
        '.......OOO',
        '#...O###.O',
        '#.OOO#...O',
    ]
    expected = 110
    actual = calc_north_load(rows)
    assert actual == expected

def calc_west_load(lines: list[str]) -> int:
    total_load = 0
    for row in lines:
        result, load = tilt_row_left(row)
        total_load += load
    return total_load

def calc_load(rows: list[str]) -> int:
    total_load = 0
    for row in rows:
        total_load += calc_row_load(row)
    return total_load

def calc_row_load(row: str) -> int:
    load = 0
    for i, char in enumerate(row):
        if char == 'O':
            load += len(row) - i
    return load

@pytest.mark.parametrize('row, expected', [
    ('OOO', 6),
    ('...', 0),
    ('.#.', 0),
    ('.#O', 1),
    ('#.#O..#.##',7),
    ('#.#O..#O.#',10),
])
def test_calc_row_load(row, expected):
    actual = calc_row_load(row)
    assert actual == expected

def tilt(rows: list[str]) -> list[str]:
    return [ tilt_row(row) for row in rows ]

def tilt_row(row: str) -> str:
    result = ''
    for i, char in enumerate(row):
        match char:
            case 'O':
                result += 'O'
            case '.':
                continue
            case '#':
                result += '.'*(i - len(result)) + '#'
    result += '.' * (len(row) - len(result))
    return result

def tilt_row_left(row: str) -> (str, int):
    result = ''
    load = 0
    for i, char in enumerate(row):
        match char:
            case 'O':
                result += 'O'
                load += len(row) - len(result) + 1
            case '.':
                continue
            case '#':
                result += '.'*(i - len(result)) + '#'
    result += '.' * (len(row) - len(result))
    return result, load

@pytest.mark.parametrize('row, expected', [
    ('OOO', ('OOO', 6)),
    ('...', ('...', 0)),
    ('.#.', ('.#.', 0)),
    ('.#O', ('.#O', 1)),
    ('#.#..O#.##',('#.#O..#.##',7)),
    ('#.#..O#.O#',('#.#O..#O.#',10)),
])
def test_tilt_left(row, expected):
    actual = tilt_row_left(row)
    assert actual == expected

def rotate_90_clockwise(lines: list[str]) -> list[str]:
    return [ x[::-1] for x in transpose(lines) ]

def test_rotate_90_clockwise():
    lines = [
        'ABC',
        'DEF',
    ]
    expected = [
        'DA',
        'EB',
        'FC',
    ]
    actual = rotate_90_clockwise(lines)
    assert actual == expected

def rotate_90_anticlockwise(lines: list[str]) -> list[str]:
    return list(reversed(transpose(lines)))

def test_rotate_90_anticlockwise():
    lines = [
        'ABC',
        'DEF',
    ]
    expected = [
        'CF',
        'BE',
        'AD',
    ]
    actual = rotate_90_anticlockwise(lines)
    assert actual == expected

def test_calc_north_load():
    expected = 136
    actual = calc_north_load(test_data)
    assert actual == expected

if __name__ == '__main__':
    run()

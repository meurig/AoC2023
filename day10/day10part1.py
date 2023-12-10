import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        rows = f.read().split('\n')
    start_char = 'J'

    result = length_to_furthest_point(rows, start_char)
    print(f'Day10 part 1: {result}')

def take_step(rows: list[str], current_position: (int, int), previous_position: (int, int)) -> (int, int):
    i, j = current_position
    char = rows[i][j]
    a = b = None
    match char:
        case '|':
            a = i + 1, j
            b = i - 1, j
        case '-':
            a = i, j + 1
            b = i, j - 1
        case 'L':
            a = i - 1, j
            b = i, j + 1
        case 'J':
            a = i - 1, j
            b = i, j - 1
        case '7':
            a = i, j - 1
            b = i + 1, j
        case 'F':
            a = i, j + 1
            b = i + 1, j
    return a if a != previous_position else b

def get_starting_position(rows) -> (int, int):
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char == 'S':
                return i, j
    raise ValueError

test_rows = [
        '..F7.',
        '.FJ|.',
        'SJ.L7',
        '|F--J',
        'LJ...',
    ]
test_start_char = 'F'

def test_get_starting_position():
    expected = (2, 0)
    actual = get_starting_position(test_rows)
    assert actual == expected

def length_to_furthest_point(rows: list[str], start_char: str) -> int:
    start_position = get_starting_position(rows)
    i, j = start_position
    rows[i] = rows[i][:j] + start_char + rows[i][j+1:] if j != 0 else start_char + rows[i][j+1:]
    current_position = start_position
    total_steps = 0
    previous_position = None
    new_position = None
    while new_position != start_position:
        new_position = take_step(rows, current_position, previous_position)
        total_steps += 1
        previous_position = current_position
        current_position = new_position
    return int(total_steps / 2)


def test_length_to_furthest_point():
    expected = 8
    actual = length_to_furthest_point(test_rows, test_start_char)
    assert actual == expected

if __name__ == '__main__':
    run()

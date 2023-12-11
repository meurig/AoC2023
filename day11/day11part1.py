import copy
import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = sum_of_shortest_paths(lines)
    print(f'DayX part 1: {result}')

def expand_empty_space(rows) -> list[str]:
    empty_rows = [True] * len(rows)
    empty_columns = [True] * len(rows[0])
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char != '.':
                empty_rows[i] = False
                empty_columns[j] = False

    expanded_columns = []
    for i, row in enumerate(rows):
        new_column = ''
        for j, char in enumerate(row):
            new_column += '..' if empty_columns[j] else char
        expanded_columns.append(new_column)

    new_row = ''.join(['.'] * len(expanded_columns[0]))
    expanded_rows = []
    for i, row in enumerate(expanded_columns):
        if empty_rows[i]:
            str(expanded_rows.append(new_row))
            str(expanded_rows.append(new_row))
        else:
            str(expanded_rows.append(row))

    return expanded_rows


expanded_test_rows = [
    '....#........',
    '.........#...',
    '#............',
    '.............',
    '.............',
    '........#....',
    '.#...........',
    '............#',
    '.............',
    '.............',
    '.........#...',
    '#....#.......',
]

def test_expand_empty_space():
    expected = expanded_test_rows
    actual = expand_empty_space(test_rows)
    assert actual == expected

def find_galaxies(rows: list[str]) -> list[(int, int)]:
    galaxies = []
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char == '#':
                galaxies.append((i, j))
    return galaxies

def get_shortest_path(a: (int, int), b: (int, int)) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x2 - x1) + abs(y2 - y1)

def test_get_shortest_path():
    a = (6, 1)
    b = (11, 5)
    expected = 9
    actual = (get_shortest_path(a, b))
    assert actual == expected

def sum_of_shortest_paths(rows: list[str]) -> int:
    rows = expand_empty_space(rows)
    galaxies = find_galaxies(rows)
    total = 0
    visited = set([])
    for x in galaxies:
        for y in galaxies:
            if x == y or (y, x) in visited:
                continue
            visited.add((x, y))
            total += get_shortest_path(x, y)
    return total

test_rows = [
        '...#......',
        '.......#..',
        '#.........',
        '..........',
        '......#...',
        '.#........',
        '.........#',
        '..........',
        '.......#..',
        '#...#.....',
    ]

def test_sum_of_shortest_paths():
    actual = sum_of_shortest_paths(test_rows)
    assert actual == 374

if __name__ == '__main__':
    run()

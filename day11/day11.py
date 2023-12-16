import time
import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result1 = sum_of_shortest_paths(lines, 1)
    print(f'Day11 part 1: {result1} (in {(time.time() - start_time):.2f}s)')

    start_time = time.time()
    result2 = sum_of_shortest_paths(lines, 1000000)
    print(f'Day11 part 2: {result2} (in {(time.time() - start_time):.2f}s)')

def find_empty_space(rows: list[str]) -> (list[int], list[int]):
    empty_rows = [True] * len(rows)
    empty_columns = [True] * len(rows[0])
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char != '.':
                empty_rows[i] = False
                empty_columns[j] = False
    return (
        [i for i, row in enumerate(empty_rows) if row],
        [j for j, col in enumerate(empty_columns) if col]
    )

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

def test_find_empty_space():
    expected = ([3, 7], [2, 5, 8])
    actual = find_empty_space(test_rows)
    assert actual == expected

def find_galaxies(rows: list[str], empty_rows, empty_columns, expansion_factor) -> list[(int, int)]:
    galaxies = []
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char == '#':
                galaxies.append(
                    (
                        i + (expansion_factor-1)*(len([r for r in empty_rows if r < i])),
                        j + (expansion_factor-1)*(len([c for c in empty_columns if c < j]))
                    ))
    return galaxies

test_galaxies = [
    '..#'
]
@pytest.mark.parametrize('expansion_factor, expected', [
    (1, [(0, 2)]),
    (2, [(0, 4)]),
    (10, [(0, 20)])
])
def test_find_galaxies(expansion_factor, expected):
    er, ec = find_empty_space(test_galaxies)
    actual = find_galaxies(test_galaxies, er, ec, expansion_factor)
    assert actual == expected

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

def sum_of_shortest_paths(rows: list[str], expansion_factor) -> int:
    empty_rows, empty_columns = find_empty_space(rows)
    galaxies = find_galaxies(rows, empty_rows, empty_columns, expansion_factor)
    total = 0
    visited = set([])
    for x in galaxies:
        for y in galaxies:
            if x == y or (y, x) in visited:
                continue
            visited.add((x, y))
            total += get_shortest_path(x, y)
    return total

@pytest.mark.parametrize('expansion_factor, expected', [
    (2, 374),
    (10, 1030),
    (100, 8410),
])
def test_sum_of_shortest_paths(expansion_factor, expected):
    actual = sum_of_shortest_paths(test_rows, expansion_factor)
    assert actual == expected

if __name__ == '__main__':
    run()

import time
from pathlib import Path

import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result = take_steps_and_count(lines, 64)
    print(f'Day21 part 1: {result} (in {(time.time() - start_time):.2f}s)')

def take_steps_and_count(grid: list[str], steps: int) -> int:
    for _ in range(steps):
        grid = take_step(grid)
    result = count_o_positions(grid)
    return result

def count_o_positions(grid: list[str]) -> int:
    return sum([ 1 if char == 'O' else 0 for row in grid for char in row ])

def take_step(grid: list[str]) -> list[str]:
    # print()
    # print('Before:')
    # for row in grid:
    #     print(row)
    grid_height = len(grid)
    grid_width = len(grid[0])
    next_step: list[list[str]] = [[''] * grid_width for _ in range(grid_height)]
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '#':
                next_step[i][j] = '#'
            elif any([n in ['S', 'O'] for n in get_neighbours(i, j, grid)]):
                next_step[i][j] = 'O'
            else:
                next_step[i][j] = '.'
    grid = [ ''.join(row) for row in next_step ]
    # print()
    # print('After:')
    # for row in grid:
    #     print(row)
    return grid

def get_neighbours(i, j, grid) -> list[str]:
    return [grid[x][y] for x, y in get_neighbouring_positions(i, j, len(grid), len(grid[0])) ]

def get_neighbouring_positions(i, j, grid_height, grid_width) -> list[(int, int)]:
    potential_neighbours = [
        (i - 1, j),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j),
    ]
    results = [(x, y) for x, y in potential_neighbours if 0 <= x < grid_height and 0 <= y < grid_width]
    return results

test_data = [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........',
]

@pytest.mark.parametrize('grid, steps, expected', [
    (test_data, 1, 2),
    (test_data, 2, 4),
    (test_data, 3, 6),
    (test_data, 6, 16),
])
def test_take_steps_and_count(grid, steps, expected):
    actual = take_steps_and_count(test_data, steps)
    assert actual == expected

if __name__ == '__main__':
    run()

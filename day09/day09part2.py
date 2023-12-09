import pytest
from pathlib import Path

from day09.day09part1 import calculate_all_levels


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day09 part 2: {result}')

def append_values(levels: list[list[int]]):
    levels[-1].append(0)
    for a, b in list(zip(levels, levels[1:]))[::-1]:
        a.append(a[0] - b[-1]) # this could/should be added at the start, but appending works and is faster
    return levels

def test_append_values():
    levels = [
        [1, 3, 6, 10, 15, 21],
        [2, 3, 4, 5, 6],
        [1, 1, 1, 1],
        [0, 0, 0],
    ]
    expected = [
        [1, 3, 6, 10, 15, 21, 0],
        [2, 3, 4, 5, 6, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0],
    ]
    append_values(levels)
    assert levels == expected

def calc(value: str) -> int:
    numbers = [int(x) for x in value.split()]
    levels = calculate_all_levels(numbers)
    append_values(levels)
    return levels[0][-1]


testdata =[
    ("0 3 6 9 12 15", -3),
    ("1 3 6 10 15 21", 0),
    ("10 13 16 21 30 45", 5),
]

@pytest.mark.parametrize("value, expected", testdata)
def test_calc(value: str, expected: int):
    result = calc(value)
    assert result == expected

def calc_all(data: list) -> int:
    total = 0
    for x in data:
        total += calc(x)
    return total


def test_calc_all():
    data = [x for (x, y) in testdata]
    actual = calc_all(data)
    assert actual == 2

if __name__ == '__main__':
    run()

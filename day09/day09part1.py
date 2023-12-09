import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day09 part 1: {result}')

def append_values(levels: list[list[int]]):
    for a, b in list(zip(levels, levels[1:]))[::-1]:
        a.append(a[-1] + b[-1])
    levels[-1].append(0)
    return levels

def test_append_values():
    levels = [
        [1, 3, 6, 10, 15, 21],
        [2, 3, 4, 5, 6],
        [1, 1, 1, 1],
        [0, 0, 0],
    ]
    expected = [
        [1, 3, 6, 10, 15, 21, 28],
        [2, 3, 4, 5, 6, 7],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0],
    ]
    append_values(levels)
    assert levels == expected

def calculate_all_levels(numbers: list[int]) -> list[list[int]]:
    levels = []
    level = numbers
    while not are_all_zeros(level):
        levels.append(level)
        level = find_rate_of_change(level)
    levels.append(level)
    return levels

def test_calculate_all_levels():
    numbers = [1, 3, 6, 10, 15, 21]
    expected = [
        [1, 3, 6, 10, 15, 21],
        [2, 3, 4, 5, 6],
        [1, 1, 1, 1],
        [0, 0, 0],
    ]
    actual = calculate_all_levels(numbers)
    assert actual == expected

def are_all_zeros(numbers: list[int]) -> bool:
    if not numbers:
        raise ValueError
    for number in numbers:
        if number != 0:
            return False
    return True

@pytest.mark.parametrize("numbers, expected", [
    ([0,0,0,0], True),
    ([0,1,0,0], False),
    ([0,0,0,-1], False),
])
def test_are_all_zeros(numbers, expected):
    actual = are_all_zeros(numbers)
    assert actual == expected

def find_rate_of_change(numbers: list[int]) -> list[int]:
    return [b - a for a, b in zip(numbers, numbers[1:])]

@pytest.mark.parametrize("numbers, expected", [
    ([1, 3, 6, 10, 15, 21], [2, 3, 4, 5, 6]),
])
def test_find_rate_of_change(numbers, expected):
    actual = find_rate_of_change(numbers)
    assert actual == expected

def calc(value: str) -> int:
    numbers = [int(x) for x in value.split()]
    levels = calculate_all_levels(numbers)
    append_values(levels)
    return levels[0][-1]


testdata =[
    ("0 3 6 9 12 15", 18),
    ("1 3 6 10 15 21", 28),
    ("10 13 16 21 30 45", 68),
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
    assert actual == 114

if __name__ == '__main__':
    run()

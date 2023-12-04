from typing import Tuple, Set, List

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day04 part 1: {result}')


def seperate_numbers(line: str) -> Tuple[Set[int], List[int]]:
    inputs = line.split(':')[1].split('|')
    winners = { int(x) for x in inputs[0].strip().split(' ') if x != '' }
    ours = [ int(x) for x in inputs[1].strip().split(' ') if x != '' ]
    return winners, ours

def test_seperate_numbers():
    line = 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
    expected_winners = {41, 48, 83, 86, 17}
    expected_ours = [83, 86, 6, 31, 17, 9, 48, 53]
    winners, ours = seperate_numbers(line)
    assert winners == expected_winners
    assert ours == expected_ours

def calculate_score(value: str) -> int:
    winners, ours = seperate_numbers(value)
    matching_numbers = [ x for x in ours if x in winners ]
    matches = len(matching_numbers)
    points = 0 if matches == 0 else pow(2, matches - 1)
    return points

testdata = [
    ('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 8),
    ('Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19', 2),
    ('Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', 2),
    ('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83', 1),
    ('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', 0),
    ('Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11', 0),
]
@pytest.mark.parametrize("value, expected", testdata)
def test_calculate_score(value: str, expected: int):
    # arrange
    # act
    result = calculate_score(value)
    # assert
    assert result == expected


def calc_all(data: list) -> int:
    total = 0
    for x in data:
        total += calculate_score(x)
    return total

def test_calc_all():
    data = [x for (x, y) in testdata]
    actual = calc_all(data)
    assert actual == 13


if __name__ == '__main__':
    run()

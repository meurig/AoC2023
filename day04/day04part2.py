from typing import List

import pytest
from pathlib import Path

from day04.day04part1 import seperate_numbers


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day04 part 2: {result}')

def calculate_score(value: str) -> int:
    winners, ours = seperate_numbers(value)
    matching_numbers = [ x for x in ours if x in winners ]
    return len(matching_numbers)

testdata = [
    ('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 4),
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

def get_card_scores(data: List[str]) -> List[int]:
    return [ calculate_score(line) for line in data ]

def calc_all(data: list) -> int:
    scores = get_card_scores(data)
    counts = [ 1 for _ in data ]
    for card, score in enumerate(scores):
        for x in range(card, card + score):
            counts[x+1] += counts[card]
    total_count = 0
    for count in counts:
        total_count += count
    return total_count

testdata = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]
def test_calc_all():
    actual = calc_all(testdata)
    assert actual == 30


if __name__ == '__main__':
    run()

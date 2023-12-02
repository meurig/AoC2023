from typing import Tuple

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day02 part 1: {result}')


limits = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def calc(value: str) -> (int, bool):
    items = value.split(':')
    game = items[0]
    game = int(game.split()[1])
    subsets = items[1].split(';')
    subsets = [ subset.split(',') for subset in subsets ]
    for subset in subsets:
        for item in subset:
            colour = item.split()[1]
            count = int(item.split()[0])
            if count > limits.get(colour, 0):
                return game, False
    return game, True


def calc_all(data: list) -> int:
    total = 0
    for x in data:
        game, result = calc(x)
        if result:
            total += game
    return total


testdata = [
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", (1, True)),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", (2, True)),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", (3, False)),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", (4, False)),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", (5, True)),
]


@pytest.mark.parametrize("value, expected", testdata)
def test_calc(value: str, expected: Tuple[int, bool]):
    # arrange
    # act
    result = calc(value)
    # assert
    assert result == expected


def test_calc_all():
    data = [x for (x, y) in testdata]
    actual = calc_all(data)
    assert actual == 8


if __name__ == '__main__':
    run()

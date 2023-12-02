from pathlib import Path
import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day02 part 2: {result}')


def calc(value: str) -> int:
    subsets = value.split(':')[1].split(';')
    subsets = [subset.split(',') for subset in subsets]
    # print()
    limits = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    for subset in subsets:
        for item in subset:
            colour = item.split()[1]
            count = int(item.split()[0])
            # print(f'colour: {colour}')
            # print(f'count: {count}')
            if count > limits.get(colour, 0):
                limits[colour] = count
    return limits['red'] * limits['green'] * limits['blue']


def calc_all(data: list) -> int:
    total = 0
    for x in data:
        total += calc(x)
    return total


testdata = [
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 1560),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 630),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
]


@pytest.mark.parametrize("value, expected", testdata)
def test_calc(value: str, expected: int):
    # arrange
    # act
    result = calc(value)
    # assert
    assert result == expected


def test_calc_all():
    data = [x for (x, y) in testdata]
    actual = calc_all(data)
    assert actual == 2286


if __name__ == '__main__':
    run()

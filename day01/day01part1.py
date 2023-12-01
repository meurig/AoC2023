import pytest
import re
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day01 part 1: {result}')


def calc(value: str) -> int:
    numbers = re.sub('\\D', '', value)
    answer = f'{numbers[0]}{numbers[-1]}'
    return int(answer)


def calc_all(data: list) -> int:
    total = 0
    for x in data:
        total += calc(x)
    return total


testdata = [
    ("1abc2", 12),
    ("pqr3stu8vwx", 38),
    ("a1b2c3d4e5f", 15),
    ("treb7uchet", 77),
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
    assert actual == 142


if __name__ == '__main__':
    run()

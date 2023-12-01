from pathlib import Path
import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_all(lines)
    print(f'Day01 part 2: {result}')


def calc(value: str) -> int:

    replacements = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }

    first_number = None
    for i in range(len(value)):
        if value[i].isdigit():
            first_number = int(value[i])
            break
        for k, v in replacements.items():
            if value[i:i+len(k)] == k:
                first_number = int(v)
                break
        else:
            continue
        break

    last_number = None
    for i in reversed(range(len(value))):
        if value[i].isdigit():
            last_number = int(value[i])
            break
        for k, v in replacements.items():
            if value[i-len(k)+1:i+1] == k:
                last_number = int(v)
                break
        else:
            continue
        break

    return int(f'{first_number}{last_number}')


def calc_all(data: list) -> int:
    total = 0
    for x in data:
        total += calc(x)
    return total


testdata = [
    ("two1nine", 29),
    ("eightwothree", 83),
    ("abcone2threexyz", 13),
    ("xtwone3four", 24),
    ("4nineeightseven2", 42),
    ("zoneight234", 14),
    ("7pqrstsixteen", 76)
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
    assert actual == 281


if __name__ == '__main__':
    run()

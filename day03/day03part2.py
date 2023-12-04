from typing import List
import pytest
from pathlib import Path

from day03.day03part1 import get_adjacent_positions, get_number


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc(lines)
    print(f'Day03 part 2: {result}')

def calc(data: list) -> int:
    total = 0
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            if item == '*':
                total += gear_result(i, j, data)
    return total

def gear_result(i: int, j: int, data: List[str]) -> int:
    numbers = {} # starting position to value
    result = 1
    for x, y in get_adjacent_positions((i, j), len(data), len(data[0])):
        if data[x][y].isdigit():
            number, real_start_index = get_number(data[x], y)
            start_position = (x, real_start_index)
            if not start_position in numbers:
                numbers[start_position] = number
                result *= number
    return result if len(numbers) == 2 else 0


testdata = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

def test_calc_all():
    actual = calc(testdata)
    assert actual == 467835


if __name__ == '__main__':
    run()

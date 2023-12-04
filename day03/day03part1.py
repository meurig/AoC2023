from typing import List, Tuple, Dict
import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc(lines)
    print(f'Day03 part 1: {result}')

def get_number(line: str, start_index: int) -> Tuple[int, int]:
    number = ''
    real_start = start_index
    for x in range(start_index, len(line)):
        if line[x].isdigit():
            number = number + line[x]
        else:
            break

    for x in reversed(range(0, max(0, start_index))):
        if line[x].isdigit():
            number = line[x] + number
            real_start = x
        else:
            break

    return int(number), real_start

testdata_get_number = [
    (137,764,137),
    (138,764,137),
    (139,764,137),
]
@pytest.mark.parametrize("start_index, expected_number, expected_real_start", testdata_get_number)
def test_get_number(start_index, expected_number, expected_real_start):
    # arrange
    input = '.......-.............343......750..661....%........+..323.....1..............480.........+..............198.......................533.../764'
    # act
    number, real_start  = get_number(input, start_index)
    # assert
    assert number == expected_number
    assert real_start == expected_real_start


def is_symbol(char: str) -> int:
    return 0 if (char.isdigit() or char == ".") else 1


def get_adjacent_positions(position: Tuple[int, int], max_i, max_j) -> List[Tuple[int,int]]:
    i, j = position
    valid = []
    for x in range(max(i-1,0),min(i+1, max_i)+1):
        for y in range(max(j-1,0),min(j+1, max_j)+1):
            if (x,y) != position:
                valid.append((x,y))
    return valid


testdata_get_adjacent_spaces = [
    ((0,0),[(0,1),(1,0),(1,1)]),
    ((9,9),[(8,8),(8,9),(9,8)]),
    ((5,5),[(4,4),(4,5),(4,6),(5,4),(5,6),(6,4),(6,5),(6,6)])
]
@pytest.mark.parametrize("position, expected", testdata_get_adjacent_spaces)
def test_get_adjacent_positions(position, expected):
    # arrange
    position = (0,0)
    max_i = max_j = 9
    expected = [(0,1),(1,0),(1,1)]
    # act
    actual = get_adjacent_positions(position, max_i, max_j)
    # assert
    assert actual == expected


def get_adjacent_numbers(i: int, j: int, data: List[str]) -> Dict[Tuple[int, int], int]:
    adjacent_numbers = {}
    for x, y in get_adjacent_positions((i, j), len(data), len(data[0])):
        if data[x][y].isdigit():
            number, real_start = get_number(data[x], y)
            adjacent_numbers[(x, real_start)] = number
    return adjacent_numbers

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
testdata_get_adjacent_numbers = [
    (4, 3, {
        (4,0): 617
    }),
    (1, 3, {
        (0,0): 467,
        (2,2): 35,
    })
]
@pytest.mark.parametrize("i, j, expected", testdata_get_adjacent_numbers)
def test_get_adjacent_numbers(i, j, expected):
    # arrange
    i = 1
    j = 3
    expected = {
        (0, 0): 467,
        (2, 2): 35,
    }
    # act
    actual = get_adjacent_numbers(i, j, testdata)
    # assert
    assert actual == expected


def calc(data: List[str]) -> int:
    valid_numbers = {} # position to value
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            if is_symbol(item):
                for position, number in get_adjacent_numbers(i, j, data).items():
                    valid_numbers[position] = number
    total = 0
    for number in valid_numbers.values():
        total += number
    return total


def test_calc():
    expected = 4361
    actual = calc(testdata)
    assert actual == expected


if __name__ == '__main__':
    run()

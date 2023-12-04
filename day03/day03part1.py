from typing import Callable, List, Optional, Tuple

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc(lines)
    print(f'Day03 part 1: {result}')

def to_matrix(data: list, func: Optional[Callable] = (lambda x: x)) -> List[List]:
    result = []
    for i, line in enumerate(data):
        result.append([])
        for j, char in enumerate(line):
            result[i].append(func(char))
    return result

def to_string_list(data: List[List]) -> List[str]:
    return [ ''.join([ str(x) for x in line]) for line in data]

def pretty_print(data):
    for x in data:
        print(x)

def get_symbols(data: list) -> List[List[bool]]:
    def is_symbol(char: str) -> int:
        return 0 if (char.isdigit() or char == ".") else 1
    print()
    result = to_matrix(data, is_symbol)
    #pretty_print(to_string_list(result))
    return result

def get_adjacent_spaces(position: Tuple[int, int], max_i, max_j) -> List[Tuple[int,int]]:
    i, j = position
    valid = []
    for x in range(max(i-1,0),min(i+1, max_i)+1):
        for y in range(max(j-1,0),min(j+1, max_j)+1):
            if (x,y) != position:
                valid.append((x,y))
    return valid

def get_spaces_adjacent_to_symbols(data: list) -> List[List[int]]:
    symbols = get_symbols(data)
    adjacents = []
    # initialize empty list of lists
    for x, line in enumerate(data):
        adjacents.append([])
        for _ in enumerate(line):
            adjacents[x].append(0)

    for i, line in enumerate(symbols):
        for j, item in enumerate(line):
            if symbols[i][j]:
                for x, y in get_adjacent_spaces((i,j),len(data)-1, len(line)-1):
                    adjacents[x][y] = 1
    return adjacents


def get_number(line: str, start_index: int) -> int:
    number = ''
    for x in range(start_index, len(line)):
        if line[x].isdigit():
            number = number + line[x]
        else:
            return int(number)
    return int(number)


def calc(data: List[str]) -> int:
    total = 0
    valid_spaces = get_spaces_adjacent_to_symbols(data)
    #pretty_print(to_string_list(valid_spaces))
    data = to_matrix(data)
    for i, line in enumerate(data):
        skip = 0
        for j, item in enumerate(line):
            if skip > 0:
                skip -= 1
                continue
            if str(item).isdigit():
                number = get_number(line, j)
                length = len(str(number))
                #print(f'number = {number}, length = {length}')
                is_valid = False
                for x in range(j, j+length):
                    #print(f'i = {i}, x = {x}')
                    #print(f'data[{i}][{x}] = {data[i][x]}')
                    #print(f'valid_spaces[{i}][{x}] = {valid_spaces[i][x]}')
                    if valid_spaces[i][x]:
                        is_valid = True
                if is_valid:
                    total += number
                #else:
                    #print(f'not valid: {number}')
                skip = length
                continue
    return total

def test_get_number():
    input = '.......-.............343......750..661....%........+..323.....1..............480.........+..............198.......................533.../764'
    number = get_number(input, 137)
    expected = 764
    assert number == expected


def test_calc():
    expected = 4361
    actual = calc(testdata)
    assert actual == expected


def test_get_spaces_adjacent_to_symbols():
    # arrange
    expected = [
        '0011100000',
        '0010100000',
        '0011111100',
        '0011110100',
        '0010111100',
        '0011101000',
        '0000111000',
        '0011111000',
        '0010101000',
        '0011111000'
    ]
    # act
    actual = get_spaces_adjacent_to_symbols(testdata)
    # assert
    assert to_string_list(actual) == expected

testdata_get_adjacent_spaces = [
    ((0,0),[(0,1),(1,0),(1,1)]),
    ((9,9),[(8,8),(8,9),(9,8)]),
    ((5,5),[(4,4),(4,5),(4,6),(5,4),(5,6),(6,4),(6,5),(6,6)])
]
@pytest.mark.parametrize("position, expected", testdata_get_adjacent_spaces)
def test_get_adjacent_spaces(position, expected):
    # arrange
    position = (0,0)
    max_i = max_j = 9
    expected = [(0,1),(1,0),(1,1)]
    # act
    actual = get_adjacent_spaces(position, max_i, max_j)
    # assert
    assert actual == expected



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

def test_get_symbols():
    # arrange
    expected = [
        "0000000000",
        "0001000000",
        "0000000000",
        "0000001000",
        "0001000000",
        "0000010000",
        "0000000000",
        "0000000000",
        "0001010000",
        "0000000000",
    ]
    # act
    actual = get_symbols(testdata)
    # assert
    assert to_string_list(actual) == expected


if __name__ == '__main__':
    run()

from pathlib import Path
import pytest
from functools import cache

def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result1 = sum_all_arrangements(lines, False)
    print(f'Day12 part 1: {result1}')
    result2 = sum_all_arrangements(lines, True)
    print(f'Day12 part 2: {result2}')

def unfold_input(value: str, pattern: str) -> (str, list[int]):
    new_value = value
    new_pattern = pattern
    for _ in range(4):
        new_value += '?' + value
        new_pattern += ',' + pattern
    return new_value, new_pattern

def test_unfold_input():
    value = '.#'
    pattern = '1'
    expected = ('.#?.#?.#?.#?.#', '1,1,1,1,1')
    actual = unfold_input(value, pattern)
    assert actual == expected

def split_row(row: str) -> (str, str):
    value = row.split(' ')[0]
    pattern = row.split(' ')[1]
    return value, pattern


test_arrangements= [
    ('. 1', []),
    ('? 1', ['#']),
    ('# 1', ['#']),
    ('?? 1', ['#.', '.#']),
    ('??? 1,1', ['#.#']),
    ('???.### 1,1,3', [
        '#.#.###'
    ]),
    ('.??..??...?##. 1,1,3', [
        '.#...#....###.',
        '.#....#...###.',
        '..#..#....###.',
        '..#...#...###.',
    ]),
    ('?###???????? 3,2,1', [
        '.###.##.#...',
        '.###.##..#..',
        '.###.##...#.',
        '.###.##....#',
        '.###..##.#..',
        '.###..##..#.',
        '.###..##...#',
        '.###...##.#.',
        '.###...##..#',
        '.###....##.#',
    ]),
    ('?.??????#??.???#.?? 1,1,2,1,4,1', [
        '#.#.##..#...####.#.',
        '#.#.##..#...####..#',
        '#.#..##.#...####.#.',
        '#.#..##.#...####..#',
        '#.#....##.#.####.#.',
        '#.#....##.#.####..#',
        '#..#.##.#...####.#.',
        '#..#.##.#...####..#',
        '#..#...##.#.####.#.',
        '#..#...##.#.####..#',
        '#...#..##.#.####.#.',
        '#...#..##.#.####..#',
        '#....#.##.#.####.#.',
        '#....#.##.#.####..#',
        '..#.#..##.#.####.#.',
        '..#.#..##.#.####..#',
        '..#..#.##.#.####.#.',
        '..#..#.##.#.####..#',
        '...#.#.##.#.####.#.',
        '...#.#.##.#.####..#',
    ]),
    ('??????#?.???.?????? 1,2,3,2,1', [ # yes, I really needed lots of tests to identify my many bugs!
        '#.##.###.##..#.....',
        '#.##.###.##...#....',
        '#.##.###.##....#...',
        '#.##.###.##.....#..',
        '#.##.###.##......#.',
        '#.##.###.##.......#',
        '#.##.###..##.#.....',
        '#.##.###..##..#....',
        '#.##.###..##...#...',
        '#.##.###..##....#..',
        '#.##.###..##.....#.',
        '#.##.###..##......#',
        '#.##.###.....##.#..',
        '#.##.###.....##..#.',
        '#.##.###.....##...#',
        '#.##.###......##.#.',
        '#.##.###......##..#',
        '#.##.###.......##.#',
        '#....##..###.##.#..',
        '#....##..###.##..#.',
        '#....##..###.##...#',
        '#....##..###..##.#.',
        '#....##..###..##..#',
        '#....##..###...##.#',
        '#.....##.###.##.#..',
        '#.....##.###.##..#.',
        '#.....##.###.##...#',
        '#.....##.###..##.#.',
        '#.....##.###..##..#',
        '#.....##.###...##.#',
        '.#...##..###.##.#..',
        '.#...##..###.##..#.',
        '.#...##..###.##...#',
        '.#...##..###..##.#.',
        '.#...##..###..##..#',
        '.#...##..###...##.#',
        '.#....##.###.##.#..',
        '.#....##.###.##..#.',
        '.#....##.###.##...#',
        '.#....##.###..##.#.',
        '.#....##.###..##..#',
        '.#....##.###...##.#',
        '..#..##..###.##.#..',
        '..#..##..###.##..#.',
        '..#..##..###.##...#',
        '..#..##..###..##.#.',
        '..#..##..###..##..#',
        '..#..##..###...##.#',
        '..#...##.###.##.#..',
        '..#...##.###.##..#.',
        '..#...##.###.##...#',
        '..#...##.###..##.#.',
        '..#...##.###..##..#',
        '..#...##.###...##.#',
        '...#.##..###.##.#..',
        '...#.##..###.##..#.',
        '...#.##..###.##...#',
        '...#.##..###..##.#.',
        '...#.##..###..##..#',
        '...#.##..###...##.#',
        '...#..##.###.##.#..',
        '...#..##.###.##..#.',
        '...#..##.###.##...#',
        '...#..##.###..##.#.',
        '...#..##.###..##..#',
        '...#..##.###...##.#',
        '....#.##.###.##.#..',
        '....#.##.###.##..#.',
        '....#.##.###.##...#',
        '....#.##.###..##.#.',
        '....#.##.###..##..#',
        '....#.##.###...##.#',
    ]),
]

@cache
def recursive_count_arrangements(value: str, pattern_str: str) -> int:
    pattern = [] if len(pattern_str) == 0 else [int(x) for x in pattern_str.split(',')]
    if not pattern:
        if '#' in value:  # have patterns that can't possibly match
            return 0
        else:
            return 1

    if sum(pattern) + len(pattern) - 1 > len(value):  # doesn't fit
        return 0

    size = pattern[0]
    result = 0
    reached_end = len(value) == size
    next_char = None if reached_end else value[size]
    potential_match = value[0:size]
    if '.' not in potential_match and next_char != '#':  # we have a match!
        # get results assuming match
        if reached_end:
            return 1 if len(pattern) == 1 else 0
        elif len(value) == size + 1:  # almost reached end
            if len(pattern) == 1:
                result = 1
        else:
            new_value = value[size + 1:] # we skip an extra 1 as it must be a '.' for a space between '#'s
            result = recursive_count_arrangements(new_value, ','.join([str(x) for x in pattern[1:]]))

    # if current char is # it's only valid to be part of a match
    # if we're already at the end, no point carrying on
    if not value[0] == '#' and not reached_end:
        # otherwise we also get results assuming not match
        new_value = value[1:]
        result += recursive_count_arrangements(new_value, ','.join([str(x) for x in pattern]))

    return result

@pytest.mark.parametrize('row, arrangements', test_arrangements)
def test_recursive_count_arrangements(row, arrangements):
    value, pattern = split_row(row)
    expected = len(arrangements)
    actual = recursive_count_arrangements(value, pattern)
    assert actual == expected

testdata = [
    ('???.### 1,1,3', 1),
    ('.??..??...?##. 1,1,3', 4),
    ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
    ('????.#...#... 4,1,1', 1),
    ('????.######..#####. 1,6,5', 4),
    ('?###???????? 3,2,1', 10),
]

def count_arrangements(row: str, unfold: bool) -> int:
    value, pattern = split_row(row)
    if unfold:
        value, pattern = unfold_input(value, pattern)
    count = recursive_count_arrangements(value, pattern)
    return count

@pytest.mark.parametrize("value, expected", testdata)
def test_count_arrangements(value, expected):
    actual = count_arrangements(value, False)
    assert actual == expected

def sum_all_arrangements(lines: list[str], unfold: bool) -> int:
    total = 0
    for i, row in enumerate(lines):
        total += count_arrangements(row, unfold)
    return total

def test_sum_all_arrangements():
    rows = [x for (x, y) in testdata]
    actual = sum_all_arrangements(rows, False)
    assert actual == 21

def test_sum_all_arrangements_unfolded():
    rows = [x for (x, y) in testdata]
    actual = sum_all_arrangements(rows, True)
    assert actual == 525152

if __name__ == '__main__':
    run()
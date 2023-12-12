from pathlib import Path
import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = sum_all_arrangements(lines)
    print(f'Day12 part 1: {result}')

def split_row(row: str) -> (str, list[int]):
    value = row.split(' ')[0]
    pattern = [int(x) for x in row.split(' ')[1].split(',')]
    return value, pattern

def find_arrangements(value: str, i: int, pattern: list[int]) -> list[str]:
    start = value[:i]
    if '?' in start:
        raise ValueError(f'unexpected ? in start of string {start}')
    if not pattern:
        if '#' in value[i:]: # have patterns that can't possibly match
            return []
        else:
            return [value.replace('?', '.')]
    size = pattern[0]
    if len(value) < i + size: # doesn't fit
        return []

    results = []
    reached_end = len(value) == i + size
    previous_char = None if i == 0 else value[i - 1]
    next_char = None if reached_end else value[i + size]
    potential_match = value[i:i + size]
    if '.' not in potential_match and next_char != '#' and previous_char != '#': # we have a match!
        # get results assuming match
        middle = ''.join(['#'] * size)
        end = '' if reached_end else '.' + value[i+size+1:]
        results += find_arrangements(start + middle + end, i+size+1, pattern[1:])


    # if current char is # it's only valid to be part of a match
    if not (value[i] == '#'):
        # otherwise we also get results assuming not match
        middle = '.'
        end = value[i+1:]
        results += find_arrangements(start + middle + end, i+1, pattern)
    return results

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

@pytest.mark.parametrize('row, expected', test_arrangements)
def test_find_arrangements(row, expected):
    value, pattern = split_row(row)
    actual = find_arrangements(value, 0, pattern)
    assert actual == expected

testdata = [
    ('???.### 1,1,3', 1),
    ('.??..??...?##. 1,1,3', 4),
    ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
    ('????.#...#... 4,1,1', 1),
    ('????.######..#####. 1,6,5', 4),
    ('?###???????? 3,2,1', 10),
]

def count_arrangements(row: str) -> int:
    value, pattern = split_row(row)
    arrangements = find_arrangements(value, 0, pattern)
    return len(arrangements)

@pytest.mark.parametrize("value, expected", testdata)
def test_count_arrangements(value, expected):
    actual = count_arrangements(value)
    assert actual == expected

def sum_all_arrangements(lines: list[str]) -> int:
    total = 0
    for row in lines:
        total += count_arrangements(row)
    return total

def test_sum_all_arrangements():
    rows = [x for (x, y) in testdata]
    actual = sum_all_arrangements(rows)
    assert actual == 21

if __name__ == '__main__':
    run()
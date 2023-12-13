from itertools import groupby
from pathlib import Path

import pytest


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')
    patterns = [list(g) for k, g in groupby(lines, key=lambda x: x == '') if not k]

    result1 = summarize_notes(patterns, False)
    print(f'Day13 part 1: {result1}')

    result2 = summarize_notes(patterns, True)
    print(f'Day13 part 2: {result2}')

def find_mirror_with_transpose(pattern: list[str], smudge: bool) -> (int, bool):
    horizontal_mirror = find_mirror(pattern, smudge)
    if horizontal_mirror is not None:
        return horizontal_mirror, False
    vertical_mirror = find_mirror(transpose(pattern), smudge)
    if vertical_mirror is not None:
        return vertical_mirror, True
    else:
        raise Exception(f'No mirror found in pattern: {pattern}')

def test_find_mirror_with_transpose():
    pattern = test_data[1]
    actual = find_mirror_with_transpose(pattern, False)
    assert actual == (3, False)

def test_find_mirror_with_transpose2():
    pattern = test_data[0]
    actual = find_mirror_with_transpose(pattern, False)
    assert actual == (4, True)

def test_find_mirror_with_transpose3():
    pattern = test_data[2]
    actual = find_mirror_with_transpose(pattern, False)
    assert actual == (0, False)

def test_find_mirror_with_transpose4():
    pattern = test_data[3]
    actual = find_mirror_with_transpose(pattern, False)
    assert actual == (0, True)

def transpose(pattern: list[str]) -> list[str]:
    return [''.join(x) for x in zip(*pattern)]

def test_transpose():
    data = ['123', '456']
    expected = ['14', '25', '36']
    assert transpose(data) == expected

def verify_mirror(pattern: list[str], mirror_index: int) -> bool:
    for i in reversed(range(mirror_index + 1)):
        j = (mirror_index + 1) + (mirror_index - i)
        if j == len(pattern):
            break
        if pattern[i] != pattern[j]:
            return False
    return True

test_data = [
    [
        '#.##..##.',
        '..#.##.#.',
        '##......#',
        '##......#',
        '..#.##.#.',
        '..##..##.',
        '#.#.##.#.',
    ],
    [
        '#...##..#',
        '#....#..#',
        '..##..###',
        '#####.##.',
        '#####.##.',
        '..##..###',
        '#....#..#',
    ],
    [
        '#......',
        '#......',
        '....#..',
        '#.#.###',
        '#####..',
        '###.##.',
        '...#.##',
        '#.#.###',
        '####.#.',
        '..##..#',
        '..##..#',
        '####.#.',
        '#.#.###',
        '...#.##',
        '###.##.',
        '###.#..',
        '#.#.###'
    ],
    [
        '...##..',
        '..#....',
        '..#....',
        '..###..',
        '###.#.#',
        '##..#.#',
        '.....##',
        '......#',
        '..#.#..',
    ],
]

@pytest.mark.parametrize('pattern, index, expected', [
    (test_data[1], 3, True),
    (test_data[1], 0, False),
    (test_data[2], 0, True),
    (transpose(test_data[3]), 0, True),
])
def test_verify_mirror(pattern, index, expected):
    assert verify_mirror(pattern, index) == expected

def match_except_smudge(pattern1: str, pattern2: str) -> bool:
    if len(pattern1) != len(pattern2):
        raise ValueError(f'pattern length don\'t match: {pattern1}, {pattern2}')
    smudge_count = 0
    for i in range(len(pattern1)):
        if pattern1[i] != pattern2[i]:
            smudge_count += 1
            if smudge_count > 1:
                return False
    return smudge_count == 1


@pytest.mark.parametrize('value1, value2, expected', [
    ('...', '..#', True),
    ('...', '...', False),
    ('##.', '...', False),
])
def test_match_except_smudge(value1, value2, expected):
    actual = match_except_smudge(value1, value2)
    assert actual == expected

def verify_smudged_mirror(pattern: list[str], mirror_index: int):
    smudge_count = 0
    for i in reversed(range(mirror_index + 1)):
        j = (mirror_index + 1) + (mirror_index - i)
        if j == len(pattern):
            break
        if pattern[i] != pattern[j]:
            if match_except_smudge(pattern[i], pattern[j]) and smudge_count == 0:
                smudge_count += 1
            else:
                return False
    return smudge_count == 1

def test_verify_smudged_mirror():
    assert verify_smudged_mirror(test_data[0], 2) == True
    assert verify_smudged_mirror(test_data[1], 0) == True
    # assert verify_smudged_mirror(test_data[2], 0) == True
    # assert verify_smudged_mirror(transpose(test_data[3]), 0) == True

def find_mirror(pattern: list[str], smudge: bool) -> int:
    potentials = [i for i in range(len(pattern) - 1) if pattern[i] == pattern[i + 1]]
    if smudge:
        potentials += [i for i in range(len(pattern) -1) if match_except_smudge(pattern[i], pattern[i+1])]
        mirrors = [p for p in potentials if verify_smudged_mirror(pattern, p)]
    else:
        mirrors = [p for p in potentials if verify_mirror(pattern, p)]

    if len(mirrors) > 1:
        raise Exception(f'Found {len(mirrors)} mirrors: {mirrors} in {pattern}')
    return mirrors[0] if mirrors else None

def test_find_mirror():
    pattern = test_data[1]
    actual = find_mirror(pattern, False)
    assert actual == 3

def get_summary(pattern: list[str], smudge: bool) -> int:
    index, is_vert = find_mirror_with_transpose(pattern, smudge)
    count = index + 1
    return count if is_vert else count * 100


def test_get_summary():
    assert get_summary(test_data[0], False) == 5
    assert get_summary(test_data[1], False) == 400

def summarize_notes(patterns: list[list[str]], smudge: bool) -> int:
    total = 0
    for pattern in patterns:
        total += get_summary(pattern, smudge)
    return total

def test_summarize_notes():
    actual = summarize_notes(test_data[:2], False)
    assert actual == 405

def test_summarize_notes2():
    actual = summarize_notes(test_data[:2], True)
    assert actual == 400

if __name__ == '__main__':
    run()

from itertools import groupby
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')
    patterns = [list(g) for k, g in groupby(lines, key=lambda x: x == '') if not k]

    result = summarize_notes(patterns)
    print(f'Day13 part 1: {result}')

def find_mirror_with_transpose(pattern: list[str]) -> (int, bool):
    horizontal_mirror = find_mirror(pattern)
    if horizontal_mirror is not None:
        return horizontal_mirror, False
    vertical_mirror = find_mirror(transpose(pattern))
    if vertical_mirror is not None:
        return vertical_mirror, True
    else:
        raise Exception(f'No mirror found in pattern: {pattern}')

def test_find_mirror_with_transpose():
    pattern = test_data[1]
    actual = find_mirror_with_transpose(pattern)
    assert actual == (3, False)

def test_find_mirror_with_transpose2():
    pattern = test_data[0]
    actual = find_mirror_with_transpose(pattern)
    assert actual == (4, True)

def test_find_mirror_with_transpose3():
    pattern = test_data[2]
    actual = find_mirror_with_transpose(pattern)
    assert actual == (0, False)

def test_find_mirror_with_transpose4():
    pattern = test_data[3]
    actual = find_mirror_with_transpose(pattern)
    assert actual == (0, True)

def transpose(pattern: list[str]) -> list[str]:
    return [''.join(x) for x in zip(*pattern)]

def test_transpose():
    data = ['123', '456']
    expected = ['14', '25', '36']
    assert transpose(data) == expected

def verify_mirror(pattern: list[str], mirror_index: int) -> bool:
    for i in reversed(range(mirror_index)):
        j = (mirror_index + 1) + (mirror_index - i)
        if j == len(pattern):
            break
        if pattern[i] != pattern[j]:
            return False
    return True

def test_verify_mirror():
    pattern = test_data[1]
    assert verify_mirror(pattern, 3) == True
    assert verify_mirror(pattern, 4) == False
    assert verify_mirror(test_data[2], 0) == True
    assert verify_mirror(transpose(test_data[3]), 0) == True

def find_mirror(pattern: list[str]) -> int:
    potentials = [i for i in range(len(pattern) -1) if pattern[i] == pattern[i+1]]
    mirrors = [p for p in potentials if verify_mirror(pattern, p)]
    if len(mirrors) > 1:
        raise Exception(f'Found {len(mirrors)} mirrors: {mirrors} in {pattern}')
    return mirrors[0] if mirrors else None

def test_find_mirror():
    pattern = test_data[1]
    actual = find_mirror(pattern)
    assert actual == 3

def get_summary(pattern: list[str]) -> int:
    index, is_vert = find_mirror_with_transpose(pattern)
    count = index + 1
    return count if is_vert else count * 100


def test_get_summary():
    assert get_summary(test_data[0]) == 5
    assert get_summary(test_data[1]) == 400

def summarize_notes(patterns: list[list[str]]) -> int:
    total = 0
    for pattern in patterns:
        total += get_summary(pattern)
    return total

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

def test_summarize_notes():
    actual = summarize_notes(test_data[:2])
    assert actual == 405

if __name__ == '__main__':
    run()

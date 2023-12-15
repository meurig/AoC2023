import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')
    init_seq = lines[0].split(',')

    result = sum_of_hashes(init_seq)
    print(f'Day15 part 1: {result}')


def aoc_hash(step: str) -> int:
    current = 0
    mult_factor = 17
    div_factor = 256
    for char in step:
        current += ord(char)
        current *= mult_factor
        current = current % div_factor
    return current


@pytest.mark.parametrize('step, expected', [
    ('HASH', 52),
    ('rn=1', 30),
    ('cm-', 253),
    ('qp=3', 97),
    ('cm=2', 47),
    ('qp-', 14),
    ('pc=4', 180),
    ('ot=9', 9),
    ('ab=5', 197),
    ('pc-', 48),
    ('pc=6', 214),
    ('ot=7', 231),
])
def test_aoc_has(step, expected):
    actual = aoc_hash(step)
    assert actual == expected

def sum_of_hashes(init_seq: list[str]) -> int:
    return sum([ aoc_hash(x) for x in init_seq ])

@pytest.mark.parametrize('line, expected', [
    ('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7', 1320),
])
def test_sum_of_hashes(line, expected):
    seq = line.split(',')
    actual = sum_of_hashes(seq)
    assert actual == expected

if __name__ == '__main__':
    run()

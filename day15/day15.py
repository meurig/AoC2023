from collections import OrderedDict

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')
    init_seq = lines[0].split(',')

    result1 = sum_of_hashes(init_seq)
    print(f'Day15 part 1: {result1}')

    result2 = sum_of_focusing_power(init_seq)
    print(f'Day15 part 2: {result2}')

def split_step(step: str) -> (str, int, str, int):
    if '-' in step:
        op_char = '-'
        label = step[:-1]
        focal_length = None
    elif '=' in step:
        op_char = '='
        parts = step.split('=')
        label = parts[0]
        focal_length = int(parts[1])
    else:
        raise ValueError(f'no - or = found in step: {step}')
    box_number = aoc_hash(label)
    return label, box_number, op_char, focal_length

@pytest.mark.parametrize('step, expected', [
    ('rn=1', ('rn', 0, '=', 1)),
    ('cm-', ('cm', 0, '-', None))
])
def test_split_step(step, expected):
    actual = split_step(step)
    assert actual == expected


def apply_seq(init_seq: list[str]) -> list[OrderedDict[str, int]]:
    lenses: list[OrderedDict[str, int]] = [OrderedDict() for _ in range(256) ]
    for step in init_seq:
        label, box_number, op_char, focal_length = split_step(step)
        if op_char == '=':
            lenses[box_number][label] = focal_length
        else:
            if label in lenses[box_number]:
                lenses[box_number].pop(label)
    return lenses

def test_apply_seq():
    init_seq = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')
    actual = apply_seq(init_seq)
    assert actual[0] == OrderedDict([('rn', 1), ('cm', 2)])
    assert actual[3] == OrderedDict([('ot', 7), ('ab', 5), ('pc', 6)])

def lens_focus_pow(box_number: int, slot_index: int, focal_length: int) -> int:
    a = 1 + box_number
    b = 1 + slot_index
    c = focal_length
    result = a * b * c
    return result

@pytest.mark.parametrize('box_number, slot_index, focal_length, expected', [
    (0, 0, 1, 1),
    (0, 1, 2, 4),
    (3, 0, 7, 28),
    (3, 1, 5, 40),
    (3, 2, 6, 72),
])
def test_lens_focus_pow(box_number, slot_index, focal_length, expected):
    actual = lens_focus_pow(box_number, slot_index, focal_length)
    assert actual == expected

def focus_power(box_number: int, lenses: OrderedDict[str, int]) -> int:
    result = 0
    for slot_index, focal_length in enumerate(lenses.values()):
        result += lens_focus_pow(box_number, slot_index, focal_length)
    return result

@pytest.mark.parametrize('box_number, lenses, expected', [
    (0, OrderedDict([('rn',1), ('cm', 2)]), 5),
    (3, OrderedDict([('ot', 7), ('ab', 5), ('pc', 6)]), 140),
])
def test_focus_power(box_number, lenses, expected):
    actual = focus_power(box_number, lenses)
    assert actual == expected

def sum_of_focusing_power(init_seq: list[str]) -> int:
    boxes = apply_seq(init_seq)
    return sum([ focus_power(box_number, lenses) for box_number, lenses in enumerate(boxes) ])

@pytest.mark.parametrize('line, expected', [
    ('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7', 145),
])
def test_sum_of_focusing_power(line, expected):
    seq = line.split(',')
    actual = sum_of_focusing_power(seq)
    assert actual == expected

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
    ('rn', 0),
    ('cm', 0),
    ('qp', 1),
    ('ot', 3)

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

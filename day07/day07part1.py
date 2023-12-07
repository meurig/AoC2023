from enum import Enum
from functools import cmp_to_key
from typing import List

import pytest
from pathlib import Path

class Rank(Enum):
    FiveOfAKind = 7  # AAAAA
    FourOfAKind = 6  # AA8AA
    FullHouse = 5    # 23332
    ThreeOfAKind = 4 # TTT98
    TwoPair = 3      # 23432
    OnePair = 2      # A23A4
    HighCard = 1     # 23456

class Card(Enum):
    A = 14
    K = 13
    Q = 12
    J = 11
    T = 10

def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_total_winnings(lines)
    print(f'Day07 part 1: {result}')


def get_rank(hand: str) -> Rank:
    counts = {}
    for card in hand:
        counts.update({card: counts.get(card, 0) + 1})
    if len(counts) == 1:
        return Rank.FiveOfAKind
    elif len(counts) == 2:
        if counts[hand[0]] == 4 or counts[hand[0]] == 1:
            return Rank.FourOfAKind
        else:
            return Rank.FullHouse
    elif len(counts) == 3:
        if max(counts.values()) == 3:
            return Rank.ThreeOfAKind
        else:
            return Rank.TwoPair
    elif len(counts) == 4:
        return Rank.OnePair
    elif len(counts) == 5:
        return Rank.HighCard
    else:
        raise Exception(f'Unable to determine Rank: {hand}')

@pytest.mark.parametrize('hand, expected', [
    ('AAAAA', Rank.FiveOfAKind),
    ('AA8AA', Rank.FourOfAKind),
    ('23332', Rank.FullHouse),
    ('TTT98', Rank.ThreeOfAKind),
    ('23432', Rank.TwoPair),
    ('A23A4', Rank.OnePair),
    ('23456', Rank.HighCard),
])
def test_get_rank(hand, expected):
    actual = get_rank(hand)
    assert actual == expected

def is_left_card_higher(left_card: str, right_card: str) -> bool:
    if left_card.isdigit() and right_card.isdigit():
        return int(left_card) > int(right_card)
    elif left_card.isdigit():
        return False
    elif right_card.isdigit():
        return True
    else:
        left = Card[left_card]
        right = Card[right_card]
        return left.value > right.value

@pytest.mark.parametrize('left_card, right_card, expected', [
    ('A', 'K', True),
    ('K', 'A', False),
    ('A', 'A', False),
    ('J', '9', True),
    ('8', '7', True),
    ('7', 'Q', False),
])
def test_is_left_card_higher(left_card, right_card, expected):
    actual = is_left_card_higher(left_card, right_card)
    assert actual == expected

def is_left_higher_by_card(left: str, right: str) -> bool:
    for x in range(5):
        left_card = left[x]
        right_card = right[x]
        if left_card != right_card:
            return is_left_card_higher(left_card, right_card)
    return False

@pytest.mark.parametrize('left, right, expected', [
    ('33332', '2AAAA', True),
    ('2AAAA', '33332', False),
    ('77888', '77788', True),
    ('77788', '77888', False),
])
def test_is_left_higher_by_card(left, right, expected):
    actual = is_left_higher_by_card(left, right)
    assert actual == expected

def compare_hands(left: str, right: str) -> int: # -ve means left higher, 0 means same
    if left == right:
        return 0
    left_rank = get_rank(left)
    right_rank = get_rank(right)
    if left_rank.value > right_rank.value:
        return -1
    elif right_rank.value > left_rank.value:
        return 1
    else:
        return -1 if is_left_higher_by_card(left, right) else 1

@pytest.mark.parametrize("left, right, expected", [
    ('32T3K', 'KK677', 1),
    ('KK677', 'KTJJT', -1),
])
def test_compare_hands(left, right, expected):
    actual = compare_hands(left, right)
    assert actual == expected

def compare_lines(left, right):
    left_hand = left.split()[0]
    right_hand = right.split()[0]
    return compare_hands(left_hand, right_hand)

def sort_lines(lines):
    return sorted(lines, key=cmp_to_key(compare_lines))

def test_sort_lines():
    expected = [
        'QQQJA 483',
        'T55J5 684',
        'KK677 28',
        'KTJJT 220',
        '32T3K 765',
    ]
    actual = sort_lines(test_lines)
    assert actual == expected

def sort_hands(hands: List[str]) -> List[str]:
    return sorted(hands, key=cmp_to_key(compare_hands))

test_lines= [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]

def test_sort_hands():
    hands = [ line.split()[0] for line in test_lines ]
    expected = [
        'QQQJA',
        'T55J5',
        'KK677',
        'KTJJT',
        '32T3K',
    ]
    actual = sort_hands(hands)
    assert actual == expected

def calc_total_winnings(lines: List[str]) -> int:
    sorted_lines = reversed(sort_lines(lines))
    total = 0
    for rank, line in enumerate(sorted_lines):
        total += (rank + 1) * int(line.split()[1])
    return total


def test_calc_total_winnings():
    lines = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]
    expected = 6440
    actual = calc_total_winnings(lines)
    assert actual == expected


if __name__ == '__main__':
    run()

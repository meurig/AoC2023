from enum import Enum
from functools import cmp_to_key
from typing import List

import pytest
from pathlib import Path

from day07.day07part1 import Rank

class Card(Enum):
    A = 14
    K = 13
    Q = 12
    T = 10
    J = 1

def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = calc_total_winnings(lines)
    print(f'Day07 part 2: {result}')


def get_rank(hand: str) -> Rank:
    counts = {}
    single_jack_bonus = False
    double_jack_bonus = False
    for card in hand:
        counts.update({card: counts.get(card, 0) + 1})
    if 'J' in counts:
        if counts['J'] == 5:
            return Rank.FiveOfAKind
        if counts['J'] == 4:
            return Rank.FiveOfAKind
        if counts['J'] == 3:
            if len(counts) == 2:
                return Rank.FiveOfAKind
            elif len(counts) == 3:
                return Rank.FourOfAKind
            else:
                raise Exception
        if counts['J'] == 2:
            double_jack_bonus = True
            # high card can't happen
            # one pair must be Js so becomes three of a kind
            # two pair becomes four of a kind (one pair is Js)
            # three of a kind can't happen
            # full house becomes five of a kind
            # four of a kind can't happen
        if counts['J'] == 1:
            single_jack_bonus = True
            # high card becomes one pair
            # one pair becomes three of a kind
            # two pair becomes Full House
            # three of a kind becomes four of a kind
            # full house can't happen
            # four of a kind becomes five of a kind


    if len(counts) == 1:
        return Rank.FiveOfAKind
    elif len(counts) == 2:
        if counts[hand[0]] == 4 or counts[hand[0]] == 1:
            if double_jack_bonus:
                raise Exception
            return Rank.FiveOfAKind if single_jack_bonus else Rank.FourOfAKind
        else:
            if single_jack_bonus:
                raise Exception
            return Rank.FiveOfAKind if double_jack_bonus else Rank.FullHouse
    elif len(counts) == 3:
        if max(counts.values()) == 3:
            if double_jack_bonus:
                raise Exception
            return Rank.FourOfAKind if single_jack_bonus else Rank.ThreeOfAKind
        else:
            if single_jack_bonus:
                return Rank.FullHouse
            elif double_jack_bonus:
                return Rank.FourOfAKind
            return Rank.TwoPair
    elif len(counts) == 4:
        return Rank.ThreeOfAKind if single_jack_bonus or double_jack_bonus else Rank.OnePair
    elif len(counts) == 5:
        if double_jack_bonus:
            raise Exception
        return Rank.OnePair if single_jack_bonus else Rank.HighCard
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

    left_value = int(left_card) if left_card.isdigit() else Card[left_card].value
    right_value = int(right_card) if right_card.isdigit() else Card[right_card].value
    return left_value > right_value

@pytest.mark.parametrize('left_card, right_card, expected', [
    ('A', 'K', True),
    ('K', 'A', False),
    ('A', 'A', False),
    ('J', '9', False),
    ('8', '7', True),
    ('7', 'Q', False),
    ('J', '2', False),
    ('2', 'J', True),
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
    ('KK677', 'KTJJT', 1),
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
        'KTJJT 220',
        'QQQJA 483',
        'T55J5 684',
        'KK677 28',
        '32T3K 765'
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
        'KTJJT',
        'QQQJA',
        'T55J5',
        'KK677',
        '32T3K'
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
    expected = 5905
    actual = calc_total_winnings(lines)
    assert actual == expected


if __name__ == '__main__':
    run()

from math import sqrt, ceil, floor
from typing import Dict, Tuple
import pytest

def run():
    # Time:        48     98     90     83
    # Distance:   390   1103   1112   1360
    races = {
        48: 390,
        98: 1103,
        90: 1112,
        83: 1360,
    }

    result = get_multiplied_margins_of_error(races)
    print(f'Day06 part 1: {result}')


def get_speeds_for_exact_matches(time, distance) -> Tuple[float, float]:
    # where T = total race time, d = record distance
    # through algebra we get: s^2 -T*s + d = 0 (standard quadratic form)
    # a = 1, b=-T, c = d
    # through the use of the quadratic formula we get:
    # s = (T +/- sqrt(T^2 - 4*d))/2
    a = (time - sqrt(pow(time, 2) - 4 * distance)) / 2
    b = (time + sqrt(pow(time, 2) - 4 * distance)) / 2
    return a, b

@pytest.mark.parametrize("time, distance, expected", [
    (7, 9, (2.0, 5.0)),
    (15, 40, (4.0, 11.0)),
])
def test_get_speeds_for_exact_matches(time, distance, expected):
    a, b = get_speeds_for_exact_matches(time, distance)
    x, y = expected
    assert a > x - 1.0
    assert a < x
    assert b > y
    assert b < y + 1.0

def test_get_speeds_for_exact_matches2():
    time, distance, expected = 30, 200, (10.0, 20.0) # this is an exact match
    a, b = get_speeds_for_exact_matches(time, distance)
    assert a == expected[0]
    assert b == expected[1]

def get_winning_limits(time, distance) -> Tuple[int, int]:
    a, b = get_speeds_for_exact_matches(time, distance)
    # add a tiny bit to ensure we win - it's not okay to exactly match the winning number
    win_margin = 0.000000000001
    a, b = a + win_margin, b - win_margin
    return int(ceil(a)), int(floor(b))

@pytest.mark.parametrize("time, distance, expected", [
    (7, 9, (2, 5)),
    (15, 40, (4, 11)),
    (30, 200, (11, 19)),
])
def test_get_winning_limits(time, distance, expected):
    actual = get_winning_limits(time, distance)
    assert actual == expected

def get_margin_of_error(time: int, distance: int) -> int:
    a, b = get_winning_limits(time, distance)
    return b - a + 1

@pytest.mark.parametrize("time, distance, expected", [
    (7, 9, 4),
    (15, 40, 8),

])
def test_get_margin_of_error(time, distance, expected):
    actual = get_margin_of_error(time, distance)
    assert actual == expected

def get_multiplied_margins_of_error(races: Dict[int, int]) -> int:
    result = 1
    for time, distance in races.items():
        result *= get_margin_of_error(time, distance)
    return result

def test_get_multiplied_margins_of_error():
    races = {
        7: 9,
        15: 40,
        30: 200,
    }
    expected = 288
    actual = get_multiplied_margins_of_error(races)
    assert actual == expected


if __name__ == '__main__':
    run()

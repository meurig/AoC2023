from typing import List, Tuple
import pytest


class MiniMapper:
    def __init__(self, map_string: str):
        my_map = map_string.split()
        self.dest_start = int(my_map[0])
        self.source_start = int(my_map[1])
        self.length = int(my_map[2])
        self.source_end = self.source_start + self.length -1
        self.dest_end = self.dest_start + self.length -1

    def get_source_range(self) -> Tuple[int, int]:
        return self.source_start, self.source_end

    def in_source_range(self, value: int) -> bool:
        return self.source_start <= value <= self.source_end

    def map(self, value: int) -> int:
        if not self.in_source_range(value):
            return value
        return value - self.source_start + self.dest_start


@pytest.mark.parametrize("value, expected", [(0,0), (97,97), (98,50), (99,51), (100,100)])
def test_mini_mapper_map(value, expected):
    map_string = "50 98 2"
    mapper = MiniMapper(map_string)
    actual = mapper.map(value)
    assert actual == expected


@pytest.mark.parametrize("value, expected", [(0, False), (97, False), (98, True), (99, True), (100, False)])
def test_mini_mapper_in_range(value, expected):
    map_string = "50 98 2"
    mapper = MiniMapper(map_string)
    actual = mapper.in_source_range(value)
    assert actual == expected


def combine_ranges(ranges1: List[Tuple[int, int]], ranges2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    result = set()
    a = sorted(ranges1)
    b = sorted(ranges2)
    while len(a) > 0 and len(b) > 0:
        a_tuple = a[0]
        b_tuple = b[0]
        start = min(a_tuple[0], b_tuple[0])
        if a_tuple[0] == start and b_tuple[0] == start: # ab
            end = min(a_tuple[1], b_tuple[1])
            if a_tuple[1] == end:
                result.add(a.pop(0))
            else:
                a[0] = (end+1, a_tuple[1])
            if b_tuple[1] == end:
                result.add(b.pop(0))
            else:
                b[0] = (end+1, b_tuple[1])
        elif start == a_tuple[0]: # a
            end = min(a_tuple[1], b_tuple[0])
            if a_tuple[1] == end:
                result.add(a.pop(0))
            else:
                result.add((start, end - 1))
                a[0] = (end, a_tuple[1])
        else:  # b
            end = min(a_tuple[0], b_tuple[1])
            if b_tuple[1] == end:
                result.add(b.pop(0))
            else:
                result.add((start, end - 1))
                b[0] = (end, b_tuple[1])
    for x in a:
        result.add(x)
    for x in b:
        result.add(x)
    return sorted(list(result))

def test_combine_ranges():
    a = [(10, 30), (50, 60)]
    b = [(20, 60)]
    expected = [
        (10, 19), # a
        (20, 30), # ab
        (31, 49), # b
        (50, 60), # ab
    ]
    actual = combine_ranges(a, b)
    assert actual == expected

def test_combine_ranges2():
    a = [(10, 30), (50, 55), (83,90)]
    b = [(20, 53), (80, 85)]
    expected = [
        (10, 19), # a
        (20, 30), # ab
        (31, 49), # b
        (50, 53), # ab
        (54, 55), # a
        (80, 82), # b
        (83, 85), # ab
        (86, 90), # a
    ]
    actual = combine_ranges(a, b)
    assert actual == expected

def test_combine_ranges3():
    a = [(10, 30)]
    b = [(10, 30)]
    expected = [
        (10, 30), # ab
    ]
    actual = combine_ranges(a, b)
    assert actual == expected

def is_in_range(value: int, input_range: Tuple[int, int]) -> bool:
    return input_range[0] <= value <= input_range[1]

@pytest.mark.parametrize("value, expected", [
    (11, False),
    (12, True),
    (25, True),
    (56, True),
    (57, False),
])
def test_is_in_range(value, expected):
    input_range = (12, 56)
    actual = is_in_range(value, input_range)
    assert actual == expected


def is_in_ranges(value: int, input_ranges: List[Tuple[int, int]]):
    for input_range in input_ranges:
        if is_in_range(value, input_range):
            return True
    return False

@pytest.mark.parametrize("value, expected", [
    (11, False),
    (12, True),
    (19, True),
    (20, False),
    (25, False),
    (49, False),
    (50, True),
    (56, True),
    (57, False),
])
def test_is_in_ranges(value, expected):
    input_ranges = [(12, 19), (50, 56)]
    actual = is_in_ranges(value, input_ranges)
    assert actual == expected

class Mapper:
    def __init__(self, minimaps: List[MiniMapper]):
        self.minimaps = minimaps

    def map(self, value: int):
        for mapper in self.minimaps:
            if mapper.in_source_range(value):
                return mapper.map(value)
        return value

    def get_source_ranges(self) -> List[Tuple[int, int]]:
        return [minimap.get_source_range() for minimap in self.minimaps]

    def map_ranges(self, input_ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        # get ranges which don't overlap:
        a = input_ranges
        self.get_source_ranges()
        new_ranges = combine_ranges(input_ranges, self.get_source_ranges())
        # because they don't overlap, if x is in a minimap range, then y is in the same range
        mapped_ranges = [
            (self.map(x), self.map(y)) for x, y in new_ranges if is_in_ranges(x, input_ranges)
        ]
        return sorted(mapped_ranges)

@pytest.mark.parametrize("value, expected", [(79,81), (14,14), (55,57), (13,13)])
def test_mapper_map(value, expected):
    map_strings = ["50 98 2", "52 50 48"]
    mapper = Mapper([MiniMapper(map_string) for map_string in map_strings])
    actual = mapper.map(value)
    assert actual == expected


@pytest.mark.parametrize("input_ranges, expected", [
    ([(79,81)], [(81,83)]),
    ([(40, 56)], [(40, 49), (52,58)]),
    ([(40, 56), (90, 99)], [(40,49),(50,51),(52,58),(92, 99)])
])
def test_mapper_map_ranges(input_ranges, expected):
    map_strings = ["50 98 2", "52 50 48"]
    mapper = Mapper([MiniMapper(map_string) for map_string in map_strings])
    actual = mapper.map_ranges(input_ranges)
    assert actual == expected

class ChainedMapper:
    def __init__(self, mappers: List[Mapper]):
        self.mappers = mappers

    def map(self, value: int):
        for mapper in self.mappers:
            value = mapper.map(value)
        return value

    def map_ranges(self, input_ranges):
        for mapper in self.mappers:
            input_ranges = mapper.map_ranges(input_ranges)
        return input_ranges

    def get_min_mapped(self, seeds: List[int]) -> int:
        mapped_values = [self.map(seed) for seed in seeds]
        return min(mapped_values)

    def get_min_mapped_range(self, input_ranges: List[Tuple[int, int]]) -> int:
        mapped_ranges = self.map_ranges(input_ranges)
        return min(mapped_ranges)[0]


test_mappers = [
        Mapper([MiniMapper(x) for x in [
            "50 98 2", "52 50 48"
        ]]),
        Mapper([MiniMapper(x) for x in [
            "0 15 37",
            "37 52 2",
            "39 0 15",
        ]]),
        Mapper([MiniMapper(x) for x in [
            "49 53 8",
            "0 11 42",
            "42 0 7",
            "57 7 4",
        ]]),
        Mapper([MiniMapper(x) for x in [
            "88 18 7",
            "18 25 70",
        ]]),
        Mapper([MiniMapper(x) for x in [
            "45 77 23",
            "81 45 19",
            "68 64 13",
        ]]),
        Mapper([MiniMapper(x) for x in [
            "0 69 1",
            "1 0 69",
        ]]),
        Mapper([MiniMapper(x) for x in [
            "60 56 37",
            "56 93 4",
        ]])
    ]

@pytest.mark.parametrize("value, expected", [(79,82), (14,43), (55,86), (13,35)])
def test_chained_mapper_map(value, expected):
    chained_mapper = ChainedMapper(test_mappers)
    actual = chained_mapper.map(value)
    assert actual == expected

def test_chained_mapped_get_min_mapped():
    test_seeds = [79, 14, 55, 13]
    chained_mapper = ChainedMapper(test_mappers)
    actual = chained_mapper.get_min_mapped(test_seeds)
    assert actual == 35

def test_chained_mapper_get_min_mapped_range():
    input_ranges = [(79, 92), (55, 67)]
    chained_mapper = ChainedMapper(test_mappers)
    actual = chained_mapper.get_min_mapped_range(input_ranges)
    assert actual == 46
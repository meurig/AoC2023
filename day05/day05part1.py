from typing import List

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / f'0.txt') as f:
        seeds = get_seeds(f.read().split('\n')[0])
    mappers = []
    for x in range(1, 8):
        with open(Path(__file__).parent / f'{x}.txt') as f:
            mappers.append(Mapper(f.read().split('\n')[1:]))
    chained_mapper = ChainedMapper(mappers)
    result = chained_mapper.get_min_mapped(seeds)
    print(f'DayX part 1: {result}')

def get_seeds(seed_string: str) -> List[int]:
    return [int(x) for x in seed_string.split(':')[1].strip().split()]

def test_get_seeds():
    test_seeds = 'seeds: 79 14 55 13'
    expected = [79, 14, 55, 13]
    actual = get_seeds(test_seeds)
    assert actual == expected

class MiniMapper:
    def __init__(self, map_string: str):
        my_map = map_string.split()
        self.dest_start = int(my_map[0])
        self.source_start = int(my_map[1])
        self.length = int(my_map[2])

    def in_range(self, value: int):
        return self.source_start <= value < self.source_start + self.length

    def map(self, value: int) -> int:
        if not self.in_range(value):
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
    actual = mapper.in_range(value)
    assert actual == expected


class Mapper:
    def __init__(self, map_strings: List[str]):
        self.minimaps = [MiniMapper(x) for x in map_strings]

    def map(self, value: int):
        for mapper in self.minimaps:
            if mapper.in_range(value):
                return mapper.map(value)
        return value

@pytest.mark.parametrize("value, expected", [(79,81), (14,14), (55,57), (13,13)])
def test_mapper_map(value, expected):
    map_strings = ["50 98 2", "52 50 48"]
    mapper = Mapper(map_strings)
    actual = mapper.map(value)
    assert actual == expected

class ChainedMapper:
    def __init__(self, mappers: List[Mapper]):
        self.mappers = mappers

    def map(self, value: int):
        for mapper in self.mappers:
            value = mapper.map(value)
        return value

    def get_min_mapped(self, seeds: List[int]) -> int:
        mapped_values = [self.map(seed) for seed in seeds]
        return min(mapped_values)



test_mappers = [
        Mapper(["50 98 2", "52 50 48"]),
        Mapper([
            "0 15 37",
            "37 52 2",
            "39 0 15",
        ]),
        Mapper([
            "49 53 8",
            "0 11 42",
            "42 0 7",
            "57 7 4",
        ]),
        Mapper([
            "88 18 7",
            "18 25 70",
        ]),
        Mapper([
            "45 77 23",
            "81 45 19",
            "68 64 13",
        ]),
        Mapper([
            "0 69 1",
            "1 0 69",
        ]),
        Mapper([
            "60 56 37",
            "56 93 4",
        ])
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


if __name__ == '__main__':
    run()

from typing import Tuple
from pathlib import Path
from day05.day05part1 import  get_seeds
from day05.mappers import Mapper, ChainedMapper, MiniMapper


def run():
    with open(Path(__file__).parent / f'0.txt') as f:
        seed_ranges = get_seeds_range(f.read().split('\n')[0])
    mappers = []
    for x in range(1, 8):
        with open(Path(__file__).parent / f'{x}.txt') as f:
            mappers.append(Mapper([MiniMapper(line) for line in f.read().split('\n')[1:]]))
    chained_mapper = ChainedMapper(mappers)
    result = chained_mapper.get_min_mapped_range(seed_ranges)
    print(f'Day05 part 2: {result}')

def get_seeds_range(seeds_string: str) -> [Tuple[int, int]]:
    seed_range_inputs = get_seeds(seeds_string)
    seeds = []
    for i, start in enumerate(seed_range_inputs):
        if i % 2 != 0:
            continue
        end = start + seed_range_inputs[i+1]
        seeds.append((start, end - 1))
    return seeds

def test_get_seeds_range():
    expected = [(79, 92), (55, 67)]
    actual = get_seeds_range("seeds: 79 14 55 13")
    assert actual == expected

if __name__ == '__main__':
    run()
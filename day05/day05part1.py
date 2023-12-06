from typing import List

from pathlib import Path

from day05.mappers import Mapper, ChainedMapper, MiniMapper


def run():
    with open(Path(__file__).parent / f'0.txt') as f:
        seeds = get_seeds(f.read().split('\n')[0])
    mappers = []
    for x in range(1, 8):
        with open(Path(__file__).parent / f'{x}.txt') as f:
            map_strings = f.read().split('\n')[1:]
            mini_mappers = [ MiniMapper(map_string) for map_string in map_strings ]
            mappers.append(Mapper(mini_mappers))
    chained_mapper = ChainedMapper(mappers)
    result = chained_mapper.get_min_mapped(seeds)
    print(f'Day05 part 1: {result}')

def get_seeds(seed_string: str) -> List[int]:
    return [int(x) for x in seed_string.split(':')[1].strip().split()]

def test_get_seeds():
    test_seeds = 'seeds: 79 14 55 13'
    expected = [79, 14, 55, 13]
    actual = get_seeds(test_seeds)
    assert actual == expected


if __name__ == '__main__':
    run()

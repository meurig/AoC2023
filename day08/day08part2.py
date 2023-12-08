from math import lcm
from typing import List, Dict, Tuple

import pytest
from pathlib import Path

from day08.day08part1 import parse_nodes


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    directions = lines[0]
    nodes = lines[2:]

    result = parallel_count_steps_to_end(directions, nodes)
    print(f'Day08 part 2: {result}')

def traverse_map(start_node: str, directions: str, node_map: Dict[str, Tuple[str, str]]) -> int:
    current_node = node_map[start_node]
    total_steps = 0
    while True:
        for direction in directions:
            total_steps += 1
            if direction == 'L':
                new_node = current_node[0]
            else:
                new_node = current_node[1]
            if new_node[2] == 'Z':
                break
            current_node = node_map[new_node]
        else:
            continue
        break
    return total_steps

def parallel_count_steps_to_end(directions: str, nodes: List[str]) -> int:
    node_map = parse_nodes(nodes)
    loop_length: Dict[str, int] = {}
    for starting_node in [ x for x in node_map.keys() if x[2] == 'A' ]:
        loop_length[starting_node] = traverse_map(starting_node, directions, node_map)
    result = lcm(*list(loop_length.values()))
    return result


if __name__ == '__main__':
    run()

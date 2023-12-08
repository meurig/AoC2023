import re
from typing import List, Tuple, Dict

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    directions = lines[0]
    nodes = lines[2:]

    result = count_steps_to_end(directions, nodes)
    print(f'Day08 part 1: {result}')



def parse_nodes(nodes: List[str]) -> Dict[str, Tuple[str, str]]:
    return {
        name: (left, right)
        for name, left, right in [
            parse_node_string(node) for node in nodes
        ]
    }

def test_parse_nodes():
    nodes = [
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ]
    expected = {
        'AAA': ('BBB', 'BBB'),
        'BBB': ('AAA', 'ZZZ'),
        'ZZZ': ('ZZZ', 'ZZZ'),
    }
    actual = parse_nodes(nodes)
    assert actual == expected

def parse_node_string(node: str) -> Tuple[str, str, str]:
    matches = re.findall(r'[A-Z]{3}', node)
    return matches[0], matches[1], matches[2]


def test_parse_node_string():
    node = 'AAA = (BBB, CCC)'
    expected = 'AAA', 'BBB', 'CCC'
    actual = parse_node_string(node)
    assert actual == expected


def traverse_map(directions: str, node_map: Dict[str, Tuple[str, str]]) -> int:
    current_node = node_map['AAA']
    total_steps = 0
    while True:
        for direction in directions:
            total_steps += 1
            if direction == 'L':
                new_node = current_node[0]
            else:
                new_node = current_node[1]
            if new_node == 'ZZZ':
                break
            current_node = node_map[new_node]
        else:
            continue
        break
    return total_steps

def count_steps_to_end(directions: str, nodes: List[str]):
    node_map = parse_nodes(nodes)
    result = traverse_map(directions, node_map)
    return result

def test_count_steps_to_end():
    directions = 'LLR'
    nodes = [
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ]
    expected = 6
    actual = count_steps_to_end(directions, nodes)
    assert actual == expected


if __name__ == '__main__':
    run()

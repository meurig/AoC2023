import copy
import time
from pathlib import Path

import pytest

from day19.day19part1 import Comparison, parse_workflows


def run():
    with open(Path(__file__).parent / 'Input1.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result = count_acceptable_combinations(lines)
    print(f'Day19 part 2: {result} (in {(time.time() - start_time):.2f}s)')

class Rule:
    def __init__(self, condition: str):
        if condition is None:
            raise ValueError(f'Unexpected None condition')
        self.condition = condition
        self.field = condition[0]
        self.comparison = Comparison(condition[1])
        self.value = int(condition[2:])

    def __str__(self):
        return self.condition

class Node:
    def __init__(self, label: str):
        self.label = label
        self.destinations: list[(Node, Rule)] = []

    def __str__(self):
        return self.label

    def add_destination(self, destination, condition: str):
        rule = None if condition is None else Rule(condition)
        self.destinations.append((destination, rule))

def create_nodes(lines: list) -> dict[str, Node]:
    workflows: dict[str, list[(str, str)]] = parse_workflows(lines)
    nodes = {label: Node(label) for label in workflows.keys()}
    nodes['A'] = Node('A')
    nodes['R'] = Node('R')
    for label, rules in workflows.items():
        node = nodes[label]
        for condition, destination in rules:
            dest_node = nodes[destination]
            node.add_destination(dest_node, condition)
    return nodes

class PartRange:
    def __init__(self, x_range: (int, int), m_range: (int, int), a_range: (int, int), s_range: (int, int)):
        self.lower_limit = {
            'x': x_range[0],
            'm': m_range[0],
            'a': a_range[0],
            's': s_range[0],
        }
        self.upper_limit = {
            'x': x_range[1],
            'm': m_range[1],
            'a': a_range[1],
            's': s_range[1],
        }

    def count_values(self) -> int:
        x_count = max(0, self.upper_limit['x'] + 1 - self.lower_limit['x'])
        m_count = max(0, self.upper_limit['m'] + 1 - self.lower_limit['m'])
        a_count = max(0, self.upper_limit['a'] + 1 - self.lower_limit['a'])
        s_count = max(0, self.upper_limit['s'] + 1 - self.lower_limit['s'])
        return x_count * m_count * a_count * s_count

@pytest.mark.parametrize('x_range, m_range, a_range, s_range, expected', [
    ((1, 1), (1, 1), (1, 1), (1, 1), 1),
    ((2, 1), (1, 1), (1, 1), (1, 1), 0),
    ((1, 2), (1, 1), (1, 1), (1, 1), 2),
    ((1, 2), (1, 2), (1, 2), (1, 2), 16),
    ((100, 2), (1, 2), (1, 2), (1, 2), 0),
])
def test_count_values(x_range: (int, int), m_range: (int, int), a_range: (int, int), s_range: (int, int), expected):
    part_range = PartRange(x_range, m_range, a_range, s_range)
    actual = part_range.count_values()
    assert actual == expected

def split_part_range(part_range: PartRange, rule: Rule) -> (PartRange, PartRange):
    passing = copy.deepcopy(part_range)
    failing = copy.deepcopy(part_range)
    if rule.comparison == Comparison.GT:
        passing.lower_limit[rule.field] = max(passing.lower_limit[rule.field], rule.value + 1)
        failing.upper_limit[rule.field] = min(failing.upper_limit[rule.field], rule.value)
    else:
        passing.upper_limit[rule.field] = min(passing.upper_limit[rule.field], rule.value - 1)
        failing.lower_limit[rule.field] = max(failing.lower_limit[rule.field], rule.value)
    return passing, failing

def test_split_part_range():
    part_range = PartRange((1, 10),(1, 10),(1, 10),(1, 10))
    rule = Rule('x>6')
    passing, failing = split_part_range(part_range, rule)
    assert passing.lower_limit['x'] == 7
    assert failing.upper_limit['x'] == 6

def test_split_part_range2():
    part_range = PartRange((1, 10),(1, 10),(1, 10),(1, 10))
    rule = Rule('x<6')
    passing, failing = split_part_range(part_range, rule)
    assert passing.upper_limit['x'] == 5
    assert failing.lower_limit['x'] == 6

def walk_all_paths(nodes: dict[str, Node]):
    node = nodes['in']
    part_range = PartRange((1,4000), (1,4000), (1,4000), (1,4000))
    acceptable_ranges = find_acceptable_part_ranges(node, part_range)
    value_count = sum([ a_range.count_values() for a_range in acceptable_ranges ])
    return value_count

def find_acceptable_part_ranges(node: Node, part_range: PartRange) -> list[PartRange]:
    result = []
    if node.label == 'A':
        return [part_range]
    if node.label == 'R':
        return []
    for destination, rule in node.destinations:
        if rule is None:
            return result + find_acceptable_part_ranges(destination, part_range)
        else:
            passing, part_range = split_part_range(part_range, rule)
            result += find_acceptable_part_ranges(destination, passing)
    raise Exception(f'Not all paths lead to A or R at node: {node}')

def count_acceptable_combinations(lines: list) -> int:
    nodes = create_nodes(lines)
    result = walk_all_paths(nodes)
    return result


test_workflows = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
]

def test_count_acceptable_combinations():
    expected = 167409079868000
    actual = count_acceptable_combinations(test_workflows)
    assert actual == expected

if __name__ == '__main__':
    run()
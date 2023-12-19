import time
from enum import StrEnum
from pathlib import Path

def run():
    with open(Path(__file__).parent / 'Input1.txt') as f:
        workflows = f.read().split('\n')
    with open(Path(__file__).parent / 'Input2.txt') as f:
        parts = f.read().split('\n')

    start_time = time.time()
    result = sum_ratings_of_accepted_parts(workflows, parts)
    print(f'Day19 part 1: {result} (in {(time.time() - start_time):.2f}s)')

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

test_parts = [
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}',
]

def parse_workflows(lines: list[str]) -> dict[str, list[(str, str)]]:
    workflows: dict[str, list[(str, str)]] = {}
    for line in lines:
        parts = line.split('{')
        label = parts[0]
        rules_str = parts[1][:-1].split(',')
        rules = []
        for rule in rules_str:
            parts = rule.split(':')
            if len(parts) == 1:
                condition = None
                destination = parts[0]
            else:
                condition = parts[0]
                destination = parts[1]
            rules.append((condition, destination))
        workflows[label] = rules
    return workflows

def parse_parts(lines: list[str]) -> list[dict[str, int]]:
    parts: list[(int, int, int, int)] = []
    for line in lines:
        attributes = line[1:-1].split(',')
        part = {
            'x': int(attributes[0][2:]),
            'm': int(attributes[1][2:]),
            'a': int(attributes[2][2:]),
            's': int(attributes[3][2:]),
        }
        parts.append(part)
    return parts

class Comparison(StrEnum):
    GT = '>'
    LT = '<'

def apply_workflow_to_part(rules: list[(str, str)], part: dict[str, int]) -> str:
    for condition, destination in rules:
        if condition is None:
            return destination
        field = condition[0]
        comparison = Comparison(condition[1])
        value = int(condition[2:])
        if comparison == Comparison.GT:
            if part[field] > value:
                return destination
        else:
            if part[field] < value:
                return destination

def apply_workflows_to_part(workflows: dict[str, list[(str, str)]], part: dict[str, int]) -> str:
    workflow_label = 'in'
    while workflow_label != 'A' and workflow_label != 'R':
        workflow = workflows[workflow_label]
        workflow_label = apply_workflow_to_part(workflow, part)
    return workflow_label


def sum_ratings_of_accepted_parts(workflows: list[str], parts: list[str]) -> int:
    workflows = parse_workflows(workflows)
    parts = parse_parts(parts)
    accepted_parts = [ part for part in parts if apply_workflows_to_part(workflows, part) == 'A' ]
    result = sum([ sum(list(part.values())) for part in accepted_parts ])
    return result

def test_sum_ratings_of_accepted_parts():
    workflows = test_workflows
    parts = test_parts
    expected = 19114
    actual = sum_ratings_of_accepted_parts(workflows, parts)
    assert actual == expected

if __name__ == '__main__':
    run()

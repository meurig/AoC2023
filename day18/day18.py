import time
from copy import deepcopy
from enum import Enum, StrEnum
from pathlib import Path

from day05.mappers import combine_ranges


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    start_time = time.time()
    result = calc_pit_capacity(lines)
    print(f'Day18 part 1: {result} (in {(time.time() - start_time):.2f}s)')

    start_time = time.time()
    result2 = calc_pit_capacity2(lines)
    print(f'Day18 part 2: {result2} (in {(time.time() - start_time):.2f}s)')

class Heading(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class StrHeading(StrEnum):
    RIGHT = 'R'
    DOWN = 'D'
    LEFT = 'L'
    UP = 'U'

test_input = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]

def parse_inputs2(data: list[str]) -> list[(Heading, int)]:
    result = []
    for row in data:
        parts = row.split(' ')
        hex_direction = parts[2][7:-1]
        hex_distance = parts[2][2:-2]
        direction = Heading(int(hex_direction, 16))
        distance = int(hex_distance, 16)
        result.append((direction, distance))
    return result

def test_parse_inputs2():
    actual = parse_inputs2(test_input)
    assert actual[0][0] == Heading.RIGHT
    assert actual[0][1] == 461937
    assert actual[1][0] == Heading.DOWN
    assert actual[1][1] == 56407
    assert actual[2][0] == Heading.RIGHT
    assert actual[2][1] == 356671

def parse_inputs(data: list[str]) -> list[(StrHeading, int)]:
    result = []
    for row in data:
        parts = row.split(' ')
        direction = StrHeading(parts[0])
        distance = int(parts[1])
        result.append((direction, distance))
    return result

def test_parse_inputs():
    actual = parse_inputs(test_input)
    assert actual[0][0] == StrHeading.RIGHT
    assert actual[0][1] == 6
    assert actual[1][0] == StrHeading.DOWN
    assert actual[1][1] == 5
    assert actual[2][0] == StrHeading.LEFT
    assert actual[2][1] == 2

def build_node_graph(steps: list[(Heading | StrHeading, int)]) -> dict[int, list[int]]:
    x, y = 0, 0
    x_min, y_min = x, y
    offset_nodes: dict[int, list[int]] = {}
    for heading, distance in steps:
        match heading:
            case StrHeading.RIGHT | Heading.RIGHT:
                x, y = x, y + distance
            case StrHeading.LEFT | Heading.LEFT:
                x, y = x, y - distance
            case StrHeading.DOWN | Heading.DOWN:
                x, y = x + distance, y
            case StrHeading.UP | Heading.UP:
                x, y = x - distance, y
        if x in offset_nodes:
            offset_nodes[x].append(y)
        else:
            offset_nodes[x] = [y]
        x_min = min(x_min, x)
        y_min = min(y_min, y)

    nodes: dict[int, list[int]] = {}
    for x, node_list in sorted(offset_nodes.items()):
        nodes[x - x_min] = sorted([y - y_min for y in node_list])

    return nodes

def calc_pit_capacity(data: list[str]) -> int:
    steps = parse_inputs(data)
    nodes = build_node_graph(steps)
    area = calc_pit_capacity_given_nodes(nodes)
    return area

def calc_pit_capacity2(data: list[str]) -> int:
    steps = parse_inputs2(data)
    nodes = build_node_graph(steps)
    area = calc_pit_capacity_given_nodes(nodes)
    return area

def calc_pit_capacity_given_nodes(nodes: dict[int, list[int]]) -> int:
    # sort the nodes by row id and iterate down the map
    # at each row with a node on it, add the area of rectangles in the preceding slice
    # take care on the row with nodes - it's volume is the intersection of the old and new slices
    slices = []
    area = 0
    prev_row = None
    for row, node_list in nodes.items():
        area += calc_rect_area(slices, prev_row, row)
        old_slices = deepcopy(slices)
        update_slices(slices, node_list)
        area += calc_slice_area(slices, old_slices)
        prev_row = row
    return area

def calc_slice_area(slices, old_slices) -> int:
    combined = combine_ranges(slices, old_slices)
    areas = [ b + 1 - a for a, b in combined ]
    return sum(areas)

def test_calc_slice_area():
    expected = 7
    old_slices = [(2, 6)]
    slices = [(0, 4)]
    actual = calc_slice_area(slices, old_slices)
    assert actual == expected

def calc_rect_area(slices, prev_row, row) -> int:
    area = 0
    for a, b in slices:
        width = b + 1 - a
        height = row - prev_row - 1
        area += width * height
    return area

def update_slices(slices, node_list) -> None:
    for i in range(0, len(node_list), 2):
        c, d = node_list[i], node_list[i + 1]
        if not slices:
            slices.append((c, d))
            continue
        interacting_slices = get_interacting_slices(slices, c, d)

        if not interacting_slices:  # if it's not touching an existing slice, add it
            slices.append((c, d))
        elif len(interacting_slices) == 2:
            a, b = interacting_slices[0]
            e, f = interacting_slices[1]
            if slices_all_touch(a, b, c, d, e, f):  # if it joins two existing slices, merge them
                slices.remove((a, b))
                slices.remove((e, f))
                slices.append((a, f))
                slices.sort()
            else:
                raise NotImplementedError(f'Unexpected combo of 3 touching slices: {[(a, b), (c, d), (e, f)]}')
        elif len(interacting_slices) == 1:
            a, b = interacting_slices[0]
            if slices_are_identical(a, b, c, d):  # if it's equal to an existing slice, remove it
                slices.remove((a, b))
            elif slice_2_is_within_slice_1(a, b, c, d):  # if it's within existing slice, split it
                slices.remove((a, b))
                slices.append((a, c))
                slices.append((d, b))
                slices.sort()
            elif slices_touch_outside(a, b, c, d):  # if it's adjacent (out) to existing slice, expand it
                slices.remove((a, b))
                slices.append((min(a, c), max(b, d)))
                slices.sort()
            elif slices_touch_inside_left(a, b, c, d):  # if it's adjacent (in) to existing slice, shrink it
                slices.remove((a, b))
                slices.append((d, b))
                slices.sort()
            elif slices_touch_inside_right(a, b, c, d):
                slices.remove((a, b))
                slices.append((a, c))
                slices.sort()
            else:
                raise ValueError(f'unexpected combination: {[(a, b), (c, d)]}')
        else:
            raise NotImplementedError(f'Unexpected number of interacting slices: {len(interacting_slices)}')

def slices_all_touch(a, b, x, y, c, d) -> bool:
    return b == x and y == c

def slices_are_distinct(a, b, x, y) -> bool:
    return a > y or x > b

def slices_are_identical(a, b, x, y) -> bool:
    return a == x and b == y

def slice_2_is_within_slice_1(a, b, x, y) -> bool:
    return a < x and b > y

def slices_touch_outside(a, b, x, y) -> bool:
    return a == y or b == x

def slices_touch_inside_left(a, b, x, y) -> bool:
    return a == x and b > y

def slices_touch_inside_right(a, b, x, y) -> bool:
    return a < x and b == y

def get_interacting_slices(slices: list[(int, int)], x, y) -> list[(int, int)]:
    return [ (a, b) for a, b in slices if not slices_are_distinct(a, b, x, y) ]

def test_calc_pit_capacity2():
    expected = 952408144115
    actual = calc_pit_capacity2(test_input)
    assert actual == expected

def test_calc_pit_capacity():
    expected = 62
    actual = calc_pit_capacity(test_input)
    assert actual == expected

if __name__ == '__main__':
    run()
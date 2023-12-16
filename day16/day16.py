from enum import Enum, StrEnum

import pytest
from pathlib import Path


def run():
    with open(Path(__file__).parent / 'Input.txt') as f:
        lines = f.read().split('\n')

    result = count_energised_tiles(lines)
    print(f'DayX part 1: {result}')

class Heading(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

class Tile(StrEnum):
    EMPTY = '.'
    MIRROR_RIGHT_UP = '/'
    MIRROR_RIGHT_DOWN = '\\'
    VERT_SPLIT = '|'
    HORIZ_SPLIT = '-'

def in_bounds(position: (int, int), lines: list[str]) -> bool:
    x, y = position
    ok_top_and_bottom = 0 <= x < len(lines)
    ok_left_and_right = 0 <= y < len(lines[0])
    return ok_top_and_bottom and ok_left_and_right

def move(position: (int, int), direction: Heading) -> (int, int):
    x, y = position
    match direction:
        case Heading.RIGHT:
            return x, y + 1
        case Heading.LEFT:
            return  x, y - 1
        case Heading.DOWN:
            return x + 1, y
        case Heading.UP:
            return x - 1, y
    raise ValueError(f'unexpected heading: {direction}')


def calc_new_positions(lines: list[str], start_pos: (int, int), direction: Heading) -> list[((int, int), Heading)]:
    x, y = start_pos
    current_char = lines[x][y]
    match current_char:
        case Tile.EMPTY:
            return [(move(start_pos, direction), direction)]
        case Tile.MIRROR_RIGHT_UP:
            match direction:
                case Heading.RIGHT:
                    return [(move(start_pos, Heading.UP), Heading.UP)]
                case Heading.LEFT:
                    return [(move(start_pos, Heading.DOWN), Heading.DOWN)]
                case Heading.DOWN:
                    return [(move(start_pos, Heading.LEFT), Heading.LEFT)]
                case Heading.UP:
                    return [(move(start_pos, Heading.RIGHT), Heading.RIGHT)]
        case Tile.MIRROR_RIGHT_DOWN:
            match direction:
                case Heading.RIGHT:
                    return [(move(start_pos, Heading.DOWN), Heading.DOWN)]
                case Heading.LEFT:
                    return [(move(start_pos, Heading.UP), Heading.UP)]
                case Heading.DOWN:
                    return [(move(start_pos, Heading.RIGHT), Heading.RIGHT)]
                case Heading.UP:
                    return [(move(start_pos, Heading.LEFT), Heading.LEFT)]
        case Tile.VERT_SPLIT:
            match direction:
                case (Heading.RIGHT | Heading.LEFT):
                    return [ (move(start_pos, Heading.DOWN), Heading.DOWN),
                             (move(start_pos, Heading.UP), Heading.UP)]
                case (Heading.UP | Heading.DOWN):
                    return [(move(start_pos, direction), direction)]
        case Tile.HORIZ_SPLIT:
            match direction:
                case (Heading.RIGHT | Heading.LEFT):
                    return [(move(start_pos, direction), direction)]
                case (Heading.UP | Heading.DOWN):
                    return [(move(start_pos, Heading.RIGHT), Heading.RIGHT),
                            (move(start_pos, Heading.LEFT), Heading.LEFT)]
def traverse(lines: list[str], current_pos: (int, int), direction: Heading, visited: set[((int, int), Heading)]) -> set[((int, int), Heading)]:
    new_positions = calc_new_positions(lines, current_pos, direction)
    visited.add((current_pos, direction))
    while len(new_positions) == 1:
        new_position, new_heading = new_positions[0]
        if in_bounds(new_position, lines):
            if (new_position, new_heading) not in visited:
                visited.add((new_position, new_heading))
                new_positions = calc_new_positions(lines, new_position, new_heading)
            else:
                new_positions = []
        else:
            new_positions = []
    for new_position, new_heading in new_positions:
        if in_bounds(new_position, lines):
            if (new_position, new_heading) not in visited:
                visited.update(traverse(lines, new_position, new_heading, visited))
    return visited

def test_traverse():
    print()
    lines = get_test_data()
    visited = traverse(lines, (0,0), Heading.RIGHT, set([]))
    actual = { position for position, heading in visited }
    assert (0, 0) in actual
    assert (0, 1) in actual
    assert (0, 2) in actual
    assert (0, 3) in actual
    assert (1, 0) not in actual
    assert (1, 1) in actual
    assert (1, 2) not in actual
    assert (1, 3) not in actual
    assert (2, 0) not in actual
    assert (2, 1) in actual
    assert (2, 2) not in actual
    assert (2, 3) not in actual

def count_energised_tiles(lines: list[str]) -> int:
    visited = traverse(lines, (0,0), Heading.RIGHT, set([]))
    energised = {position for position, heading in visited}
    return len(energised)

def get_test_data() -> list[str]:
    with open(Path(__file__).parent / 'test_input.txt') as f:
        lines = f.read().split('\n')
    return lines

def test_get_test_data():
    expected = [
        r'.|...\....',
        r'|.-.\.....',
        r'.....|-...',
        r'........|.',
        r'..........',
        '.........\\',
        r'..../.\\..',
        r'.-.-/..|..',
        '.|....-|.\\',
        r'..//.|....',
    ]
    actual = get_test_data()
    assert actual == expected

def test_count_energised_tiles():
    expected = 46
    actual = count_energised_tiles(get_test_data())
    assert actual == expected

if __name__ == '__main__':
    run()

from dataclasses import dataclass
from aoc24 import day_data, Vec, Grid
from enum import Enum
from heapq import heappop, heappush
from itertools import groupby

TEST_INPUT = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

TEST_INPUT_B = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


class Orientation(Enum):

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_left(self):
        return Orientation((self.value - 1) % 4)

    def turn_right(self):
        return Orientation((self.value + 1) % 4)

    def inverse(self):
        return Orientation((self.value + 2) % 4)

    def move(self, position):
        x, y = position
        if self == Orientation.NORTH:
            return Vec(x, y - 1)
        elif self == Orientation.EAST:
            return Vec(x + 1, y)
        elif self == Orientation.SOUTH:
            return Vec(x, y + 1)
        elif self == Orientation.WEST:
            return Vec(x - 1, y)


def bearing(fr, to):
    x_direction = to.x - fr.x
    y_direction = to.y - fr.y

    bearing = set()

    if x_direction > 0:
        bearing.add(Orientation.EAST)
    if x_direction < 0:
        bearing.add(Orientation.WEST)
    if y_direction > 0:
        bearing.add(Orientation.SOUTH)
    if y_direction < 0:
        bearing.add(Orientation.NORTH)

    return bearing


def turns(state, target):

    orientation = state.orientation
    target_bearing = bearing(state.position, target)

    target_bearing &= {orientation}

    if orientation.inverse() in target_bearing:
        return 2
    else:
        return len(target_bearing)


@dataclass
class State:
    position: Vec
    orientation: Orientation
    cost: int

    def options(self):
        return [
            State(self.position, self.orientation.turn_left(), self.cost + 1000),
            State(self.position, self.orientation.turn_right(), self.cost + 1000),
            State(
                self.orientation.move(self.position), self.orientation, self.cost + 1
            ),
        ]

    def __lt__(self, other):
        return self.cost < other.cost


@dataclass
class Puzzle:
    grid: Grid
    start: Vec
    end: Vec

    @staticmethod
    def parse(data_source):
        return Puzzle(day_data(data_source).grid())

    def __init__(self, grid):
        self.grid = grid
        self.start = grid.find("S").pop()
        self.end = grid.find("E").pop()
        self.state = State(self.start, Orientation.EAST, 0)

    def start_state(self):
        return State(self.start, Orientation.EAST, 0)

    def options(self, state):
        return [
            s
            for s in state.options()
            if self.grid.bound(s.position) and self.grid[s.position] != "#"
        ]


def a_star(puzzle):

    def heuristic(state):
        return manhattan(state.position, puzzle.end) + turns(state, puzzle.end) * 1000

    # heuristic, path
    start_state = puzzle.start_state()
    frontier = [(heuristic(start_state), [start_state])]

    best_costs = {}

    def expand_frontier(option):
        if (
            best_costs.get((option.position, option.orientation), float("inf"))
            >= option.cost
        ):
            best_costs[(option.position, option.orientation)] = option.cost
            return option

    while frontier:
        current_path = heappop(frontier)[1]
        if current_path[-1].position == puzzle.end:
            yield current_path
        else:
            for option in puzzle.options(current_path[-1]):
                if expand_frontier(option):
                    h = heuristic(option)
                    heappush(
                        frontier,
                        (h + option.cost, current_path + [option]),
                    )


def day16a(puzzle):
    """
    >>> day16a(Puzzle.parse(TEST_INPUT))
    7036
    >>> day16a(Puzzle.parse(TEST_INPUT_B))
    11048
    """
    return next(a_star(puzzle))[-1].cost


def day16b(puzzle):
    """
    >>> day16b(Puzzle.parse(TEST_INPUT))
    45
    >>> day16b(Puzzle.parse(TEST_INPUT_B))
    64
    """
    paths = next(groupby(a_star(puzzle), lambda path: path[-1].cost))[1]
    locations = set()
    for path in paths:
        for state in path:
            locations.add(state.position)
    return len(locations)


def main():
    puzzle = Puzzle.parse(16)
    print(f"Day 16a: {day16a(puzzle)}")
    print(f"Day 16b: {day16b(puzzle)}")


if __name__ == "__main__":
    main()

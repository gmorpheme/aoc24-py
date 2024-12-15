from aoc24 import day_data, Vec, Grid
from enum import Enum
from functools import reduce
import os
import time

TEST_INPUT_A = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

TEST_INPUT_B = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

TEST_INPUT_C = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

def parse(data_source):
    before, after = day_data(data_source).split()
    plan = Plan(before.grid())
    movements = [Movement.parse(c) for c in after.text() if c != "\n"]
    return plan, movements

class Movement(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def parse(text):
        match text:
            case "^":
                return Movement.UP
            case "v":
                return Movement.DOWN
            case "<":
                return Movement.LEFT
            case ">":
                return Movement.RIGHT

    def shift(self, vec):
        match self:
            case Movement.UP:
                return Vec(vec[0], vec[1] - 1)
            case Movement.DOWN:
                return Vec(vec[0], vec[1] + 1)
            case Movement.LEFT:
                return Vec(vec[0] - 1, vec[1])
            case Movement.RIGHT:
                return Vec(vec[0] + 1, vec[1])

    def inverse(self):
        match self:
            case Movement.UP:
                return Movement.DOWN
            case Movement.DOWN:
                return Movement.UP
            case Movement.LEFT:
                return Movement.RIGHT
            case Movement.RIGHT:
                return Movement.LEFT


class Plan:

    def __init__(self, grid):
        self.grid = grid
        self.fish = grid.find("@").pop()

    def beam(self, movement):
        loc = self.fish
        while self.grid[loc] != "#":
            yield loc
            loc = movement.shift(loc)

    def move(self, movement):
        beam = list(self.beam(movement))
        chars = [self.grid[loc] for loc in beam]
        try:
            space_index = chars.index(".")
            replacement = ['.'] + chars[:space_index]
            for loc, c in zip(beam, replacement):
                self.grid[loc] = c
                if c == "@":
                    self.fish = loc
        except ValueError:
            pass

    def gps_value(self):
        return sum(p.x + p.y * 100 for p in self.grid.find("O"))

    def dump(self):
        self.grid.dump()

    def to_plan_b(self):
        return PlanB.from_a_grid(self.grid)


def expand(c):
    match c:
        case "#":
            return "##"
        case ".":
            return ".."
        case "@":
            return "@."
        case "O":
            return "[]"

class PlanB:

    def __init__(self, rows):
        self.grid = Grid(rows)
        self.fish = self.grid.find("@").pop()

    @staticmethod
    def from_a_grid(grid):
        rows = [sum((list(expand(c)) for c in row),[]) for row in grid.rows]
        return PlanB(rows)

    def beam(self, movement):
        loc = self.fish
        while self.grid[loc] != "#":
            yield loc
            loc = movement.shift(loc)

    def move(self, movement):
        if movement in [Movement.LEFT, Movement.RIGHT]:
            self.move_horizontal(movement)
        else:
            self.move_vertical(movement)

    def move_horizontal(self, movement):
        beam = list(self.beam(movement))
        chars = [self.grid[loc] for loc in beam]
        try:
            space_index = chars.index(".")
            replacement = ['.'] + chars[:space_index]
            for loc, c in zip(beam, replacement):
                self.grid[loc] = c
                if c == "@":
                    self.fish = loc
        except ValueError:
            pass

    def affected_cells(self, movement):
        row = [self.fish]
        rows = [row]
        while True:
            next_row = []
            for x in row:
                if self.grid[x] != ".":
                    x1 = movement.shift(x)
                    match self.grid[x1]:
                        case "#":
                            return []
                        case ".":
                            next_row.append(x1)
                        case "[":
                            next_row.append(x1)
                            next_row.append(Movement.RIGHT.shift(x1))
                        case "]":
                            next_row.append(x1)
                            next_row.append(Movement.LEFT.shift(x1))
            row = next_row
            rows.append(row)
            if all(self.grid[x] == '.' for x in row):
                return rows

    def move_vertical(self, movement):
        if beam := self.affected_cells(movement):
            all = reduce(set.union, map(set, beam))
            for row in reversed(beam):
                for loc in row:
                    precursor = movement.inverse().shift(loc)
                    if precursor in all:
                        self.grid[loc] = self.grid[precursor]
                    else:
                        self.grid[loc] = "."
            self.fish = movement.shift(self.fish)
            self.grid[self.fish] = "@"

    def gps_value(self):
        return sum(p.x + p.y * 100 for p in self.grid.find("["))

    def dump(self):
        self.grid.dump()



def day15a(plan, movements):
    """
    >>> day15a(*parse(TEST_INPUT_A))
    2028
    >>> day15a(*parse(TEST_INPUT_B))
    10092
    """
    for m in movements:
        plan.move(m)
    return plan.gps_value()


def day15b(plan, movements):
    """
    >>> plan, movements = parse(TEST_INPUT_B)
    >>> plan_b = plan.to_plan_b()
    >>> day15b(plan_b, movements)
    9021
    """
    for m in movements:
        plan.move(m)
    return plan.gps_value()

def main():
    plan, movements = parse(15)
    plan_b = plan.to_plan_b()
    print(f"Day 15a: {day15a(plan, movements)}")
    print(f"Day 15b: {day15b(plan_b, movements)}")

if __name__ == "__main__":
    main()

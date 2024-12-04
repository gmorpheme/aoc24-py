from aoc24 import day_data, Grid
from collections import deque

TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


class CrissCross:

    def __init__(self, grid):
        self.grid = grid

    def columns(self):
        for i in range(self.grid.width):
            yield [row[i] for row in self.grid.rows]

    def rows(self):
        for row in self.grid.rows:
            yield row

    def upward_diagonal(self, start_x, start_y):
        x = start_x
        y = start_y
        while 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            yield self.grid[(x, y)]
            x += 1
            y -= 1

    def upward_diagonals(self):
        for y in range(self.grid.height):
            yield self.upward_diagonal(0, y)

        for x in range(1, self.grid.width):
            yield self.upward_diagonal(x, self.grid.height - 1)

    def downward_diagonal(self, start_x, start_y):
        x = start_x
        y = start_y
        while 0 <= x < self.grid.width and 0 <= y < self.grid.height:
            yield self.grid[(x, y)]
            x += 1
            y += 1

    def downward_diagonals(self):
        for y in range(self.grid.height):
            yield self.downward_diagonal(0, y)

        for x in range(1, self.grid.width):
            yield self.downward_diagonal(x, 0)

    def all_lines(self):
        yield from self.rows()
        yield from self.columns()
        yield from self.upward_diagonals()
        yield from self.downward_diagonals()

class Matcher:

    def __init__(self, string):
        self.string = string
        self.state = self.string
        self.count = 0

    def accept(self, c):
        if self.state[0] == c:
            self.state = self.state[1:]
            if not self.state:
                self.count += 1
                self.state = self.string
        elif self.state != self.string:
            self.state = self.string
            if self.state[0] == c:
                self.state = self.state[1:]

def run_matchers(matchers, line):
    for c in line:
        for matcher in matchers:
            matcher.accept(c)
    return [matcher.count for matcher in matchers]

def day4a(grid):
    """
    >>> day4a(Grid(TEST_INPUT.splitlines()))
    18
    """
    cc = CrissCross(grid)

    def matchers():
        return (Matcher("XMAS"), Matcher("SAMX"))

    return sum(sum(run_matchers(matchers(), line)) for line in cc.all_lines())

def is_mas_cross(grid, pos):
    if grid[pos] == "A":
        (x, y) = pos
        match (grid[(x - 1, y - 1)], grid[(x + 1, y + 1)], grid[(x - 1, y + 1)], grid[(x + 1, y - 1)]):
            case ("M", "S", "M", "S"):
                return True
            case ("M", "S", "S", "M"):
                return True
            case ("S", "M", "M", "S"):
                return True
            case ("S", "M", "S", "M"):
                return True
            case _:
                return False
    return False

def day4b(grid):
    """
    >>> day4b(Grid(TEST_INPUT.splitlines()))
    9
    """
    count = 0
    for x in range(1, grid.width - 1):
        for y in range(1, grid.height - 1):
            if is_mas_cross(grid, (x, y)):
                count += 1

    return count

def main():
    grid = day_data(4).grid()
    print(f"Day 4a: {day4a(grid)}")
    print(f"Day 4b: {day4b(grid)}")


if __name__ == "__main__":
    main()

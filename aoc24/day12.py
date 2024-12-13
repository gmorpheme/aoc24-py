from aoc24 import Vec, day_data
from itertools import groupby, pairwise
from operator import xor

TEST_INPUT = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def parse(data_source):
    return day_data(data_source).grid()


class Region:
    def __init__(self, pos, character):
        self.members = {pos}
        self.perimeter = 4
        self.character = character

    def neighbours(self, pos):
        x, y = pos
        return {
            Vec(x, y - 1),
            Vec(x, y + 1),
            Vec(x - 1, y),
            Vec(x + 1, y),
        }

    def touches(self, pos):
        return bool(self.neighbours(pos) & self.members)

    def accept(self, pos):
        neighbours = self.neighbours(pos)
        match len(neighbours & self.members):
            case 0:
                return False
            case 1:
                self.perimeter += 2
            case 2:
                self.perimeter += 0
            case 3:
                self.perimeter -= 2
            case 4:
                self.perimeter -= 4
        self.members.add(pos)
        return True

    def merge(self, other, pos):
        self.members |= other.members
        self.perimeter += other.perimeter
        self.accept(pos)

def count_edges(s):

    min_y = min(s, key=lambda p: p.y).y
    max_y = max(s, key=lambda p: p.y).y

    min_x = min(s, key=lambda p: p.x).x
    max_x = max(s, key=lambda p: p.x).x

    horizontal_edges = 0
    for (ya, yb) in pairwise(range(min_y - 1, max_y + 2)):
        edges = groupby(range(min_x - 1, max_x + 1), lambda x: (Vec(x, ya) in s, Vec(x, yb) in s))
        edge_sigs = [e[0] for e in edges if xor(*e[0])]
        horizontal_edges += len(edge_sigs)

    vertical_edges = 0
    for (xa, xb) in pairwise(range(min_x - 1, max_x + 2)):
        edges = groupby(range(min_y - 1, max_y + 1), lambda y: (Vec(xa, y) in s, Vec(xb, y) in s))
        edge_sigs = [e[0] for e in edges if xor(*e[0])]
        vertical_edges += len(edge_sigs)

    return horizontal_edges + vertical_edges

def calculate_regions(grid):
    regions = []
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid[Vec(x, y)]
            rs = [r for r in regions if r.character == c and r.touches(Vec(x, y))]
            match len(rs):
                case 0:
                    regions.append(Region(Vec(x, y), grid[Vec(x, y)]))
                case 1:
                    rs[0].accept(Vec(x, y))
                case 2:
                    rs[0].merge(rs[1], Vec(x, y))
                    regions.remove(rs[1])

    return regions

def day12a(regions):
    """
    >>> day12a(calculate_regions(parse(TEST_INPUT)))
    1930
    """
    return sum(len(r.members) * r.perimeter for r in regions)

def day12b(regions):
    """
    >>> day12b(calculate_regions(parse(TEST_INPUT)))
    1206
    """
    return sum(count_edges(r.members) * len(r.members) for r in regions)


def main():
    regions = calculate_regions(parse(12))
    print(f"Day 12a: {day12a(regions)}")
    print(f"Day 12b: {day12b(regions)}")


if __name__ == "__main__":
    main()

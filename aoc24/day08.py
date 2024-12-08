from aoc24 import day_data, Pos
from collections import defaultdict
from itertools import combinations

TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def compute_antinodes(pos_a, pos_b):
    antinode_a = Pos(
        pos_b.x - 2 * (pos_b.x - pos_a.x), pos_b.y - 2 * (pos_b.y - pos_a.y)
    )
    antinode_b = Pos(
        pos_a.x + 2 * (pos_b.x - pos_a.x), pos_a.y + 2 * (pos_b.y - pos_a.y)
    )
    return set((antinode_a, antinode_b))


def compute_antinodes_b(pos_a, pos_b, grid):
    diff = Pos(pos_b.x - pos_a.x, pos_b.y - pos_a.y)
    ndiff = Pos(pos_a.x - pos_b.x, pos_a.y - pos_b.y)

    def priors():
        pos = pos_a
        while grid.bound(pos):
            yield pos
            pos = pos.offset(ndiff)

    def subsequents():
        pos = pos_b
        while grid.bound(pos):
            yield pos
            pos = pos.offset(diff)

    return set(priors()) | set(subsequents())


def parse_antennae(grid):
    antennae = defaultdict(set)
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid[(x, y)]
            if c != '.':
                antennae[c].add(Pos(x, y))

    return antennae


def day8a(grid):
    """
    >>> day8a(day_data(TEST_INPUT).grid())
    14
    """
    antennae = parse_antennae(grid)
    antinodes = set()
    for c in antennae.keys():
        for i, j in combinations(antennae[c], 2):
            antinodes |= compute_antinodes(i, j)

    return len([a for a in antinodes if grid.bound(a)])


def day8b(grid):
    """
    >>> day8b(day_data(TEST_INPUT).grid())
    34
    """
    antennae = parse_antennae(grid)
    antinodes = set()
    for c in antennae.keys():
        for i, j in combinations(antennae[c], 2):
            antinodes |= compute_antinodes_b(i, j, grid)

    return len(antinodes)


def main():
    grid = day_data(8).grid()
    print(f"Day 8a: {day8a(grid)}")
    print(f"Day 8b: {day8b(grid)}")


if __name__ == "__main__":
    main()

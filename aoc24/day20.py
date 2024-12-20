from aoc24 import day_data, Vec
from itertools import takewhile

TEST_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def parse(data_source):
    return day_data(data_source).grid()


CARDINALS = [Vec(0, 1), Vec(1, 0), Vec(0, -1), Vec(-1, 0)]


def find_path(grid):
    grid.dump()
    start = grid.find('S').pop()
    end = grid.find('E').pop()

    pos = start
    path = [start]
    while pos != end:
        for direction in CARDINALS:
            new_pos = pos + direction
            if new_pos not in path and grid[new_pos] != '#':
                path.append(new_pos)
                pos = new_pos
    return path


def day20a(grid):
    """
    >>> day20a(parse(TEST_INPUT))
    """
    path = find_path(grid)
    indices = {v: i for i, v in enumerate(path)}
    teleports = {c + d for c in CARDINALS for d in CARDINALS} - {Vec(0, 0)}
    cheats = {}

    for i, pos in enumerate(path):
        for v in teleports:
            if (r := indices.get(pos + v)) and r > i:
                cheats[(pos, pos + v)] = r - i - 2

    print(
        sum(
            1
            for c in takewhile(
                lambda x: x >= 100, sorted(cheats.values(), reverse=True)
            )
        )
    )


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def day20b(grid):
    """
    >>> day20b(parse(TEST_INPUT))
    """
    path = find_path(grid)

    def teleportable(a, b):
        return manhattan(a, b) <= 20

    cheats = {}

    for i, pos in enumerate(path):
        for skip, pos2 in enumerate(path[i + 1 :]):
            if teleportable(pos, pos2):
                cheats[(pos, pos2)] = skip - manhattan(pos, pos2) + 1

    return sum(
        1 for c in takewhile(lambda x: x >= 100, sorted(cheats.values(), reverse=True))
    )


def main():
    grid = parse(20)
    print(f"Day 20a: {day20a(grid)}")
    print(f"Day 20b: {day20b(grid)}")


if __name__ == "__main__":
    main()

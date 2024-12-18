from aoc24 import day_data, Vec
from collections import defaultdict

TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


class CycleException(Exception):
    def __init__(self, message):
        super().__init__(message)


def rotate(direction):
    c = complex(*direction) * 1j
    return (int(c.real), int(c.imag))


def compute_path(grid, pos, direction, obstacles):
    path = [pos]
    path_dict = defaultdict(set)
    while check := grid.bound(pos + direction):
        if check in obstacles:
            direction = rotate(direction)
        else:
            if check in path_dict[pos]:
                raise CycleException(f"Cycle detected at {pos} -> {check}")
            path_dict[pos].add(check)
            path.append(check)
            pos = check

    return path


def day6a(grid):
    """
    >>> day6a(day_data(TEST_INPUT).grid())
    41
    """
    return len(set(compute_path(grid, grid.find('^').pop(), (0, -1), grid.find('#'))))


def day6b(grid):
    """
    >>> day6b(day_data(TEST_INPUT).grid())
    6
    """
    obstacles = grid.find('#')
    start = grid.find('^').pop()
    path = compute_path(grid, start, (0, -1), obstacles)

    obstructions = set()
    for next in path[1:]:
        if next not in obstacles:
            try:
                compute_path(grid, start, (0, -1), obstacles | {next})
            except CycleException:
                obstructions.add(next)

    return len(obstructions)


def main():
    grid = day_data(6).grid()
    print(f"Day 6a: {day6a(grid)}")
    print(f"Day 6b: {day6b(grid)}")


if __name__ == "__main__":
    main()

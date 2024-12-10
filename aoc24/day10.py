from aoc24 import day_data
from collections import defaultdict

TEST_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def lower_neighbours(grid, pos):
    return [p for p in grid.neighbours(pos) if grid[pos] - grid[p] == 1]


def dfs_to_head(grid, pos):
    if grid[pos] == 0:
        yield pos
    else:
        for n in lower_neighbours(grid, pos):
            yield from dfs_to_head(grid, n)


def day10a(grid):
    """
    >>> day10a(day_data(TEST_INPUT).grid(int))
    36
    """
    heads = defaultdict(set)
    for t in grid.find(9):
        for head in dfs_to_head(grid, t):
            heads[t].add(head)
    return sum(len(s) for s in heads.values())


def day10b(grid):
    """
    >>> day10b(day_data(TEST_INPUT).grid(int))
    81
    """
    heads = defaultdict(list)
    for t in grid.find(9):
        for head in dfs_to_head(grid, t):
            heads[t].append(head)
    return sum(len(s) for s in heads.values())


def main():
    grid = day_data(10).grid(int)
    print(f"Day 10a: {day10a(grid)}")
    print(f"Day 10b: {day10b(grid)}")


if __name__ == "__main__":
    main()

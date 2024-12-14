from aoc24 import day_data, Vec
from functools import reduce
import operator

TEST_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


def parse(data_source):
    for x, y, vx, vy in day_data(data_source).tuples(
        r"p=(\-?[0-9]+),(\-?[0-9]+) v=(\-?[0-9]+),(\-?[0-9]+)", (int, int, int, int)
    ):
        yield Vec(x, y), Vec(vx, vy)


def dump(positions, bounds):
    for y in range(bounds.y):
        for x in range(bounds.x):
            if Vec(x, y) in positions:
                print("#", end="")
            else:
                print(".", end="")
        print()


def evolve(p, v, n, bounds):
    """
    >>> evolve(Vec(2, 4), Vec(2, -3), 1, Vec(11, 7))
    Vec(x=4, y=1)
    >>> evolve(Vec(2, 4), Vec(2, -3), 5, Vec(11, 7))
    Vec(x=1, y=3)
    """
    return (p + (v * n)) % bounds


def quadrant_counts(positions, bounds):
    tl = tr = bl = br = 0
    for p in positions:
        if p.x < bounds.x // 2:
            if p.y < bounds.y // 2:
                tl += 1
            elif p.y >= bounds.y // 2 + 1:
                bl += 1
        elif p.x >= bounds.x // 2 + 1:
            if p.y < bounds.y // 2:
                tr += 1
            elif p.y >= bounds.y // 2 + 1:
                br += 1
    return tl, tr, bl, br


def sociability(positions, bounds):
    sociabilities = []
    positions = set(positions)
    for p in positions:
        neighbours = {
            Vec(x, y) for x in range(p.x - 1, p.x + 2) for y in range(p.y - 1, p.y + 2)
        }
        sociabilities.append(len(neighbours & positions))
    return sum(sociabilities) / len(sociabilities)


def day14a(tuples, bounds):
    """
    >>> day14a(list(parse(TEST_INPUT)), Vec(11, 7))
    12
    """
    final_positions = [evolve(p, v, 100, bounds) for p, v in tuples]
    return reduce(operator.mul, quadrant_counts(final_positions, bounds))


def day14b(tuples, bounds):

    return max(
        range(bounds.x * bounds.y),
        key=lambda x: sociability((evolve(p, v, x, bounds) for p, v in tuples), bounds),
    )


def main():
    tuples = list(parse(14))
    bounds = Vec(101, 103)
    print(f"Day 14a: {day14a(tuples, bounds)}")
    print(f"Day 14b: {day14b(tuples, bounds)}")


if __name__ == "__main__":
    main()

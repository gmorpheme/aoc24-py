from aoc24 import day_data
import math
from functools import cache

TEST_INPUT = """125 17"""


def parse(data_source):
    return tuple(day_data(data_source).sequence(int))


def evolve(stone):
    """
    >>> evolve(0)
    (1,)
    >>> evolve(1)
    (2024,)
    >>> evolve(12)
    (1, 2)
    >>> evolve(125)
    (253000,)
    """

    if stone == 0:
        return (1,)
    string = str(stone)
    if len(string) % 2 == 0:
        return (int(string[0 : len(string) // 2]), int(string[len(string) // 2 :]))
    else:
        return (stone * 2024,)


@cache
def len_n(stone, n):
    if n == 0:
        return 1
    else:
        return sum(len_n(s, n - 1) for s in evolve(stone))


def day11a(stones):
    """
    >>> day11a(parse(TEST_INPUT))
    55312
    """
    return sum(len_n(s, 25) for s in stones)


def day11b(stones):
    return sum(len_n(s, 75) for s in stones)


def main():
    stones = parse(11)
    print(f"Day 11a: {day11a(stones)}")
    print(f"Day 11b: {day11b(stones)}")


if __name__ == "__main__":
    main()

import re
from collections import Counter
from aoc24 import day_data

TEST_DATA = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse(data_source):
    return zip(*day_data(data_source).tuples(r'(\d+)\s+(\d+)', (int, int)))


def difference(left, right):
    return abs(right - left)


def day1a(left, right):
    """
    >>> day1a(*parse(TEST_DATA))
    11
    """
    return sum(
        difference(left, right) for left, right in zip(sorted(left), sorted(right))
    )


def day1b(left, right):
    """
    >>> day1b(*parse(TEST_DATA))
    31
    """
    counter = Counter(right)
    return sum(value * counter.get(value, 0) for value in left)


def main():
    left, right = parse(1)
    print(f"Day 1a: {day1a(left, right)}")
    print(f"Day 1b: {day1b(left, right)}")


if __name__ == "__main__":
    main()

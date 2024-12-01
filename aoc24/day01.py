import re
from collections import Counter
from aoc24 import day_data

TEST_INPUT = ['3   4', '4   3', '2   5', '1   3', '3   9', '3   3']


def parse_line(line):
    regex = re.compile(r'(\d+)\s+(\d+)')
    return [int(g) for g in regex.match(line).groups()]


def difference(left, right):
    return abs(right - left)


def day1a(lines):
    """
    >>> day1a(TEST_INPUT)
    11
    """

    left, right = zip(*[parse_line(line) for line in lines])
    return sum(
        difference(left, right) for left, right in zip(sorted(left), sorted(right))
    )


def day1b(lines):
    """
    >>> day1b(TEST_INPUT)
    31
    """
    left, right = zip(*[parse_line(line) for line in lines])
    counter = Counter(right)
    return sum(value * counter.get(value, 0) for value in left)


def main():
    lines = day_data(1).lines()
    print(f"Day 1a: {day1a(lines)}")
    print(f"Day 1b: {day1b(lines)}")


if __name__ == "__main__":
    main()

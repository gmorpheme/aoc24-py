from itertools import pairwise
from aoc24 import day_data

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def parse_line(line):
    return [int(x) for x in line.split()]


def safe(levels):
    s = None
    for left, right in pairwise(levels):
        difference = right - left
        a = abs(difference)
        if a == 0:
            return False
        s2 = difference // a
        if a < 1 or a > 3 or (s and (s2 != s)):
            return False
        s = s2

    return True

def safe_with_dampening(levels):
    differences = [right - left for left, right in pairwise(levels)]
    unacceptable_if_increasing = [d < 1 or d > 3 for d in differences]
    unacceptable_if_decreasing = [d < -3 or d > -1 for d in differences]

    match (unacceptable_if_increasing.count(True), unacceptable_if_decreasing.count(True)):
        case (0, _):
            return True
        case (_, 0):
            return True
        case (a, b):
            # If there is an unacceptable difference (and possibly an
            # immediate correcting difference), can we remove either
            # the pre-value or post-value to make it acceptable?
            if a <= 2:
                bad_index = unacceptable_if_increasing.index(True)
                if safe(levels[:bad_index + 1] + levels[bad_index + 2:]):
                    return True
                if safe(levels[:bad_index] + levels[bad_index + 1:]):
                    return True
            if b <= 2:
                bad_index = unacceptable_if_decreasing.index(True)
                if safe(levels[:bad_index + 1] + levels[bad_index + 2:]):
                    return True
                if safe(levels[:bad_index] + levels[bad_index + 1:]):
                    return True
            return False

def day2a(records):
    """
    >>> day2a(parse_line(line) for line in day_data(TEST_INPUT).lines())
    2
    """
    return [safe(record) for record in records].count(True)

def day2b(records):
    """
    >>> day2b(parse_line(line) for line in day_data(TEST_INPUT).lines())
    4
    """
    return [safe_with_dampening(record) for record in records].count(True)

def main():
    records = [parse_line(line) for line in day_data(2).lines()]
    print(f"Day 2a: {day2a(records)}")
    print(f"Day 2b: {day2b(records)}")


if __name__ == "__main__":
    main()

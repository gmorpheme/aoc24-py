from aoc24 import day_data
import re
import operator
import math
from collections import deque

TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def parse_checks(data_source):
    return list(day_data(data_source).labelled_sequences(int, int, ":"))


def check_line(result, operands, operators=(operator.mul, operator.add)):

    operands = deque(operands)
    candidates = {operands.popleft()}

    while operands:
        next_operand = operands.popleft()
        candidates = set(
            n
            for op in operators
            for c in candidates
            if (n := op(c, next_operand)) <= result
        )

    return result in candidates


def concatenate(lhs, rhs):
    """
    >>> concatenate(1, 2)
    12
    >>> concatenate(12, 345)
    12345
    >>> concatenate(10, 10)
    1010
    >>> concatenate(10, 100)
    10100
    """
    return lhs * (10 ** math.floor(1 + math.log10(rhs))) + rhs


def day7a(checks):
    """
    >>> day7a(parse_checks(TEST_INPUT))
    3749
    """
    return sum(result for result, operands in checks if check_line(result, operands))


def day7b(checks):
    """
    >>> day7b(parse_checks(TEST_INPUT))
    11387
    """
    return sum(
        result
        for result, operands in checks
        if check_line(result, operands, (operator.mul, operator.add, concatenate))
    )


def main():
    checks = parse_checks(7)
    print(f"Day 7a: {day7a(checks)}")
    print(f"Day 7b: {day7b(checks)}")


if __name__ == "__main__":
    main()

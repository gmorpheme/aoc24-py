from aoc24 import day_data

TEST_INPUT = """ """


def parse(data_source):
    return day_data(data_source).lines()


def day14a(lines):
    """
    >>> day14a(parse(TEST_INPUT))
    """


def day14b(lines):
    """
    >>> day14b(parse(TEST_INPUT))
    """


def main():
    lines = parse(14)
    print(f"Day 14a: {day14a(lines)}")
    print(f"Day 14b: {day14b(lines)}")


if __name__ == "__main__":
    main()

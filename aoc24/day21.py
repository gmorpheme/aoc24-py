from aoc24 import day_data

TEST_INPUT = """ """


def parse(data_source):
    return day_data(data_source).lines()


def day21a(lines):
    """
    >>> day21a(parse(TEST_INPUT))
    """


def day21b(lines):
    """
    >>> day21b(parse(TEST_INPUT))
    """


def main():
    lines = parse(21)
    print(f"Day 21a: {day21a(lines)}")
    print(f"Day 21b: {day21b(lines)}")


if __name__ == "__main__":
    main()

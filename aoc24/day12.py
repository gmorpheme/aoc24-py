from aoc24 import day_data

TEST_INPUT = """ """


def parse(data_source):
    return day_data(data_source).lines()


def day12a(lines):
    """
    >>> day12a(parse(TEST_INPUT))
    """


def day12b(lines):
    """
    >>> day12b(parse(TEST_INPUT))
    """


def main():
    lines = parse(12)
    print(f"Day 12a: {day12a(lines)}")
    print(f"Day 12b: {day12b(lines)}")


if __name__ == "__main__":
    main()

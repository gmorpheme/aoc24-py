from functools import cache
from aoc24 import day_data

TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse(data_source):
    towels, designs = day_data(data_source).split()
    towels = frozenset(towels.sequence(lambda x: x.strip(), sep=', '))
    designs = [d.strip() for d in designs.lines()]
    return towels, designs


@cache
def routes(target, towels):
    if not target:
        return 1
    return sum(routes(target[len(t) :], towels) for t in towels if target.startswith(t))


def day19a(towels, designs):
    """
    >>> day19a(*parse(TEST_INPUT))
    6
    """
    return sum(1 for d in designs if routes(d, frozenset(towels)) > 0)


def day19b(towels, designs):
    """
    >>> day19b(['r', 'g', 'b', 'rb', 'gb', 'br'], ['rrbgbr'])
    6
    >>> day19b(['ab', 'bc', 'a', 'b', 'c'], ['abc'])
    3
    >>> day19b(['g', 'b', 'r', 'br', 'gb'], ['gbbr'])
    4
    >>> day19b(*parse(TEST_INPUT))
    16
    """
    return sum(routes(d, frozenset(towels)) for d in designs)


def main():
    towels, designs = parse(19)
    print(f"Day 19a: {day19a(towels, designs)}")
    print(f"Day 19b: {day19b(towels, designs)}")


if __name__ == "__main__":
    main()

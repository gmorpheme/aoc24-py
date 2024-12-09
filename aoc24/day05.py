from aoc24 import day_data
from collections import defaultdict
import re
from graphlib import TopologicalSorter

TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse(data_source):
    dep_data, manual_data = day_data(data_source).split()

    deps = defaultdict(set)
    for k, v in dep_data.tuples(r"(\d+)\|(\d+)", (int, int)):
        deps[v].add(k)

    manuals = []
    for seq in manual_data.sequences(int, sep=","):
        manuals.append(seq)

    return deps, manuals


def check_manual(deps, pages):
    relevant_pages = set(pages)
    met = set()
    for p in pages:
        required = deps[p] & relevant_pages
        if not required.issubset(met):
            return 0
        met.add(p)
    return pages[len(pages) // 2]


def corrected_middle(deps, pages):
    needed = set(pages)
    deps = {k: v & needed for k, v in deps.items() if k in needed}
    ts = TopologicalSorter(deps)
    corrected = list(ts.static_order())
    return corrected[len(corrected) // 2]


def day5a(deps, manuals):
    """
    >>> day5a(*parse(TEST_INPUT))
    143
    """
    return sum(check_manual(deps, m) for m in manuals)


def day5b(deps, manuals):
    """
    >>> day5b(*parse(TEST_INPUT))
    123
    """
    bad_manuals = [m for m in manuals if not (check_manual(deps, m))]
    return sum(corrected_middle(deps, m) for m in bad_manuals)


def main():
    deps, manuals = parse(5)
    print(f"Day 5a: {day5a(deps, manuals)}")
    print(f"Day 5b: {day5b(deps, manuals)}")


if __name__ == "__main__":
    main()

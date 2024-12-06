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

def parse(lines):
    iterator = iter(lines)
    line = next(iterator)

    deps = defaultdict(set)

    while m := re.match(r"(\d+)\|(\d+)", line.strip()):
        k, v = map(int, m.groups())
        deps[v].add(k)
        line = next(iterator)

    manuals = []
    for line in iterator:
        manuals.append(list(map(int, line.split(","))))

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

def day5a(lines):
    """
    >>> day5a(day_data(TEST_INPUT).lines())
    143
    """
    deps, manuals = parse(lines)
    return sum(check_manual(deps, m) for m in manuals)

def day5b(lines):
    """
    >>> day5b(day_data(TEST_INPUT).lines())
    123
    """
    deps, manuals = parse(lines)
    bad_manuals = [m for m in manuals if not(check_manual(deps, m))]
    return sum(corrected_middle(deps, m) for m in bad_manuals)

def main():
    lines = day_data(5).lines()
    print(f"Day 5a: {day5a(lines)}")
    print(f"Day 5b: {day5b(lines)}")

if __name__ == "__main__":
    main()

from aoc24 import day_data
import re

TEST_INPUT = r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


def day3a(text):
    """
    >>> day3a(TEST_INPUT)
    161
    """
    mul_regex = re.compile(r'mul\((\d+),(\d+)\)')
    return sum(int(l) * int(r) for l, r in mul_regex.findall(text))


TEST_INPUT_B = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def day3b(text):
    """
    >>> day3b(TEST_INPUT_B)
    48
    """

    inst_regex = re.compile(r'(do\(\))|(don\'t\(\))|(mul\((\d+),(\d+)\))')
    total = 0
    on = True
    for m in inst_regex.finditer(text):
        match m.groups():
            case (None, None, _, l, r):
                if on:
                    total += int(l) * int(r)
            case ('do()', _, _, _, _):
                on = True
            case (_, 'don\'t()', _, _, _):
                on = False
    return total


def main():
    text = day_data(3).text()
    print(f"Day 3a: {day3a(text)}")
    print(f"Day 3b: {day3b(text)}")


if __name__ == "__main__":
    main()

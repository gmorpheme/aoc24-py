from aoc24 import day_data, Vec
from dataclasses import dataclass
from fractions import Fraction
import re

TEST_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

PUZZLE_RE = re.compile(
    r"""Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)""",
    re.MULTILINE,
)

TENTRILLION = 10000000000000


@dataclass
class Matrix:

    col_a: Vec
    col_b: Vec

    @property
    def row_a(self):
        return Vec(self.col_a.x, self.col_b.x)

    @property
    def row_b(self):
        return Vec(self.col_a.y, self.col_b.y)

    def determinant(self):
        """
        >>> Matrix(Vec(94,34),Vec(22,67)).determinant()
        5550
        """
        return self.row_a.x * self.row_b.y - self.row_a.y * self.row_b.x

    def inverse(self):
        """
        >>> m = Matrix(Vec(94,34),Vec(22,67))
        >>> i = m.inverse()
        >>> m * i
        Matrix(col_a=Vec(x=Fraction(1, 1), y=Fraction(0, 1)), col_b=Vec(x=Fraction(0, 1), y=Fraction(1, 1)))
        """
        det = self.determinant()
        return Matrix(
            Vec(self.col_b.y, -self.col_a.y) / det,
            Vec(-self.col_b.x, self.col_a.x) / det,
        )

    def __mul__(self, other):
        """
        >>> m = Matrix(Vec(94,34),Vec(22,67))
        >>> i = m.inverse()
        >>> i * Vec(8400,5400)
        Vec(x=Fraction(80, 1), y=Fraction(40, 1))
        """
        if isinstance(other, tuple):
            return Vec(self.row_a.dot(other), self.row_b.dot(other))
        elif isinstance(other, Matrix):
            return Matrix(
                Vec(self.row_a.dot(other.col_a), self.row_a.dot(other.col_b)),
                Vec(self.row_b.dot(other.col_a), self.row_b.dot(other.col_b)),
            )


@dataclass
class ClawMachine:
    button_a: Vec
    button_b: Vec
    prize: Vec

    def perturb_prize(self, dx, dy):
        return ClawMachine(
            self.button_a, self.button_b, Vec(self.prize.x + dx, self.prize.y + dy)
        )

    def solve(self):
        """
        >>> ClawMachine(Vec(94,34),Vec(22,67),Vec(8400,5400)).solve()
        Vec(x=80, y=40)
        >>> ClawMachine(Vec(26,66),Vec(67,21),Vec(TENTRILLION+12748,TENTRILLION+12176)).solve()
        Vec(x=118679050709, y=103199174542)
        """
        matrix = Matrix(self.button_a, self.button_b)

        if matrix.determinant():
            # The matrix is invertible
            inverse = matrix.inverse()
            solution = inverse * self.prize
            if solution.x.is_integer() and solution.y.is_integer():
                return Vec(int(solution.x), int(solution.y))
        else:
            # Degenerate solution so col vectors are linearly
            # dependent
            factor = self.button_b.x / self.button_a.x

            if factor > Fraction(1, 3):
                # button_b is more than 1/3 of button_a so it's more
                # economical if it divides cleanly
                presses = self.prize.x / self.button_b.x
                if presses.is_integer():
                    return Vec(0, presses)

            presses = self.prize.x / self.button_b.x
            if presses.is_integer():
                return Vec(presses, 0)


def parse(data_source):
    text = day_data(data_source).text()
    for ax, ay, bx, by, px, py in PUZZLE_RE.findall(text):
        yield ClawMachine(
            Vec(int(ax), int(ay)),
            Vec(int(bx), int(by)),
            Vec(int(px), int(py)),
        )


def day13a(machines):
    """
    >>> day13a(parse(TEST_INPUT))
    480
    """
    return sum(s.x * 3 + s.y for machine in machines if (s := machine.solve()))


def day13b(machines):

    machines = [m.perturb_prize(TENTRILLION, TENTRILLION) for m in machines]
    return sum(s.x * 3 + s.y for machine in machines if (s := machine.solve()))


def main():
    machines = list(parse(13))
    print(f"Day 13a: {day13a(machines)}")
    print(f"Day 13b: {day13b(machines)}")


if __name__ == "__main__":
    main()

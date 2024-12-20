import importlib
import pathlib
import datetime
import re
from dataclasses import dataclass
from typing import NamedTuple, Iterator
from functools import cached_property
from itertools import takewhile
from fractions import Fraction

def day(n):
    title = f'Day {n}'
    print(title + ' ' + '-' * (80 - len(title) - 1))
    start = datetime.datetime.now()
    try:
        module = importlib.import_module(f'aoc24.day{n:02}')
        module.main()
    except Exception as e:
        print(e)
    finally:
        end = datetime.datetime.now()
        summary = f'Elapsed: {end - start}'
        print('-' * (80 - len(summary) - 1) + ' ' + summary + '\n')


def debug(n):
    import pdb

    module = importlib.import_module(f'aoc24.day{n:02}')
    pdb.runcall(module.main)


def latest_day():
    for n in range(25, 0, -1):
        if pathlib.Path(f'aoc24/day{n:02}.py').exists():
            return day(n)


def all_days():
    print('All days')
    for n in range(26):
        if pathlib.Path(f'aoc24/day{n:02}.py').exists():
            day(n)

class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vec(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Vec(self.x - other[0], self.y - other[1])

    def __truediv__(self, scalar):
        return Vec(Fraction(self.x, scalar), Fraction(self.y, scalar))

    def __mod__(self, other):
        return Vec(self.x % other[0], self.y % other[1])

    def __mul__(self, scalar):
        return Vec(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def offset(self, direction):
        return Vec(self.x + direction[0], self.y + direction[1])

class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, scalar):
        return Vec3(Fraction(self.x, scalar), Fraction(self.y, scalar), Fraction(self.z, scalar))

    def __mod__(self, other):
        return Vec3(self.x % other.x, self.y % other.y, self.z % other.z)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def offset(self, direction):
        return Vec3(self.x + direction.x, self.y + direction.y, self.z + direction.z)

class Grid:

    """
    A simple grid represented as rows, starting with y=0.
    """

    def __init__(self, rows):
        self.rows = rows

    def __getitem__(self, locator):
        match locator:
            case (x, y):
                return self.rows[y][x]

    def __setitem__(self, locator, value):
        match locator:
            case (x, y):
                self.rows[y][x] = value


    def bound(self, pos):
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return pos

    def neighbours(self, pos):
        for d in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            if n := self.bound(pos +  d):
                yield n

    def find(self, item):
        return {Vec(x, y) for y in range(self.height) for x in range(self.width) if self[(x, y)] == item}

    def dump(self):
        for row in self.rows:
            print(''.join(row))
        print()

    @cached_property
    def height(self):
        return len(self.rows)

    @cached_property
    def width(self):
        return len(self.rows[0])

class DayData:

    def __init__(self, line_iter):
        self.line_iter = line_iter

    def dicts(self, regex):
        r = re.compile(regex)
        return [r.match(line).groupdict() for line in self.lines()]

    def tuples(self, regex, xforms):
        return [tuple(map(lambda f, x: f(x), xforms, re.match(regex, line).groups())) for line in self.lines()]

    def sequence(self, xform = None, sep = None):
        if sep:
            if xform:
                return list(map(xform, self.text().split(sep)))
            else:
                return list(self.text().split(sep))
        else:
            if xform:
                return [xform(x) for x in self.text().split()]
            else:
                return self.text().split()

    def sequences(self, xform, sep = None):
        if sep:
            return [list(map(xform, line.split(sep))) for line in self.lines()]
        else:
            return [[xform(x) for x in line.split()] for line in self.lines()]

    def labelled_sequences(self, label_xform, item_xform, sep = None, seq_sep = None):
        for line in self.lines():
            head, tail = line.split(sep)
            items = tail.split(seq_sep)
            yield label_xform(head), [item_xform(x) for x in items]

    def grid(self, item_transform = lambda x: x):
        return Grid([list(item_transform(c) for c in line.strip()) for line in self.lines()])

    def split(self):
        after = iter(self.lines())
        before = takewhile(lambda x: x.strip(), after)
        return LinesData(before), LinesData(after)

@dataclass
class TestData(DayData):
    text_data: str

    def lines(self):
        return self.text_data.splitlines()

    def text(self):
        return self.text_data.strip()

@dataclass
class LinesData(DayData):

    lineiter: Iterator[str]

    def lines(self):
        yield from self.lineiter

    def text(self):
        return "".join(self.lineiter).strip()

@dataclass
class DayTextFileInput(DayData):
    day: int

    def filename(self):
        return f"aoc24/data/day{self.day:02}input.txt"

    def lines(self):
        return list(open(self.filename()))

    def file(self):
        return open(self.filename())

    def text(self):
        return self.file().read().strip()

def day_data(n):
    if type(n) is str:
        return TestData(n)
    else:
        return DayTextFileInput(n)

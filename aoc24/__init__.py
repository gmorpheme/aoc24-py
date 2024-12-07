import importlib
import pathlib
import datetime
import re
from dataclasses import dataclass
from typing import NamedTuple
from functools import cached_property

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
    for n in range(0, 26):
        try:
            module = importlib.import_module(f'aoc24.day{n:02}')
        except Exception:
            pass
        else:
            module.main()

class Pos(NamedTuple):
    x: int
    y: int

    def offset(self, direction):
        return Pos(self.x + direction[0], self.y + direction[1])

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

    def find(self, item):
        return {Pos(x, y) for y in range(self.height) for x in range(self.width) if self[(x, y)] == item}

    @cached_property
    def height(self):
        return len(self.rows)

    @cached_property
    def width(self):
        return len(self.rows[0])

@dataclass
class TestData:
    text_data: str

    def lines(self):
        return self.text_data.splitlines()

    def dicts(self, regex):
        r = re.compile(regex)
        return [r.match(line).groupdict() for line in self.lines()]

    def tuples(self, regex):
        r = re.compile(regex)
        return [tuple(r.match(line).groups()) for line in self.lines()]

    def text(self):
        return self.text_data

    def grid(self, item_transform = lambda x: x):
        return Grid([list(item_transform(c) for c in line.strip()) for line in self.lines()])

@dataclass
class DayData:
    day: int

    def filename(self):
        return f"aoc24/data/day{self.day:02}input.txt"

    def lines(self):
        return list(open(self.filename()))

    def dicts(self, regex):
        r = re.compile(regex)
        return [r.match(line).groupdict() for line in open(self.filename())]

    def tuples(self, regex):
        r = re.compile(regex)
        return [tuple(r.match(line).groups()) for line in open(self.filename())]

    def file(self):
        return open(self.filename())

    def text(self):
        return self.file().read()

    def grid(self, item_transform = lambda x: x):
        return Grid([list(item_transform(c) for c in line.strip()) for line in self.lines()])

def day_data(n):
    if type(n) is str:
        return TestData(n)
    else:
        return DayData(n)

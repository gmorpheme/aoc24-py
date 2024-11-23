import argparse
from aoc24 import day, debug, all_days

parser = argparse.ArgumentParser(prog='aoc', description='Run advent of code programs')
parser.add_argument('day', metavar='N', type=int, nargs='?', help='day to run')
parser.add_argument('--debug', action='store_true', help='debug')

if __name__ == '__main__':
    print('Advent of Code 2024')
    opts = parser.parse_args()
    if n := opts.day:
        if opts.debug:
            debug(n)
        else:
            day(n)
    else:
        all_days()

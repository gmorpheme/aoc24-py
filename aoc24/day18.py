from aoc24 import day_data, Vec, Vec3
from dataclasses import dataclass
from heapq import heappop, heappush

TEST_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


class SparseGrid:
    def __init__(self, seqs, bounds):
        self.arrivals = {Vec(x, y): t + 1 for t, (x, y) in enumerate(seqs)}
        self.bounds = bounds

    def __getitem__(self, v3):
        (x, y, t) = v3
        if not (0 <= x <= self.bounds.x and 0 <= y <= self.bounds.y):
            return True
        t_from = self.arrivals.get(Vec(x, y))
        if t_from is not None:
            return t >= t_from
        else:
            return False

    def arrival(self, t):
        return next(k for k, v in self.arrivals.items() if v == t)


@dataclass
class Challenge:
    """I expected these implementations to change for part 2. I
    generalised prematurely again."""

    start: Vec
    end: Vec
    instant: int

    def heuristic(self, v3):
        return abs(v3[0] - self.end[0]) + abs(v3[1] - self.end[1])

    def options(self, v3):
        (x, y, _) = v3
        return [
            Vec3(x + dx, y + dy, self.instant)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if 0 <= x + dx <= self.end.x and 0 <= y + dy <= self.end.y
        ]

    def initial_state(self):
        return Vec3(self.start.x, self.start.y, self.instant)

    def done(self, v3):
        return v3[:2] == self.end


def a_star(grid, challenge):
    start = challenge.initial_state()
    frontier = [(challenge.heuristic(start), [start])]

    best_costs = {}

    def expand_frontier(path):
        best = best_costs.get(path[-1], float("inf"))
        cost = len(path) - 1 + challenge.heuristic(path[-1])
        if cost < best:
            best_costs[path[-1]] = cost
            heappush(frontier, (cost, path))

    while frontier:
        _, path = heappop(frontier)
        if challenge.done(path[-1]):
            return path
        for option in challenge.options(path[-1]):
            if not grid[option]:
                new_path = path + [option]
                expand_frontier(new_path)


def parse(data_source):
    return day_data(data_source).sequences(int, ',')


def day18a(grid, challenge):
    """
    >>> challenge = Challenge(Vec(0, 0), Vec(6, 6), 12)
    >>> day18a(SparseGrid(parse(TEST_INPUT), Vec(6, 6)), challenge)
    22
    """
    path = a_star(grid, challenge)
    return len(path) - 1


def day18b(grid, challenge):
    """
    >>> challenge = Challenge(Vec(0, 0), Vec(6, 6), 12)
    >>> day18b(SparseGrid(parse(TEST_INPUT), Vec(6, 6)), challenge)
    Vec(x=6, y=1)
    """
    min_t, max_t = 0, len(grid.arrivals)
    while min_t < (max_t - 1):
        mid_t = (min_t + max_t) // 2
        challenge.instant = mid_t
        path = a_star(grid, challenge)
        if path:
            min_t = mid_t
        else:
            max_t = mid_t

    return grid.arrival(max_t)


def main():
    grid = SparseGrid(parse(18), Vec(70, 70))
    challenge = Challenge(Vec(0, 0), Vec(70, 70), 1024)
    print(f"Day 18a: {day18a(grid, challenge)}")
    print(f"Day 18b: {day18b(grid, challenge)}")


if __name__ == "__main__":
    main()

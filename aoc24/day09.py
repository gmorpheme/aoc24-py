from aoc24 import day_data
from collections import deque

TEST_INPUT = "2333133121414131402"


def parse_disk(text):

    disk = []
    file = True
    for i, c in enumerate(text):
        if file:
            disk.append((int(c), i // 2))
            file = False
        else:
            disk.append((int(c), None))
            file = True

    return disk


def compress(disk):
    while True:
        (n, id) = disk.pop()
        if n == 0 or id is None:
            continue
        try:
            target_index = next(i for (i, (k, v)) in enumerate(disk) if v is None)
            target_space = disk[target_index][0]
            moved_files = min(target_space, n)
            excess_space = target_space - moved_files
            excess_files = n - moved_files
            if excess_space:
                disk[target_index] = (excess_space, None)
                disk.insert(target_index, (moved_files, id))
            else:
                disk[target_index] = (moved_files, id)
            if moved_files < n:
                disk.append((excess_files, id))

        except StopIteration:
            disk.append((n, id))
            break

    return disk


def defragment(disk):
    head = disk
    tail = deque()

    while head:
        (n, id) = head.pop()
        if n == 0:
            continue
        if id is None:
            tail.appendleft((n, id))
            continue
        try:
            target_index = next(
                i for (i, (k, v)) in enumerate(head) if v is None and k >= n
            )
            target_space = head[target_index][0]
            excess_space = target_space - n
            if excess_space:
                head[target_index] = (excess_space, None)
                head.insert(target_index, (n, id))
            else:
                head[target_index] = (n, id)
            tail.appendleft((n, None))

        except StopIteration:
            tail.appendleft((n, id))

    return tail


def blocks(disk):
    for n, id in disk:
        yield from [id] * n


def checksum(disk):
    return sum(i * (n or 0) for i, n in enumerate(blocks(disk)))


def day9a(text):
    """
    >>> day9a(day_data(TEST_INPUT).text())
    1928
    """
    return checksum(compress(parse_disk(text)))


def day9b(text):
    """
    >>> day9b(day_data(TEST_INPUT).text())
    2858
    """
    return checksum(defragment(parse_disk(text)))


def main():
    text = day_data(9).text()
    print(f"Day 9a: {day9a(text)}")
    print(f"Day 9b: {day9b(text)}")


if __name__ == "__main__":
    main()

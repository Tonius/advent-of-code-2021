from collections import defaultdict
from heapq import heappop, heappush


grid: dict[tuple[int, int], int] = {}

with open("15-input.txt") as input_file:
    for y, line in enumerate(input_file.read().splitlines()):
        for x, risk_level in enumerate(line):
            grid[(x, y)] = int(risk_level)


def get_lowest_total_risk_level(grid: dict[tuple[int, int], int]):
    start = (0, 0)
    end = max(grid.keys(), key=lambda coords: coords[0] + coords[1])

    def get_adjacent(x: int, y: int) -> list[tuple[int, int]]:
        return [
            coords
            for coords in [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]
            if start[0] <= coords[0] <= end[0] and start[1] <= coords[1] <= end[1]
        ]

    total_risk_levels = defaultdict(lambda: None, {start: 0})
    lowest_heap = []
    visited = set()
    current = start

    while True:
        for adjacent in get_adjacent(*current):
            current_risk_level = total_risk_levels[adjacent]
            new_risk_level = total_risk_levels[current] + grid[adjacent]

            if current_risk_level is None or new_risk_level < current_risk_level:
                total_risk_levels[adjacent] = new_risk_level
                heappush(lowest_heap, (new_risk_level, adjacent))

        if current == end:
            break

        visited.add(current)

        current = heappop(lowest_heap)[1]

    return total_risk_levels[end]


print("\npart 1")
print(f"Lowest total risk level: {get_lowest_total_risk_level(grid)}")


print("\npart 2")
grid_size_x = max(x for x, _ in grid) + 1
grid_size_y = max(y for _, y in grid) + 1


def increase_risk_level(risk_level: int, offset: int):
    risk_level += offset
    while risk_level > 9:
        risk_level -= 9

    return risk_level


bigger_grid = grid.copy()

for (x, y), risk_level in grid.items():
    for x_offset in range(0, 5):
        for y_offset in range(0, 5):
            bigger_grid[
                (
                    x + x_offset * grid_size_x,
                    y + y_offset * grid_size_y,
                )
            ] = increase_risk_level(risk_level, x_offset + y_offset)

print(f"Lowest total risk level: {get_lowest_total_risk_level(bigger_grid)}")

from collections import defaultdict
from math import ceil


risk_levels: dict[tuple[int, int], int] = {}

with open("15-input.txt") as input_file:
    for y, line in enumerate(input_file.read().splitlines()):
        for x, risk_level in enumerate(line):
            risk_levels[(x, y)] = int(risk_level)


def get_lowest_total_risk_level(risk_levels: dict[tuple[int, int], int]):
    start = (0, 0)
    end = max(risk_levels.keys(), key=lambda coords: coords[0] + coords[1])

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
    visited = set()
    current = start

    node_count = len(risk_levels)
    printerval = ceil(node_count / 100)

    while True:
        for adjacent in get_adjacent(*current):
            current_risk_level = total_risk_levels[adjacent]
            new_risk_level = total_risk_levels[current] + risk_levels[adjacent]

            if current_risk_level is None or new_risk_level < current_risk_level:
                total_risk_levels[adjacent] = new_risk_level

        if current == end:
            break

        visited.add(current)

        if len(visited) % printerval == 0:
            print(f"visited {len(visited)} of {len(risk_levels)}")

        lowest_value = None
        for (x, y), value in total_risk_levels.items():
            if (
                value is not None
                and (x, y) not in visited
                and (lowest_value is None or value < lowest_value)
            ):
                lowest_value = value
                current = (x, y)

    return total_risk_levels[end]


print("\npart 1")
print(f"Lowest total risk level: {get_lowest_total_risk_level(risk_levels)}")


print("\npart 2")
grid_size_x = max(x for x, _ in risk_levels) + 1
grid_size_y = max(y for _, y in risk_levels) + 1


def increase_risk_level(risk_level: int, offset: int):
    risk_level += offset
    while risk_level > 9:
        risk_level -= 9

    return risk_level


new_risk_levels = risk_levels.copy()

for x_offset in range(1, 5):
    for (x, y), risk_level in risk_levels.items():
        new_risk_levels[(x + x_offset * grid_size_x, y)] = increase_risk_level(
            risk_level, x_offset
        )

risk_levels = new_risk_levels

new_risk_levels = risk_levels.copy()

for y_offset in range(1, 5):
    for (x, y), risk_level in risk_levels.items():
        new_risk_levels[(x, y + y_offset * grid_size_y)] = increase_risk_level(
            risk_level, y_offset
        )

risk_levels = new_risk_levels

print(f"Lowest total risk level: {get_lowest_total_risk_level(risk_levels)}")

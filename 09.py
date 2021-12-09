from functools import reduce
from operator import mul
from typing import Optional


class Heightmap:
    def __init__(self, data: str):
        self.points: dict[int, dict[int, int]] = {}

        for x, line in enumerate(data.splitlines()):
            for y, height in enumerate(line):
                self.add_point(x, y, int(height))

        self.max_x = max(self.points)
        self.max_y = max(self.points[0])

    def add_point(self, x: int, y: int, height: int):
        if x not in self.points:
            self.points[x] = {}

        self.points[x][y] = height

    def get_height_at(self, x: int, y: int) -> Optional[int]:
        if x < 0 or x > self.max_x or y < 0 or y > self.max_y:
            return None

        return self.points[x][y]

    def get_adjacent_heights(self, x: int, y: int) -> list[int]:
        return [
            height
            for height in [
                self.get_height_at(x - 1, y),
                self.get_height_at(x + 1, y),
                self.get_height_at(x, y - 1),
                self.get_height_at(x, y + 1),
            ]
            if height is not None
        ]

    def get_low_points(self) -> list[tuple[int, int]]:
        low_points = []

        for x, row in self.points.items():
            for y, height in row.items():
                if all(
                    height < adjacent_height
                    for adjacent_height in self.get_adjacent_heights(x, y)
                ):
                    low_points.append((x, y))

        return low_points

    def get_basin_size(self, start_x: int, start_y: int):
        basin_points = []

        check_points = [(start_x, start_y)]

        while len(check_points) > 0:
            check_point = check_points.pop(0)

            if check_point not in basin_points:
                height = self.get_height_at(*check_point)

                if height is not None and height < 9:
                    basin_points.append(check_point)

                    check_points.extend(
                        [
                            (check_point[0] - 1, check_point[1]),
                            (check_point[0] + 1, check_point[1]),
                            (check_point[0], check_point[1] - 1),
                            (check_point[0], check_point[1] + 1),
                        ]
                    )

        return len(basin_points)


with open("09-input.txt") as input_file:
    heightmap = Heightmap(input_file.read())


print("\npart 1")

low_points = heightmap.get_low_points()

low_point_risk_level_sum = sum(heightmap.get_height_at(x, y) + 1 for x, y in low_points)

print(f"Sum of the risk levels of all low points: {low_point_risk_level_sum}")


print("\npart 2")

three_largest_basin_sizes = sorted(
    [heightmap.get_basin_size(x, y) for x, y in low_points]
)[-3:]

print(f"Sizes of the three largest basins: {three_largest_basin_sizes}")
print(f"Result: {reduce(mul, three_largest_basin_sizes)}")

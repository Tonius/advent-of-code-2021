from dataclasses import dataclass
from typing import Iterable


@dataclass
class Coords:
    x: int
    y: int

    @classmethod
    def from_string(cls, value: str):
        x, y = value.split(",")

        return cls(x=int(x), y=int(y))


@dataclass
class Line:
    from_coords: Coords
    to_coords: Coords

    @classmethod
    def from_string(cls, value: str):
        from_coords, to_coords = value.split(" -> ")

        return cls(
            from_coords=Coords.from_string(from_coords),
            to_coords=Coords.from_string(to_coords),
        )

    def _get_range(self, from_: int, to: int, length: int) -> Iterable[int]:
        if to > from_:
            return range(from_, to + 1)
        elif to < from_:
            return range(from_, to - 1, -1)

        return [from_ for _ in range(length)]

    def get_covered_coords(self) -> Iterable[tuple[int, int]]:
        length = (
            max(
                abs(self.from_coords.x - self.to_coords.x),
                abs(self.from_coords.y - self.to_coords.y),
            )
            + 1
        )

        for x, y in zip(
            self._get_range(line.from_coords.x, line.to_coords.x, length),
            self._get_range(line.from_coords.y, line.to_coords.y, length),
        ):
            yield x, y


class Points:
    def __init__(self):
        self.points: dict[int, dict[int, int]] = {}

    def increment(self, x: int, y: int):
        if x not in self.points:
            self.points[x] = {}

        if y not in self.points[x]:
            self.points[x][y] = 0

        self.points[x][y] += 1

    def get_points_with_at_least_two_lines_count(self) -> int:
        result = 0

        for row in self.points.values():
            for count in row.values():
                if count >= 2:
                    result += 1

        return result


with open("05-input.txt") as input_file:
    lines = [Line.from_string(line) for line in input_file]


print("\npart 1")

points = Points()

for line in lines:
    if line.from_coords.x == line.to_coords.x or line.from_coords.y == line.to_coords.y:
        for x, y in line.get_covered_coords():
            points.increment(x, y)

print(
    f"Points with at least 2 lines: {points.get_points_with_at_least_two_lines_count()}"
)


print("\npart 2")

points = Points()

for line in lines:
    for x, y in line.get_covered_coords():
        points.increment(x, y)

print(
    f"Points with at least 2 lines: {points.get_points_with_at_least_two_lines_count()}"
)

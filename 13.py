from typing import Literal


with open("13-input.txt") as input_file:
    dot_lines, fold_lines = input_file.read().strip().split("\n\n")

dots: set[tuple[int, int]] = set()

for dot_line in dot_lines.split("\n"):
    dots.add((int(coord) for coord in dot_line.split(",")))

folds: list[tuple[str, int]] = []

for fold_line in fold_lines.split("\n"):
    axis, value = fold_line.removeprefix("fold along ").split("=")
    folds.append((axis, int(value)))


print("\npart 1")


def do_fold(dots: set[tuple[int, int]], axis: Literal["x", "y"], value: int):
    new_dots: set[tuple[int, int]] = set()

    for x, y in dots:
        if axis == "x" and x > value:
            x = value - (x - value)
        elif axis == "y" and y > value:
            y = value - (y - value)

        new_dots.add((x, y))

    return new_dots


for i, (axis, value) in enumerate(folds):
    dots = do_fold(dots, axis, value)

    if i == 0:
        print(f"Number of dots after first fold: {len(dots)}")


print("\npart 2")

max_x = max(x for x, _ in dots)
max_y = max(y for y, _ in dots)

lines = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]

for x, y in dots:
    lines[y][x] = "#"

for i, chars in enumerate(lines):
    if all(all(char == "." for char in line) for line in lines[i:]):
        break

    print("".join(chars))

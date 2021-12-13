from collections import Counter
from dataclasses import dataclass
from typing import Callable, Optional


START = "start"
END = "end"


@dataclass
class Cave:
    name: str
    connected_caves: list["Cave"]

    def is_big(self) -> bool:
        return self.name.isupper()

    def find_paths_to(
        self,
        to_cave_name: str,
        can_pass_through_cave: Callable[["Cave", list[str]], bool],
        current_path: Optional[list[str]] = None,
    ):
        if current_path is None:
            current_path = []

        current_path = [*current_path, self.name]

        if self.name == to_cave_name:
            return [current_path]

        paths = []

        for cave in self.connected_caves:
            if can_pass_through_cave(cave, current_path):
                paths.extend(
                    cave.find_paths_to(
                        to_cave_name, can_pass_through_cave, current_path
                    )
                )

        return paths


caves: list[Cave] = []


def find_cave(name: str):
    for cave in caves:
        if cave.name == name:
            return cave

    return None


def find_or_make_cave(name: str):
    cave = find_cave(name)
    if cave is None:
        cave = Cave(name, [])
        caves.append(cave)

    return cave


with open("12-input.txt") as input_file:
    for line in input_file.read().splitlines():
        first_cave, second_cave = (find_or_make_cave(name) for name in line.split("-"))
        first_cave.connected_caves.append(second_cave)
        second_cave.connected_caves.append(first_cave)


print("\npart 1")


def can_pass_through_cave_one(cave: Cave, current_path: list[str]):
    return cave.is_big() or cave.name not in current_path


paths = find_cave(START).find_paths_to(END, can_pass_through_cave_one)

print(f"Number of paths: {len(paths)}")


print("\npart 2")


def can_pass_through_cave_two(cave: Cave, current_path: list[str]):
    if cave.name == START:
        return False

    if can_pass_through_cave_one(cave, current_path):
        return True

    return max(Counter([c for c in current_path[1:] if c.islower()]).values()) == 1


paths = find_cave(START).find_paths_to(END, can_pass_through_cave_two)

print(f"Number of paths: {len(paths)}")

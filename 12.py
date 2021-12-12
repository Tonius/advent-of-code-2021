from dataclasses import dataclass
from typing import Optional


@dataclass
class Cave:
    name: str
    connected_caves: list["Cave"]

    def is_big(self) -> bool:
        return self.name.isupper()

    def traverse(self, traversed_small_caves: Optional[list["Cave"]] = None):
        if traversed_small_caves is None:
            traversed_small_caves = []

        if not self.is_big():
            traversed_small_caves.append(self)

        print(self.name)

        if self.name == "end":
            return

        for cave in self.connected_caves:
            if cave.is_big() or cave not in traversed_small_caves:
                cave.traverse(traversed_small_caves)


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

find_cave("start").traverse()

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cave:
    name: str
    connected_caves: list["Cave"]

    def is_big(self) -> bool:
        return self.name.isupper()

    def traverse(self, traversed_caves: Optional[list["Cave"]] = None):
        if traversed_caves is None:
            traversed_caves = []

        traversed_caves.append(self)

        if self.name == "end":
            exit()

        for cave in self.connected_caves:
            if cave.is_big() or cave not in traversed_caves:
                print(f"{self.name} -> {cave.name}")

                cave.traverse(traversed_caves)


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

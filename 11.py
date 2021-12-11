from dataclasses import dataclass
from typing import Optional


@dataclass
class Octopus:
    x: int
    y: int
    energy_level: int
    flashed: bool

    def increase_energy_level(self, octopuses: list["Octopus"]):
        self.energy_level += 1

        if self.energy_level > 9 and not self.flashed:
            self.flashed = True

            for x in range(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    octopus = find_octopus(octopuses, x, y)
                    if octopus is not None and octopus is not self:
                        octopus.increase_energy_level(octopuses)


def find_octopus(octopuses: list[Octopus], x: int, y: int) -> Optional[Octopus]:
    for octopus in octopuses:
        if octopus.x == x and octopus.y == y:
            return octopus

    return None


octopuses: list[Octopus] = []

with open("11-input.txt") as input_file:
    for y, row in enumerate(input_file.read().splitlines()):
        for x, energy_level in enumerate(row):
            octopuses.append(Octopus(x, y, int(energy_level), flashed=False))

flashes = 0
step = 0

while True:
    step += 1

    for octopus in octopuses:
        octopus.increase_energy_level(octopuses)

    if all(octopus.flashed for octopus in octopuses):
        print(f"First step during which all octopuses flash: {step}")
        exit()

    for octopus in octopuses:
        if octopus.flashed:
            flashes += 1
            octopus.energy_level = 0
            octopus.flashed = False

    if step == 100:
        print(f"Number of flashes after 100 steps: {flashes}")

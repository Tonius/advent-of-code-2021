from typing import Optional


with open("17-input.txt") as input_file:
    target_x, target_y = (
        input_file.read().strip().removeprefix("target area: ").split(", ")
    )

target_from_x, target_to_x = (int(x) for x in target_x.removeprefix("x=").split(".."))
target_from_y, target_to_y = (int(y) for y in target_y.removeprefix("y=").split(".."))

target_corners = [
    (target_from_x, target_from_y),
    (target_from_x, target_to_y),
    (target_to_x, target_from_y),
    (target_to_x, target_to_y),
]


SIMULATE_STEPS = 300


class Probe:
    def __init__(self, x_velocity: int, y_velocity: int):
        self.x: int = 0
        self.y: int = 0
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def get_highest_y(self) -> Optional[int]:
        highest_y = self.y

        for _ in range(SIMULATE_STEPS):
            self.step()
            highest_y = max(highest_y, self.y)

            if (
                target_from_x <= self.x <= target_to_x
                and target_from_y <= self.y <= target_to_y
            ):
                return highest_y

    def step(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x_velocity > 0:
            self.x_velocity -= 1
        elif self.x_velocity < 0:
            self.x_velocity += 1

        self.y_velocity -= 1


count = 0
highest_highest_y = None

for x_velocity in range(target_to_x + 1):
    print(f"{x_velocity} / {target_to_x}")

    for y_velocity in range(target_from_y - 1, target_from_y + SIMULATE_STEPS):
        highest_y = Probe(x_velocity, y_velocity).get_highest_y()
        if highest_y is not None:
            count += 1
            if highest_highest_y is None or highest_y > highest_highest_y:
                highest_highest_y = highest_y

print(f"\nHighest Y position: {highest_highest_y}")
print(f"Amount of initial velocities that reach target: {count}")

from math import ceil, floor
from typing import Literal, Optional, Sequence, Union


Side = Literal["left", "right"]


class Node:
    parent: Optional["Pair"] = None
    parent_side: Optional[Side] = None

    def get_magnitude(self) -> int:
        raise NotImplementedError

    def get_depth(self):
        depth = 0

        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent

        return depth

    @classmethod
    def from_data(cls, data: Union[Sequence, int]):
        if isinstance(data, int):
            return Number(data)

        return Pair(Node.from_data(data[0]), Node.from_data(data[1]))


class Number(Node):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

    def __str__(self):
        return str(self.value)

    def get_magnitude(self):
        return self.value

    def get_number_to_side(self, side: Side) -> Optional["Number"]:
        prev_node = self
        node = self.parent
        switch_sides = False

        while True:
            if node is None:
                return None

            child = getattr(
                node,
                ("right" if side == "left" else "left") if switch_sides else side,
            )

            if child is not prev_node:
                if isinstance(child, Number):
                    return child
                elif isinstance(child, Pair):
                    prev_node = node
                    node = child
                    switch_sides = True
            else:
                prev_node = node
                node = node.parent

    def split(self):
        value = self.value / 2
        self.parent.set_child(
            self.parent_side, Pair(Number(floor(value)), Number(ceil(value)))
        )


class Pair(Node):
    left: Node
    right: Node

    def __init__(self, left: Node, right: Node):
        self.set_child("left", left)
        self.set_child("right", right)

    def set_child(self, side: Side, value: Node):
        setattr(self, side, value)
        value.parent = self
        value.parent_side = side

    def __repr__(self):
        return f"Pair({repr(self.left)}, {repr(self.right)})"

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def __add__(self, other: "Pair"):
        return Pair(self, other).reduce()

    def get_magnitude(self):
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def find_pair_to_explode(self):
        if self.get_depth() == 4:
            return self

        for name in ("left", "right"):
            child = getattr(self, name)

            if isinstance(child, Pair):
                result = child.find_pair_to_explode()
                if result is not None:
                    return result

        return None

    def find_number_to_split(self):
        for name in ("left", "right"):
            child = getattr(self, name)

            if isinstance(child, Number) and child.value >= 10:
                return child

            if isinstance(child, Pair):
                result = child.find_number_to_split()
                if result is not None:
                    return result

        return None

    def reduce(self) -> "Pair":
        pair_to_explode = self.find_pair_to_explode()
        number_to_split = self.find_number_to_split()

        if pair_to_explode is not None:
            pair_to_explode.explode()
            self.reduce()
        elif number_to_split is not None:
            number_to_split.split()
            self.reduce()

        return self

    def explode(self):
        if not isinstance(self.left, Number) or not isinstance(self.right, Number):
            raise Exception("Not a pair of numbers!")

        left_number = self.left.get_number_to_side("left")
        if left_number is not None:
            left_number.value += self.left.value

        right_number = self.right.get_number_to_side("right")
        if right_number is not None:
            right_number.value += self.right.value

        self.parent.set_child(self.parent_side, Number(0))


with open("18-input.txt") as input_file:
    pairs = [eval(line) for line in input_file.read().strip().splitlines()]


print("\npart 1")

final_sum = Node.from_data(pairs[0])
for pair in pairs[1:]:
    final_sum += Node.from_data(pair)

print(f"Final sum: {final_sum}")
print(f"Magnitude of final sum: {final_sum.get_magnitude()}")


print("\npart 2")

max_magnitude = 0

for pair in pairs:
    for other_pair in pairs:
        if other_pair is not pair:
            result: Pair = Node.from_data(pair) + Node.from_data(other_pair)
            max_magnitude = max(max_magnitude, result.get_magnitude())

print(f"Largest magnitude of any sum: {max_magnitude}")

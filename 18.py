from typing import Literal, Optional, Sequence, Union


Side = Literal["left", "right"]


class Node:
    parent: Optional["Pair"] = None
    parent_side: Optional[Side] = None

    def get_depth(self):
        depth = 0

        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent

        return depth

    def split(self):
        print(f"split {repr(self)}")

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

    def get_number_to_left(self) -> Optional["Number"]:
        # TODO: zie boekje
        ...

    def get_number_to_right(self) -> Optional["Number"]:
        ...


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
            if isinstance(child, Number):
                if child.value >= 10:
                    return child
            elif isinstance(child, Pair):
                result = child.find_number_to_split()
                if result is not None:
                    return result

        return None

    def reduce(self) -> "Pair":
        pair_to_explode = self.find_pair_to_explode()
        number_to_split = self.find_number_to_split()

        if pair_to_explode is not None:
            pair_to_explode.explode()
        elif number_to_split is not None:
            number_to_split.split()

        return self

    def explode(self):
        print(f"explode {repr(self)}")

        if not isinstance(self.left, Number) or not isinstance(self.right, Number):
            raise Exception("Not a pair of numbers!")

        left_number = self.left.get_number_to_left()
        if left_number is not None:
            left_number.value += self.left.value

        right_number = self.right.get_number_to_right()
        if right_number is not None:
            right_number.value += self.right.value

        self.parent.set_child(self.parent_side, Number(0))


pair = Pair.from_data([[[[[9, 8], 1], 2], 3], 4])
print(pair.reduce())

from typing import Optional, Sequence, Union


class Number:
    x: Union[int, "Number"]
    y: Union[int, "Number"]

    def __new__(cls, x: Union[int, "Number"], y: Union[int, "Number"]):
        number = super().__new__(cls)
        number.x = x
        number.y = y
        return number.reduce()

    @classmethod
    def from_data(cls, data: Union[Sequence, int]):
        if isinstance(data, int):
            return data

        return Number(Number.from_data(data[0]), Number.from_data(data[1]))

    def __repr__(self):
        return f"Number({repr(self.x)}, {repr(self.y)})"

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def __add__(self, other: "Number"):
        return Number(self, other)

    def reduce(self) -> "Number":
        return self

    # TODO: first *regular* number on the left or right is changed so this is wrong
    def find_nested(
        self,
        count: int = 0,
        left: Optional["Number"] = None,
        right: Optional["Number"] = None,
    ):
        if count == 4:
            return self, left, right

        if isinstance(self.x, Number):
            result = self.x.find_nested(count + 1, right=self.y)
            if result is not None:
                return result

        if isinstance(self.y, Number):
            result = self.y.find_nested(count + 1, left=self.x)
            if result is not None:
                return result

        return None


number = Number.from_data([[[[[9, 8], 1], 2], 3], 4])
print(number.find_nested())

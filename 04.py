from dataclasses import dataclass
from typing import Optional


@dataclass
class BoardNumber:
    row: int
    column: int
    value: int
    marked: bool


class Board:
    row_count: int
    column_count: int
    numbers: list["BoardNumber"]
    last_called_number: Optional[int] = None

    def __init__(self, lines: list[str]):
        ...

    def mark_number(self, number: int):
        self.last_called_number = None

        for board_number in self.numbers:
            if board_number.value == number:
                board_number.marked = True
                self.last_called_number = number

    def wins(self) -> bool:
        for row in range(self.row_count):
            if all(number.marked for number in self.numbers if number.row == row):
                return True

        for column in range(self.column_count):
            if all(number.marked for number in self.numbers if number.column == column):
                return True

        return False

    def get_score(self) -> int:
        unmarked_sum = sum(number.value for number in self.numbers if not number.marked)

        return unmarked_sum * self.last_called_number


with open("04-input.txt") as input_file:
    input_data = input_file.read().split("\n\n")

numbers_to_draw = input_data[0]

for board_lines in input_data[1:]:
    ...

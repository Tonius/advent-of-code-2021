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
        self.numbers = []

        for row, row_numbers in enumerate(lines):
            for column, number in enumerate(row_numbers.split()):
                self.numbers.append(
                    BoardNumber(row=row, column=column, value=int(number), marked=False)
                )

        self.row_count = max(number.row for number in self.numbers) + 1
        self.column_count = max(number.column for number in self.numbers) + 1

    def __repr__(self):
        return (
            f"Board(row_count={self.row_count}, column_count={self.column_count}, "
            f"numbers={repr(self.numbers)})"
        )

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

numbers_to_draw = [int(number) for number in input_data[0].split(",")]

boards = [Board(board_data.splitlines()) for board_data in input_data[1:]]
board_count = len(boards)

for number in numbers_to_draw:
    for board in boards:
        board.mark_number(number)

        if board.wins():
            current_board_count = len(boards)

            if current_board_count == board_count:
                print(f"Score of first board to win: {board.get_score()}")
            elif current_board_count == 1:
                print(f"Score of last board to win: {board.get_score()}")
                exit()

            boards = [b for b in boards if b is not board]

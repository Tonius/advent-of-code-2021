def get_amount_of_values_greater_than_previous_value(values: list[int]) -> int:
    return sum(
        1 if second_value > first_value else 0
        for first_value, second_value in zip(values[:-1], values[1:])
    )


def get_three_value_sliding_window_sums(values: list[int]) -> list[int]:
    return [sum(window) for window in zip(values[:-2], values[1:-1], values[2:])]


with open("01-input.txt") as input_file:
    values = [int(line) for line in input_file]

print(get_amount_of_values_greater_than_previous_value(values))
print(
    get_amount_of_values_greater_than_previous_value(
        get_three_value_sliding_window_sums(values)
    )
)

def get_amount_of_values_greater_than_previous_value(values: list[int]) -> int:
    result = 0

    for first_value, second_value in zip(values[:-1], values[1:]):
        if second_value > first_value:
            result += 1

    return result


def get_three_value_sliding_window_sums(values: list[int]) -> list[int]:
    result: list[int] = []

    value_count = len(values)

    for index in range(value_count):
        if index < value_count - 2:
            result.append(values[index] + values[index + 1] + values[index + 2])

    return result


with open("01-input.txt") as input_file:
    values = [int(line) for line in input_file]

print(get_amount_of_values_greater_than_previous_value(values))
print(
    get_amount_of_values_greater_than_previous_value(
        get_three_value_sliding_window_sums(values)
    )
)

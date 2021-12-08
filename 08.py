entries = []

with open("08-input.txt") as input_file:
    for line in input_file:
        unique_patterns, output_value_digits = line.strip().split(" | ")
        entries.append(
            {
                "unique_patterns": [set(p) for p in unique_patterns.split()],
                "output_value_digits": [set(p) for p in output_value_digits.split()],
            }
        )


print("\npart 1")

number_of_digits_with_unique_segment_count = 0

for entry in entries:
    for digit in entry["output_value_digits"]:
        if len(digit) in (2, 4, 3, 7):
            number_of_digits_with_unique_segment_count += 1

print(
    "Amount of times that digits 1, 4, 7, or 8 appear: "
    f"{number_of_digits_with_unique_segment_count}"
)


print("\npart 2")


def find_pattern_with_length(patterns: list[set[str]], segment_count: int):
    for pattern in patterns:
        if len(pattern) == segment_count:
            patterns.remove(pattern)
            return pattern


def find_pattern_with_common_segments(
    patterns: list[set[str]], counts_per_digit: list[tuple[str, int]]
):
    for pattern in patterns:
        if all(
            len(pattern.intersection(digit)) == count
            for digit, count in counts_per_digit
        ):
            patterns.remove(pattern)
            return pattern


def determine_digit_patterns(patterns: list[set[str]]):
    patterns = list(patterns)

    one = find_pattern_with_length(patterns, 2)
    four = find_pattern_with_length(patterns, 4)
    seven = find_pattern_with_length(patterns, 3)
    eight = find_pattern_with_length(patterns, 7)
    two = find_pattern_with_common_segments(patterns, [(one, 1), (four, 2), (seven, 2)])
    nine = find_pattern_with_common_segments(
        patterns, [(one, 2), (four, 4), (seven, 3)]
    )
    five = find_pattern_with_common_segments(patterns, [(one, 1), (two, 3), (seven, 2)])
    six = find_pattern_with_common_segments(patterns, [(one, 1), (two, 4), (seven, 2)])
    zero = find_pattern_with_length(patterns, 6)
    three = patterns[0]

    return (zero, one, two, three, four, five, six, seven, eight, nine)


def get_digit_value(digit_patterns: tuple[set[str]], digit: set[str]):
    for value, pattern in enumerate(digit_patterns):
        if digit == pattern:
            return value


sum_of_output_values = 0

for entry in entries:
    digit_patterns = determine_digit_patterns(entry["unique_patterns"])
    output_value_digits = [
        get_digit_value(digit_patterns, digit) for digit in entry["output_value_digits"]
    ]
    output_value = int("".join(str(d) for d in output_value_digits))
    sum_of_output_values += output_value

print(f"Sum of all output values: {sum_of_output_values}")

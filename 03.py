from typing import Callable


with open("03-input.txt") as input_file:
    input_numbers = input_file.read().splitlines()


print("\npart 1")


def get_bit_counts_at_position(numbers: list[str], position: int) -> tuple[int, int]:
    zero_count = 0
    one_count = 0

    for number in numbers:
        bit = number[position]
        if bit == "1":
            one_count += 1
        else:
            zero_count += 1

    return zero_count, one_count


def get_most_common_bit_at_position(numbers: list[str], position: int) -> str:
    zero_count, one_count = get_bit_counts_at_position(numbers, position)

    return "1" if one_count >= zero_count else "0"


def get_least_common_bit_at_position(numbers: list[str], position: int) -> str:
    zero_count, one_count = get_bit_counts_at_position(numbers, position)

    return "1" if one_count < zero_count else "0"


binary_gamma_rate = ""
binary_epsilon_rate = ""

for position in range(len(input_numbers[0])):
    binary_gamma_rate += get_most_common_bit_at_position(input_numbers, position)
    binary_epsilon_rate += get_least_common_bit_at_position(input_numbers, position)

print(f"binary gamma rate: {binary_gamma_rate}")
print(f"binary epsilon rate: {binary_epsilon_rate}")

gamma_rate = int(binary_gamma_rate, 2)
epsilon_rate = int(binary_epsilon_rate, 2)

print(f"gamma rate: {gamma_rate}")
print(f"epsilon rate: {epsilon_rate}")
print(f"power consumption: {gamma_rate * epsilon_rate}")


print("\npart 2")


def find_rating(
    numbers: list[str], get_bit: Callable[[list[str], int], str], position: int = 0
):
    bit = get_bit(numbers, position)

    numbers = [number for number in numbers if number[position] == bit]
    if len(numbers) == 1:
        return numbers[0]

    return find_rating(numbers, get_bit, position + 1)


binary_oxygen_generator_rating = find_rating(
    input_numbers, get_most_common_bit_at_position
)
binary_co2_scrubber_rating = find_rating(
    input_numbers, get_least_common_bit_at_position
)

print(f"binary oxygen generator rating: {binary_oxygen_generator_rating}")
print(f"binary co2 scrubber rating: {binary_co2_scrubber_rating}")

oxygen_generator_rating = int(binary_oxygen_generator_rating, 2)
co2_scrubber_rating = int(binary_co2_scrubber_rating, 2)

print(f"oxygen generator rating: {oxygen_generator_rating}")
print(f"co2 scrubber rating: {co2_scrubber_rating}")
print(f"life support rating: {oxygen_generator_rating * co2_scrubber_rating}")

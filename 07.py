from typing import Callable


with open("07-input.txt") as input_file:
    crab_positions = [int(pos) for pos in input_file.readline().split(",")]


print("\npart 1")


def get_minimum_fuel_usage(get_fuel_usage: Callable[[int, int], int]):
    return min(
        sum(
            get_fuel_usage(crab_position, to_position)
            for crab_position in crab_positions
        )
        for to_position in range(min(crab_positions), max(crab_positions) + 1)
    )


def get_fuel_usage_one(crab_position: int, to_position: int):
    return abs(to_position - crab_position)


print(f"Minimum fuel usage: {get_minimum_fuel_usage(get_fuel_usage_one)}")


print("\npart 2")


def get_fuel_usage_two(crab_position: int, to_position: int):
    distance = abs(to_position - crab_position)

    # https://en.wikipedia.org/wiki/Triangular_number
    return int((distance * (distance + 1)) / 2)


print(f"Minimum fuel usage: {get_minimum_fuel_usage(get_fuel_usage_two)}")

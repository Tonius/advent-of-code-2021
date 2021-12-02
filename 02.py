with open("02-input.txt") as input_file:
    commands = [line.removesuffix("\n") for line in input_file]

print("\npart 1")

horizontal_pos: int = 0
depth: int = 0

for command in commands:
    if command.startswith("forward"):
        horizontal_pos += int(command.removeprefix("forward "))
    elif command.startswith("down"):
        depth += int(command.removeprefix("down "))
    elif command.startswith("up"):
        depth -= int(command.removeprefix("up "))

print(f"horizontal position: {horizontal_pos}")
print(f"depth: {depth}")
print(f"result: {horizontal_pos * depth}")

print("\npart 2")

aim: int = 0
horizontal_pos: int = 0
depth: int = 0

for command in commands:
    if command.startswith("down"):
        aim += int(command.removeprefix("down "))
    elif command.startswith("up"):
        aim -= int(command.removeprefix("up "))
    elif command.startswith("forward"):
        value = int(command.removeprefix("forward "))
        horizontal_pos += value
        depth += aim * value

print(f"horizontal position: {horizontal_pos}")
print(f"depth: {depth}")
print(f"result: {horizontal_pos * depth}")

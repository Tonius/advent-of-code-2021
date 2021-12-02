commands: list[tuple[str, int]] = []
with open("02-input.txt") as input_file:
    for line in input_file:
        command, value = line.split()
        commands.append((command, int(value)))

print("\npart 1")

horizontal_pos: int = 0
depth: int = 0

for command, value in commands:
    if command == "forward":
        horizontal_pos += value
    elif command == "down":
        depth += value
    elif command == "up":
        depth -= value

print(f"horizontal position: {horizontal_pos}")
print(f"depth: {depth}")
print(f"result: {horizontal_pos * depth}")

print("\npart 2")

aim: int = 0
horizontal_pos: int = 0
depth: int = 0

for command, value in commands:
    if command == "down":
        aim += value
    elif command == "up":
        aim -= value
    elif command == "forward":
        horizontal_pos += value
        depth += aim * value

print(f"horizontal position: {horizontal_pos}")
print(f"depth: {depth}")
print(f"result: {horizontal_pos * depth}")

from collections import Counter


with open("14-input.txt") as input_file:
    polymer, rule_lines = input_file.read().strip().split("\n\n")

pair_counts = Counter(
    (first + second) for first, second in zip(polymer[:-1], polymer[1:])
)
element_counts = Counter(polymer)

rules = dict(line.split(" -> ") for line in rule_lines.split("\n"))


def print_results():
    print(f"Result: {max(element_counts.values()) - min(element_counts.values())}")


for step in range(1, 40 + 1):
    for pair, pair_count in pair_counts.copy().items():
        pair_counts[pair] -= pair_count

        add_element = rules[pair]
        pair_counts[pair[0] + add_element] += pair_count
        pair_counts[add_element + pair[1]] += pair_count

        element_counts[add_element] += pair_count

    if step == 10:
        print("\nafter 10 steps")
        print_results()

print("\nafter 40 steps")
print_results()

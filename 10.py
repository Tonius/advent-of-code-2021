from math import ceil
from typing import Optional


with open("10-input.txt") as input_file:
    system = input_file.read().splitlines()


closing_to_opening_chars = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}


def analyze_line(line: str) -> tuple[list[str], Optional[str]]:
    stack = []

    for char in line:
        if char in closing_to_opening_chars:
            if stack.pop() != closing_to_opening_chars[char]:
                return stack, char
        else:
            stack.append(char)

    return stack, None


print("\npart 1")

syntax_error_score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

total_syntax_error_score = 0

for line in system:
    _, illegal_character = analyze_line(line)
    if illegal_character is not None:
        total_syntax_error_score += syntax_error_score_table[illegal_character]

print(f"Total syntax error score: {total_syntax_error_score}")


print("\npart 2")

completion_score_table = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

completion_scores = []

for line in system:
    stack, illegal_character = analyze_line(line)
    if illegal_character is not None:
        continue

    line_score = 0

    stack.reverse()
    for char in stack:
        line_score *= 5
        line_score += completion_score_table[char]

    completion_scores.append(line_score)

middle_completion_score = sorted(completion_scores)[
    ceil(len(completion_scores) / 2) - 1
]

print(f"Middle completion score: {middle_completion_score}")

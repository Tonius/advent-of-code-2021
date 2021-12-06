with open("06-input.txt") as input_file:
    initial_fish_timers = [int(f) for f in input_file.readline().split(",")]

fish_counts = {timer: 0 for timer in range(9)}
for timer in initial_fish_timers:
    fish_counts[timer] += 1

for day in range(1, 256 + 1):
    new_fish_counts = {timer: 0 for timer in fish_counts}

    for timer, fish_count in fish_counts.items():
        if timer == 0:
            new_fish_counts[6] += fish_count
            new_fish_counts[8] += fish_count
        else:
            new_fish_counts[timer - 1] += fish_count

    fish_counts = new_fish_counts

    if day == 80:
        print(f"Number of fish after 80 days: {sum(fish_counts.values())}")

print(f"Number of fish after 256 days: {sum(fish_counts.values())}")

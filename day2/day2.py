import numpy as np

day2_path = "day2/input.txt"
# day2_path = "day2/input_test.txt"  # Test data

with open(day2_path, 'r') as file:
    day2 = [list(map(int, line.split())) for line in file]

print(day2)

## ----- PART 1 ----- ##

safe = 0

for i in range(len(day2)):
    unsafe = 0
    if day2[i][0] > day2[i][1]:
        dir = "descending"
    else:
        dir = "ascending"
    for j in range(len(day2[i])-1):
        if dir == "ascending":
            if (day2[i][j+1] - day2[i][j]) > 3 or (day2[i][j+1] - day2[i][j]) <= 0:
                unsafe = True
        if dir == "descending":
            if (day2[i][j] - day2[i][j+1]) > 3 or (day2[i][j] - day2[i][j+1]) <= 0:
                unsafe = True
    if unsafe == False:
        safe += 1
print(safe)


## ----- PART 2 ----- ##

def is_safe(report):
    """Check if a report is safe without any fixes."""
    if report[0] > report[1]:
        dir = "descending"
    else:
        dir = "ascending"
    for j in range(len(report) - 1):
        if dir == "ascending":
            if (report[j + 1] - report[j]) > 3 or (report[j + 1] - report[j]) <= 0:
                return False
        if dir == "descending":
            if (report[j] - report[j + 1]) > 3 or (report[j] - report[j + 1]) <= 0:
                return False
    return True

safe = 0

for report in day2:
    if is_safe(report):
        safe += 1
    else:
        # Try removing each level and check if the report becomes safe
        for k in range(len(report)):
            modified_report = report[:k] + report[k+1:]
            if is_safe(modified_report):
                safe += 1
                break  # No need to try further removals for this report

print(safe)
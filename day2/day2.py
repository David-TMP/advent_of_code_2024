import numpy as np

day2_path = "day2/day2_input.txt"
# day2_path = "day2/day2_input_test.txt"  # Test data

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

safe = 0

for i in range(len(day2)):
    unsafe = 0
    potential_fix = 0
    if day2[i][0] > day2[i][1]:
        dir = "descending"
    else:
        dir = "ascending"
    for j in range(len(day2[i])-1):
        if dir == "ascending":
            if ((day2[i][j+1] - day2[i][j]) > 3) and ((j+1) == len(day2[i]) or j == 0):
                unsafe += 1
                potential_fix += 1
            elif (day2[i][j+1] - day2[i][j]) > 3:
                unsafe += 1
            elif (day2[i][j+1] - day2[i][j]) <= 0:
                unsafe += 1
                potential_fix += 1
        if dir == "descending":
            if ((day2[i][j] - day2[i][j+1]) > 3) and ((j+1) == len(day2[i]) or j == 0):
                unsafe += 1
                potential_fix += 1
            elif (day2[i][j] - day2[i][j+1]) > 3:
                unsafe += 1
            elif (day2[i][j] - day2[i][j+1]) <= 0:
                unsafe += 1
                potential_fix += 1
    if unsafe == 1 and potential_fix == 1:
        safe += 1
    elif unsafe == 0:
        safe += 1

print(safe)







## ----- PART 2 V2 ----- ##

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
                unsafe += 1
        if dir == "descending":
            if (day2[i][j] - day2[i][j+1]) > 3 or (day2[i][j] - day2[i][j+1]) <= 0:
                unsafe += 1
    if unsafe <= 1:
        safe += 1


# print(safe)
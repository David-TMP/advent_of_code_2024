import re

day3_path = "day3/input.txt"
day3_test_path = "day3/input_test.txt"  # Test data

with open(day3_path, 'r') as file:
    day3 = [line.strip() for line in file]


## ----- PART 1 ----- ##
x = [re.findall(r"(?<=mul\()\d+,\d+(?=\))", string) for string in day3]

# Flatten the list of lists
flat_list = [pair for sublist in x for pair in sublist]

# Better approach (more efficient and safer)
total = sum(int(a) * int(b) for a, b in (pair.split(",") for pair in flat_list))
print(f'Part 1 Solution = {total}')


## ----- PART 2 ----- ##
x = [re.findall(r"don\'t|do|(?<=mul\()\d+,\d+(?=\))", string) for string in day3]
flat_list = [pair for sublist in x for pair in sublist]

contador = 0
clean_list = []
for i in range(len(flat_list)):
    if(flat_list[i] == "do"):
        contador = 0
    elif(flat_list[i] == "don't"):
        contador = 1
    if contador == 1:
        next
    if contador == 0 and flat_list[i] != "do":
        clean_list.append(flat_list[i])

total = sum(int(a) * int(b) for a, b in (pair.split(",") for pair in clean_list))
print(f'Part 2 Solution = {total}')





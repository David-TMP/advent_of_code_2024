import re
import numpy as np

day4_path = "day4/input.txt"
day4_test_path = "day4/input_test.txt"  # Test data

with open(day4_path, 'r') as file:
    day4 = [line.strip() for line in file]

array = np.array([list(row) for row in day4])


## ----- PART 1 ----- ##

n_rows, n_cols = array.shape
word = 'XMAS|SAMX'
pattern = f"(?=({word}))"

contador = 0

for i in range(-n_rows+len('XMAS'), n_rows-len('XMAS')+1):
    x = re.findall(pattern, ''.join(np.diag(array, k=i)))
    if x:
        contador += len(x)

for i in range(-n_rows+len('XMAS'), n_rows-len('XMAS')+1):
    x = re.findall(pattern, ''.join(np.diag(np.fliplr(array), k=i)))
    if x:
        contador += len(x)

for i in range(n_rows):
    x = re.findall(pattern, ''.join(array[i]))
    if x:
        contador += len(x)

for i in range(n_cols):
    x = re.findall(pattern, ''.join(array[:, i]))
    if x:
        contador += len(x)


print(contador)


## ----- PART 2 ----- ##

part2_count = 0

for i in range(1, n_rows-1):
    for j in range(1, n_cols-1):
        if array[i, j] == 'A':
            if array[i-1, j-1] == 'M' and array[i+1, j+1] == 'S' and array[i-1, j+1] == 'S' and array[i+1, j-1] == 'M':
                part2_count += 1

            if  array[i-1, j-1] == 'M' and array[i+1, j+1] == 'S' and array[i-1, j+1] == 'M' and array[i+1, j-1] == 'S':
                part2_count += 1
            
            if array[i-1, j-1] == 'S' and array[i+1, j+1] == 'M' and array[i-1, j+1] == 'S' and array[i+1, j-1] == 'M':
                part2_count += 1

            if array[i-1, j-1] == 'S' and array[i+1, j+1] == 'M' and array[i-1, j+1] == 'M' and array[i+1, j-1] == 'S':
                part2_count += 1


print(part2_count)



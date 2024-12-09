from collections import deque 
import math

file_path = "day9/input_test.txt"

with open (file_path, 'r') as f:
    disk_map = [int(digit) for digit in f.read().strip()]

file_id = 0

files = deque(disk_map[::2])
space = deque(disk_map[1::2])

print(files)
print(space)

sol = list()

def solve_part1():
    contador = -1
    while files:
        contador += 1
        if (contador % 2) == 0:  # If even --> File
            for _ in range(files[0]):
                sol.append(math.ceil(contador/2))
            files.popleft()
        else:  # If odd --> Space
            if(space[0] == files[len(files)-1]):
                for i in range(files[len(files)-1]):
                    sol.append(len(files)-1+(math.ceil(contador/2)))
                files.pop()
                space.popleft()
                continue
            while (space[0] > files[len(files)-1]):
                for i in range(files[len(files)-1]):
                    sol.append(len(files)-1+(math.ceil(contador/2)))
                space[0] = space[0] - files[len(files)-1]
                files.pop()
            if(space[0] < files[len(files)-1]):
                for i in range(space[0]):
                    sol.append(len(files)-1+(math.ceil(contador/2)))
                files[len(files)-1] = files[len(files)-1] - space[0]
                space.popleft()
    return(sol)

x = solve_part1()
print(sum(index*value for index, value in enumerate(x)))
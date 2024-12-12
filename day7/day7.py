from itertools import product
import timeit

# Define the file name
file_name = 'day7/input.txt'

# Initialize the objects to store data
before_colon = []
after_colon = []

# Read the file
with open(file_name, 'r') as file:
    for line in file:
        # Split the line by ':'
        parts = line.strip().split(':')
        # Add the number before ':' to the first list
        before_colon.append(int(parts[0].strip()))
        # Add the numbers after ':' to the second list as a tuple of integers
        after_colon.append(tuple(map(int, parts[1].strip().split())))

# Output the results
# print("Numbers before the colon:", before_colon)
# print("Numbers after the colon:", after_colon)


## ----- PART 1 ----- ##

def find_calibration_part1():
    res = []
    for index, equation in enumerate(after_colon):
        if len(equation)-1 == 1:
            operations = [("+"), ("*")]
        else:
            operations = list(product(["+", "*"], repeat=len(equation)-1))
        # Process each set of operations
        for op_set in operations:  # Reset i here for each op_set
            result = equation[0]
            for i, op in enumerate(op_set):  # Local i resets for each op_set
                if op == "+":
                    result += equation[i + 1]
                elif op == "*":
                    result *= equation[i + 1]
            # Check if result matches the corresponding value in before_colon
            if result == before_colon[index]:
                res.append(before_colon[index])
                break
    return res        

start = timeit.default_timer()
part1_sol = find_calibration_part1()
elapsed_time = timeit.default_timer()-start
print(f'Day 7 Part 1 Solution = {sum(part1_sol)}')
print(f'Day 7 Part 1 Run Time = {str(elapsed_time)}')



## ----- PART 2 ----- ##

def find_calibration_part2():
    res = []
    for index, equation in enumerate(after_colon):
        # Include the concatenation operator '^'
        operations = list(product(["+", "*", "^"], repeat=len(equation)-1))
        
        # Process each set of operations
        for op_set in operations:
            result = equation[0]
            for i, op in enumerate(op_set):
                if op == "+":
                    result += equation[i + 1]
                elif op == "*":
                    result *= equation[i + 1]
                elif op == "^":
                    # Concatenation: combine digits
                    result = int(str(result) + str(equation[i + 1]))
            # Check if the final result matches the target
            if result == before_colon[index]:
                res.append(before_colon[index])
                break  # Move to the next equation after finding a valid combination
    return res

# def find_calibration_part2():
#     res = []
#     for index, equation in enumerate(after_colon):
#         if len(equation)-1 == 1:
#             operations = [("+"), ("*"), ("^")]
#         else:
#             operations = list(product(["+", "*", "^"], repeat=len(equation)-1))
#         # Process each set of operations
#         for op_set in operations:  # Reset i here for each op_set
#             result = equation[0]
#             for i, op in enumerate(op_set):  # Local i resets for each op_set
#                 if op == "+":
#                     result += equation[i + 1]
#                 elif op == "*":
#                     result *= equation[i + 1]
#                 elif op == "^":
#                     length = len(str(equation[i+1]))
#                     result = int(str(result) + str(equation[i+1]))
#             # Check if result matches the corresponding value in before_colon
#             if result == before_colon[index]:
#                 res.append(before_colon[index])
#                 break
#             if result > before_colon[index]:
#                 break
#     return res        

start = timeit.default_timer()
part2_sol = find_calibration_part2()
elapsed_time = timeit.default_timer()-start
print(f'Day 7 Part 2 Solution = {sum(part2_sol)}')
print(f'Day 7 Part 2 Run Time = {str(elapsed_time)}')
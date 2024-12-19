import re
import timeit

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Strip whitespace and newline characters from each line
    stripped_lines = [line.strip() for line in lines]
    
    available_patterns = []
    desirable_designs = []
    
    # Flag to indicate whether we've processed the headers
    headers_parsed = False
    
    for line in stripped_lines:
        if not headers_parsed:
            if line:
                # Split the header line by commas and strip any extra whitespace
                available_patterns = [p.strip() for p in line.split(',')]
                headers_parsed = True  # Headers have been parsed
        else:
            if line:
                # Append non-empty lines to data_lines
                desirable_designs.append(line)
    
    return available_patterns, desirable_designs


## ----- PART 1 ----- ##

def can_form_design(design, patterns):
    # dp[i] will be True if we can form design[:i] from the given patterns
    dp = [False] * (len(design) + 1)
    dp[0] = True  # empty string can always be formed

    for i in range(len(design)):
        if dp[i]:
            # Try all patterns and see if any fits starting at i
            for p in patterns:
                # If pattern p matches design starting at i
                if design[i:i+len(p)] == p:
                    dp[i+len(p)] = True
    
    return dp[len(design)]


def solve_part1(input_file):

    possible = 0
    
    # Parse the input file
    available_patterns, desirable_designs = read_input_file(input_file)

    for design in desirable_designs:
        if can_form_design(design, available_patterns):
            possible += 1
    
    return(possible)

start = timeit.default_timer()
part1_sol = solve_part1(input_file="day19/input.txt")
elapsed_time = timeit.default_timer()-start
print(f'Day 19 Part 1 Solution = {part1_sol}')
print(f'Day 19 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

def count_possible_designs(design, patterns):
    # dp[i] will be True if we can form design[:i] from the given patterns
    dp = [0] * (len(design) + 1)
    dp[0] = 1  # empty string can always be formed

    for i in range(len(design)):
        if dp[i]:
            # Try all patterns and see if any fits starting at i
            for p in patterns:
                # If pattern p matches design starting at i
                if design[i:i+len(p)] == p:
                    dp[i+len(p)] += dp[i]
    
    return dp[len(design)]


def solve_part2(input_file):

    res = []
    
    # Parse the input file
    available_patterns, desirable_designs = read_input_file(input_file)

    for design in desirable_designs:
        res.append(count_possible_designs(design, available_patterns))
    
    return(sum(res))

start = timeit.default_timer()
part2_sol = solve_part2(input_file="day19/input.txt")
elapsed_time = timeit.default_timer()-start
print(f'Day 19 Part 2 Solution = {part2_sol}')
print(f'Day 19 Part 2 Run Time = {str(elapsed_time)}')
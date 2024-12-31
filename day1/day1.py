import numpy as np
import timeit

day1_input = np.loadtxt("day1/input.txt", dtype=np.int64)


## ----- PART 1 ----- ##

def sort_lists(input):

    day1_transposed = input.transpose()

    day1_transposed.sort(axis = 1)
    left_list_sorted = day1_transposed[0]
    right_list_sorted = day1_transposed[1]

    return(left_list_sorted, right_list_sorted)


def solve_part1(left_list_sorted, right_list_sorted):

    day1_part1_res = sum(abs(right_list_sorted - left_list_sorted))

    return(day1_part1_res)

start = timeit.default_timer()
left_list_sorted, right_list_sorted = sort_lists(day1_input)
part1_sol = solve_part1(left_list_sorted, right_list_sorted)
elapsed_time = timeit.default_timer()-start
print(f'Day 1 Part 1 Solution = {part1_sol}')
print(f'Day 1 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

def solve_part2(right_list_sorted, left_list_sorted):

    left_indices = np.searchsorted(right_list_sorted, left_list_sorted, side = "left")
    right_indices = np.searchsorted(right_list_sorted, left_list_sorted, side = "right")

    counts = right_indices - left_indices

    day1_part2_res = sum(left_list_sorted * counts)
    
    return(day1_part2_res)

start = timeit.default_timer()
part2_sol = solve_part2(right_list_sorted, left_list_sorted)
elapsed_time = timeit.default_timer()-start
print(f'Day 2 Part 2 Solution = {part2_sol}')
print(f'Day 2 Part 2 Run Time = {str(elapsed_time)}')
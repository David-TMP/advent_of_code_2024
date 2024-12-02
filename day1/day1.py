import numpy as np

day1 = np.loadtxt("day1/day1_input.txt", dtype=np.int64)
# day1 = np.loadtxt("day1/day1_input_test.txt", dtype=np.int64)  # Test data

## ----- PART 1 ----- ##
day1_transposed = day1.transpose()

day1_transposed.sort(axis = 1)
left_list_sorted = day1_transposed[0]
right_list_sorted = day1_transposed[1]

day1_part1_res = sum(abs(right_list_sorted - left_list_sorted))

print(day1_part1_res)


## ----- PART 2 ----- ##

left_indices = np.searchsorted(right_list_sorted, left_list_sorted, side = "left")
right_indices = np.searchsorted(right_list_sorted, left_list_sorted, side = "right")

counts = right_indices - left_indices

day1_part2_res = sum(left_list_sorted * counts)
print(day1_part2_res)
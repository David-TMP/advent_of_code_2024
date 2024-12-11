import timeit
import cProfile  # To find bottlenecks
from collections import defaultdict

with open("day11/input.txt", "r") as f:
    stones = [int(stone) for stone in f.read().split()]

## ----- PART 1 ----- ##

def count_digits(n):
    return len(str(abs(n))) if n != 0 else 1

def solve_part1(stones_current, n_blink):
    
    stones_new = []
    
    while n_blink > 0:
        stones_new = []
        while stones_current:
            current_stone = stones_current.pop()
            n_digits = count_digits(current_stone)

            if current_stone == 0:
                stones_new.append(1)

            elif n_digits % 2 == 0:  # Even number
                half = n_digits // 2
                left_part = current_stone // (10 ** half)
                right_part = current_stone % (10 ** half)
                stones_new.extend([left_part, right_part])
            else:
                stones_new.append(current_stone * 2024)   
        n_blink -= 1
        stones_current = stones_new.copy()
    return(len(stones_new))


start = timeit.default_timer()
part1_sol = solve_part1(stones_current = stones, n_blink = 25)
elapsed_time = timeit.default_timer()-start
print(f'Day 11 Part 1 Solution = {part1_sol}')
print(f'Day 11 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- #

with open("day11/input.txt", "r") as f:
    stones = [int(stone) for stone in f.read().split()]

stones_freq = defaultdict(int)
for stone in stones:
    stones_freq[stone] += 1

def solve_part2(stones_freq, n_blink):
    
    while n_blink > 0:
        stones_new = defaultdict(int)
        for current_stone, count in stones_freq.items():    
            if current_stone == 0:
                stones_new[1] += count

            else:
                n_digits = count_digits(current_stone)

                if n_digits % 2 == 0:  # Even number
                    half = n_digits // 2
                    left_part = current_stone // (10 ** half)
                    right_part = current_stone % (10 ** half)
                    stones_new[left_part] += count
                    stones_new[right_part]  += count
                else:
                    stones_new[current_stone * 2024] += count   
        n_blink -= 1
        stones_freq = stones_new

    
    # Calculate the total number of stones
    total_stones = sum(stones_freq.values())
    return total_stones


start = timeit.default_timer()
part2_sol = solve_part2(stones_freq = stones_freq, n_blink = 75)
elapsed_time = timeit.default_timer()-start
print(f'Day 11 Part 2 Solution = {part2_sol}')
print(f'Day 11 Part 2 Run Time = {str(elapsed_time)}')
import math
import timeit
from collections import defaultdict

with open("day22/input.txt", "r") as f:
    secrets = [int(line.strip()) for line in f]



## ----- PART 1 ----- ##

def solve_part1(secrets):

    res = []

    for secret in secrets:
        n_generations = 2000
        while(n_generations>0):
            # step 1:
            secret = ((secret * 64) ^ secret) % 16777216
            
            # step 2:
            secret = ((math.floor(secret / 32)) ^ secret) % 16777216

            # step 3:
            secret = ((secret * 2048) ^ secret) % 16777216

            n_generations -= 1
        
        res.append(secret)

    return(sum(res))

start = timeit.default_timer()
part1_sol = solve_part1(secrets)
elapsed_time = timeit.default_timer()-start
print(f'Day 22 Part 1 Solution = {part1_sol}')
print(f'Day 22 Part 1 Run Time = {str(elapsed_time)}')



## ----- PART 2 ----- ##

def evolve_secret(secret: int) -> int:
    """
    Evolve 'secret' once according to the puzzle rules:
      1) secret = ((secret * 64) ^ secret) % 16777216
      2) secret = ((secret // 32) ^ secret) % 16777216
      3) secret = ((secret * 2048) ^ secret) % 16777216
    Returns the new 'secret'.
    """
    # Step 1
    secret = ((secret * 64) ^ secret) % 16777216
    # Step 2
    secret = ((secret // 32) ^ secret) % 16777216
    # Step 3
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

def solve_part2(secrets):
    """
    For each buyer/secret:
      - Generate 2001 prices (the first is the secret's ones digit),
        then 2000 changes.
      - For each distinct 4-change pattern, record the earliest
        sell price in a dictionary.
    Return the maximum total bananas achievable with the single best pattern.
    """

    # Dictionary: pattern_of_4_changes -> sum_of_sell_prices_across_all_buyers
    pattern_to_sum = defaultdict(int)

    for initial_secret in secrets:
        # Generate 2001 prices for this buyer
        prices = []
        secret = initial_secret
        prices.append(secret % 10)  # p_0

        # We'll generate the next 2000 secrets & prices
        for _ in range(2000):
            secret = evolve_secret(secret)
            prices.append(secret % 10)  # next price

        # Now compute the 2000 changes
        changes = []
        for i in range(2000):
            changes.append(prices[i+1] - prices[i])

        # Track which patterns we've already seen for THIS buyer
        seen_patterns = set()

        # For i in [0..1996], pattern = (changes[i], i+1, i+2, i+3)
        # If it's new for this buyer, record the price at i+4.
        for i in range(2000 - 3):
            pattern = (changes[i], changes[i+1], changes[i+2], changes[i+3])
            if pattern not in seen_patterns:
                seen_patterns.add(pattern)
                # The sell price is prices[i+4]
                sell_price = prices[i+4]
                pattern_to_sum[pattern] += sell_price

    # Find the best total
    best_total = max(pattern_to_sum.values())

    return best_total

start = timeit.default_timer()
part2_sol = solve_part2(secrets)
elapsed_time = timeit.default_timer()-start
print(f'Day 22 Part 2 Solution = {part2_sol}')
print(f'Day 22 Part 2 Run Time = {str(elapsed_time)}')
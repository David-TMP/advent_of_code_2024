from math import gcd
import timeit

## ----- PART 1 ----- ##

def solve_part1():
    # Read the input from input.txt in the root directory
    with open("day8/input.txt", "r", encoding="utf-8") as f:
        grid = [line.rstrip('\n') for line in f]
        
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Dictionary to store antenna positions by frequency
    # Key: frequency character, Value: list of (row, col) positions
    antennas = {}
    
    for r in range(height):
        for c in range(width):
            ch = grid[r][c]
            if ch != '.':
                antennas.setdefault(ch, []).append((r, c))
    
    # We'll use a set to store the unique antinode positions
    antinodes = set()
    
    # For each frequency, consider all pairs of antennas
    for freq, positions in antennas.items():
        if len(positions) < 2:
            # With fewer than two antennas of the same frequency, no antinodes can form
            continue
        
        n = len(positions)
        for i in range(n):
            ax, ay = positions[i]
            for j in range(i+1, n):
                bx, by = positions[j]
                
                # First antinode: 2*A - B
                x1 = 2*ax - bx
                y1 = 2*ay - by
                if 0 <= x1 < height and 0 <= y1 < width:
                    antinodes.add((x1, y1))
                
                # Second antinode: 2*B - A
                x2 = 2*bx - ax
                y2 = 2*by - ay
                if 0 <= x2 < height and 0 <= y2 < width:
                    antinodes.add((x2, y2))
    
    # Print the number of unique antinodes
    return(len(antinodes))

start = timeit.default_timer()
print(f'Day 8 Part 1 Solution = {solve_part1()}')
elapsed_time = timeit.default_timer()-start
print(f'Day 8 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

def solve_part2():
    # Read the input from input.txt in the root directory
    with open("day8/input.txt", "r", encoding="utf-8") as f:
        grid = [line.rstrip('\n') for line in f]
        
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Dictionary to store antenna positions by frequency
    # Key: frequency character, Value: list of (row, col) positions
    antennas = {}
    
    for r in range(height):
        for c in range(width):
            ch = grid[r][c]
            if ch != '.':
                antennas.setdefault(ch, []).append((r, c))
    
    # Set to store all unique antinode positions
    antinodes = set()
    
    # For each frequency, consider all pairs of antennas
    for freq, positions in antennas.items():
        # If there is only one antenna of a certain frequency,
        # no line can form with another antenna of the same frequency.
        # Thus, that single antenna does not produce antinodes.
        if len(positions) < 2:
            continue
        
        n = len(positions)
        
        for i in range(n):
            r1, c1 = positions[i]
            for j in range(i+1, n):
                r2, c2 = positions[j]
                
                dr = r2 - r1
                dc = c2 - c1
                g = gcd(abs(dr), abs(dc))
                
                # Reduce to smallest step increments
                step_r = dr // g
                step_c = dc // g
                
                # Move forward along the line
                rr, cc = r1, c1
                while 0 <= rr < height and 0 <= cc < width:
                    antinodes.add((rr, cc))
                    rr += step_r
                    cc += step_c
                
                # Move backward along the line (starting again from (r1,c1))
                rr, cc = r1, c1
                while 0 <= rr < height and 0 <= cc < width:
                    antinodes.add((rr, cc))
                    rr -= step_r
                    cc -= step_c
    
    # Print the number of unique antinodes
    return(len(antinodes))

start = timeit.default_timer()
print(f'Day 8 Part 2 Solution = {solve_part2()}')
elapsed_time = timeit.default_timer()-start
print(f'Day 8 Part 2 Run Time = {str(elapsed_time)}')
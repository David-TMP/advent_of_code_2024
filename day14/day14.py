import numpy as np
import timeit
import math

def parse_input(file_path, grid_width, grid_height):
    """
    Parses the input file and returns NumPy arrays for positions and movements.

    Parameters:
    - file_path (str): Path to the input.txt file.

    Returns:
    - positions (np.ndarray): Array of shape (N, 2) containing Xp and Yp.
    - movements (np.ndarray): Array of shape (N, 2) containing Xv and Yv.
    """
    positions_x = []
    positions_y = []
    movements_x = []
    movements_y = []
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Remove any leading/trailing whitespace
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            # Split the line into position and movement parts
            try:
                p_part, v_part = line.split()
            except ValueError:
                raise ValueError(f"Line {line_num}: Incorrect format. Expected two parts separated by space.")
            
            # Extract position values
            try:
                p_values = p_part.split('=')[1].split(',')
                x = int(p_values[0])
                y = int(p_values[1])
            except (IndexError, ValueError):
                raise ValueError(f"Line {line_num}: Position format incorrect. Expected 'p=X,Y'.")
            
            # Validate initial positions are within grid
            if not (0 <= x < grid_width) or not (0 <= y < grid_height):
                raise ValueError(f"Line {line_num}: Position ({x}, {y}) out of grid bounds.")
            
            # Extract movement values
            try:
                v_values = v_part.split('=')[1].split(',')
                dx = int(v_values[0])
                dy = int(v_values[1])
            except (IndexError, ValueError):
                raise ValueError(f"Line {line_num}: Movement format incorrect. Expected 'v=DX,DY'.")
            
            # Append to respective lists
            positions_x.append(x)
            positions_y.append(y)
            movements_x.append(dx)
            movements_y.append(dy)
    
    # Convert lists to NumPy arrays with appropriate data types
    positions = np.vstack((
        np.array(positions_x, dtype=np.int32),
        np.array(positions_y, dtype=np.int32)
    )).T  # Shape (N, 2)
    
    movements = np.vstack((
        np.array(movements_x, dtype=np.int32),
        np.array(movements_y, dtype=np.int32)
    )).T  # Shape (N, 2)
    
    return positions, movements

def update_positions(positions, movements, grid_width, grid_height):
    """
    Updates the positions based on the movements and applies wrap-around.

    Parameters:
    - positions (np.ndarray): Current positions array of shape (N, 2).
    - movements (np.ndarray): Movements array of shape (N, 2).

    Returns:
    - None: The positions array is updated in place.
    """
    # Update positions with movements
    positions += movements
    
    # Apply wrap-around using modulo operation
    positions[:, 0] = positions[:, 0] % grid_width   # X-axis wrap-around
    positions[:, 1] = positions[:, 1] % grid_height  # Y-axis wrap-around


def calculate_movements(num_updates, positions, movements, grid_width, grid_height):
    
    for update_num in range(1, num_updates + 1):
        update_positions(positions, movements, grid_width, grid_height)
    
    return(positions)


def calculate_quandrant(final_pos, grid_width, grid_height):
    
    quadrant_1 = 0
    quadrant_2 = 0
    quadrant_3 = 0
    quadrant_4 = 0

    for y, x in final_pos:
        if (x >= 0 and x < math.floor(grid_height/2)) and (y >= 0 and y < math.floor(grid_width/2)):
            quadrant_1 += 1
        elif (x > math.floor(grid_height/2) and x <= grid_height) and (y >= 0 and y < math.floor(grid_width/2)):
            quadrant_2 += 1
        elif (x >= 0 and x < math.floor(grid_height/2)) and (y > math.floor(grid_width/2) and y <= grid_width):
            quadrant_3 += 1
        elif (x > math.floor(grid_height/2) and x <= grid_height) and (y > math.floor(grid_width/2) and y <= grid_width):
            quadrant_4 += 1
        
    return([quadrant_1, quadrant_2, quadrant_3, quadrant_4])



def solve_part1(input_file, num_updates, grid_width, grid_height):
    
    try:
        # Parse the input file
        positions, movements = parse_input(input_file, grid_width, grid_height)
    except Exception as e:
        print(f"Error parsing input file: {e}")
        return
    
    final_pos = calculate_movements(num_updates, positions, movements, grid_width, grid_height)
    part1_sol = math.prod(calculate_quandrant(final_pos, grid_width, grid_height))

    return(part1_sol)

start = timeit.default_timer()
part1_sol = solve_part1('day14/input.txt', 100, 101, 103)
elapsed_time = timeit.default_timer()-start
print(f'Day 14 Part 1 Solution = {part1_sol}')
print(f'Day 14 Part 1 Run Time = {str(elapsed_time)}')





## ----- PART 2 ----- ##

import sys
import time

W = 101
H = 103

ans = [0,0,0,0]

robots = []

st = 0
for line in open("day14/input.txt"):
    if line.strip() == "":
        continue
    p,v = line.split()
    px,py = map(int,p[2:].split(",")) 
    vx,vy = map(int,v[2:].split(","))
    robots.append(((px,py),(vx,vy)))

seconds = 0
while True:
    grid = [[0 for _ in range(W)] for _ in range(H)]
    seconds += 1

    bad = False
    for robot in robots:
        pr1,pr2 = robot
        px,py = pr1
        vx,vy = pr2
        nx,ny = px + seconds*vx, py + seconds*vy
        nx = nx % W
        ny = ny % H
        grid[ny][nx] += 1
        if grid[ny][nx] > 1:
            bad = True

    if not bad:
        print(seconds)
        # for row in grid:
        #     print("".join(map(str,row)))
        # time.sleep(0.3)
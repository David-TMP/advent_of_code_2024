from collections import deque
import timeit
import heapq


# ------------------------------------------------------
# 1. Define the keypad layouts as 2D grids
#    None represents a gap or invalid position.
# ------------------------------------------------------

NUMERIC_GRID = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']  # bottom row has a gap at [3][0]
]

DIRECTIONAL_GRID = [
    [None, '^', 'A'],  # row 0: gap, up, activate
    ['<', 'v', '>']    # row 1: left, down, right
]

# ------------------------------------------------------
# 2. Build a dictionary of button -> (row, col)
#    for quick coordinate lookups.
# ------------------------------------------------------

def create_keypad_map(keypad_grid):
    """
    Given a 2D grid of buttons (with None for gaps),
    return a dictionary mapping button_label -> (row, col).
    """
    keypad_map = {}
    for r, row in enumerate(keypad_grid):
        for c, val in enumerate(row):
            if val is not None:
                keypad_map[val] = (r, c)
    return keypad_map

NUMERIC_MAP = create_keypad_map(NUMERIC_GRID)
DIRECTIONAL_MAP = create_keypad_map(DIRECTIONAL_GRID)


# ------------------------------------------------------
# 3. Define the function to find the shortest path
# ------------------------------------------------------

def find_shortest_path(init, target_button, keypad_map, keypad_grid):
    """
    Finds the shortest sequence of directions to reach the target_button
    from the start position 'A' on the given keypad, penalizing changes in direction.

    Parameters:
    - target_button (str): The button to reach.
    - keypad_map (dict): Mapping from button to (row, col).
    - keypad_grid (list of lists): The keypad layout.

    Returns:
    - str: The sequence of directions ('^', 'v', '<', '>').
           Returns None if the target is unreachable.
    """
    if 'A' not in keypad_map:
        raise ValueError("Start position 'A' not found in the keypad.")

    if target_button not in keypad_map:
        raise ValueError(f"Target button '{target_button}' not found in the keypad.")

    # Define possible directions with their corresponding row and column changes
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    start_pos = keypad_map[init]
    target_pos = keypad_map[target_button]

    # Priority queue: (number_of_changes, path_length, current_position, path_taken, last_direction)
    heap = []
    heapq.heappush(heap, (0, 0, start_pos, [], None))

    # Visited dictionary to keep track of the minimum number of changes to reach a position
    visited = {}

    while heap:
        changes, path_len, current_pos, path, last_dir = heapq.heappop(heap)

        if current_pos == target_pos:
            return ''.join(path)  # Found the target

        if current_pos in visited:
            if changes > visited[current_pos]:
                continue
        visited[current_pos] = changes

        for direction, (dx, dy) in directions.items():
            new_row = current_pos[0] + dx
            new_col = current_pos[1] + dy
            new_pos = (new_row, new_col)

            # Check if the new position is within bounds and not a gap
            if (0 <= new_row < len(keypad_grid)) and (0 <= new_col < len(keypad_grid[0])):
                if keypad_grid[new_row][new_col] is not None:
                    # Calculate new number of changes
                    if last_dir is None or direction == last_dir:
                        new_changes = changes
                    else:
                        new_changes = changes + 1

                    # If this path to new_pos has fewer changes, proceed
                    if new_pos not in visited or new_changes < visited[new_pos]:
                        heapq.heappush(heap, (
                            new_changes,
                            path_len + 1,
                            new_pos,
                            path + [direction],
                            direction
                        ))

    # If the target is not reachable
    return None


test_code = 'A029A'


with open('day21/input.txt', 'r') as f:
    codes = [line.strip() for line in f.readlines()]

def solve_part1(codes):

    sol = 0

    for code in codes:
        code = 'A' + code
        a = ""
        b = ""
        c = ""
        for index in range(len(code)-1):
            a = a + find_shortest_path(code[index], code[index+1], NUMERIC_MAP, NUMERIC_GRID) + 'A'

        a = 'A' + a

        for index in range(len(a)-1):
            b = b + find_shortest_path(a[index], a[index+1], DIRECTIONAL_MAP, DIRECTIONAL_GRID) + 'A'

        b = 'A' + b

        for index in range(len(b)-1):
            c = c + find_shortest_path(b[index], b[index+1], DIRECTIONAL_MAP, DIRECTIONAL_GRID) + 'A'

        sol += len(c) * int(code.replace("A", ""))
    
    return(sol)

x = solve_part1(codes)
print(x)
    
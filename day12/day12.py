from collections import defaultdict
from collections import deque
import timeit

with open('day12/input.txt', 'r') as file:
    garden_map = [list(line.strip()) for line in file.readlines()]

rows = len(garden_map)
cols = len(garden_map[0])


## ----- PART 1 ----- ##

visited = [[False for _ in range(cols)] for _ in range(rows)]

def bfs_part1(start_row, start_col, plant_type):
    queue = deque()
    queue.append((start_row, start_col))
    visited[start_row][start_col] = True
    area = 0
    perimeter = 0
    
    while queue:
        row, col = queue.popleft()
        area += 1
        
        # Directions: up, down, left, right
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            if r < 0 or r >= rows or c < 0 or c >= cols:  # map edge
                perimeter += 1
            elif garden_map[r][c] != plant_type:  # region border
                perimeter += 1
            elif not visited[r][c]:  # New plant in the region
                visited[r][c] = True
                queue.append((r, c))
    
    return area, perimeter

def solve_part1():
    regions = []
    for row in range(rows):
        for col in range(cols):
            if not visited[row][col]:
                plant_type = garden_map[row][col]
                area, perimeter = bfs_part1(row, col, plant_type)
                regions.append((plant_type, area, perimeter))
    
    total_cost = sum(area * perimeter for _, area, perimeter in regions)
    
    return(total_cost)

start = timeit.default_timer()
part1_sol = solve_part1()
elapsed_time = timeit.default_timer()-start
print(f'Day 12 Part 1 Solution = {part1_sol}')
print(f'Day 12 Part 1 Run Time = {str(elapsed_time)}')



## ----- PART 2 ----- ##

def delete_adjacent_duplicates(input_set):
    """
    Removes adjacent elements with the same dir_x and dir_y from the input_set.
    Adjacent means elements are next to each other in the same row or column.
    Keeps only one element per group of adjacent duplicates.
    
    Parameters:
    input_set (set of tuples): Each tuple is (row, column, dir_x, dir_y)
    
    Returns:
    set of tuples: The set after removing adjacent duplicates
    """
    
    # Group elements by (dir_x, dir_y)
    direction_groups = defaultdict(set)
    for elem in input_set:
        key = (elem[2], elem[3])  # (dir_x, dir_y)
        direction_groups[key].add((elem[0], elem[1]))  # (row, column)
    
    # Function to find connected components using Union-Find
    def find_connected_components(elements):
        parent = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_y] = root_x
        
        # Initialize parent pointers
        for elem in elements:
            parent[elem] = elem
        
        # Build connections
        element_set = set(elements)
        for (row, col) in elements:
            # Check adjacent positions
            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1)
            ]
            for neighbor in neighbors:
                if neighbor in element_set:
                    union((row, col), neighbor)
        
        # Group elements by their root parent
        components = defaultdict(set)
        for elem in elements:
            root = find(elem)
            components[root].add(elem)
        
        return components.values()
    
    # Set to keep the elements after removal
    elements_to_keep = set()
    
    # Process each direction group
    for direction, elements in direction_groups.items():
        connected_components = find_connected_components(elements)
        for component in connected_components:
            # Keep one element from each component
            element_to_keep = next(iter(component))
            elements_to_keep.add((element_to_keep[0], element_to_keep[1], direction[0], direction[1]))
    
    return elements_to_keep

visited = [[False for _ in range(cols)] for _ in range(rows)]

def bfs_part2(start_row, start_col, plant_type):
    queue = deque()
    queue.append((start_row, start_col))
    visited[start_row][start_col] = True
    area = 0
    n_sides = 0
    visited_sides = set()
    
    while queue:
        row, col = queue.popleft()
        area += 1
        
        # Directions: up, down, left, right
        for dr, dc in [(-1,0), (0,1), (1,0), (0,-1)]:
            r, c = row + dr, col + dc
            if (r < 0 or r >= rows or c < 0 or c >= cols) or (garden_map[r][c] != plant_type):
                visited_sides.add((r, c, dr, dc))
                # if (r-1, c, dr, dc) not in visited_sides and (r+1, c, dr, dc) not in visited_sides and (r, c-1, dr, dc) not in visited_sides and (r, c+1, dr, dc) not in visited_sides:
                    # print(f'WE ARE IN {garden_map[row][col]} AT POSITION {row, col} LOOKING IN DIR {dr, dc}')
                    # n_sides += 1
            elif not visited[r][c]:  # New plant in the region
                visited[r][c] = True
                queue.append((r, c))
    
    x = delete_adjacent_duplicates(visited_sides)
    n_sides = len(x)

    return area, n_sides

def solve_part2():
    regions = []
    for row in range(rows):
        for col in range(cols):
            if not visited[row][col]:
                plant_type = garden_map[row][col]
                area, n_sides = bfs_part2(row, col, plant_type)
                regions.append((plant_type, area, n_sides))

    total_cost = sum(area * n_sides for _, area, n_sides in regions)
    
    return(total_cost)

start = timeit.default_timer()
part2_sol = solve_part2()
elapsed_time = timeit.default_timer()-start
print(f'Day 12 Part 2 Solution = {part2_sol}')
print(f'Day 12 Part 2 Run Time = {str(elapsed_time)}')

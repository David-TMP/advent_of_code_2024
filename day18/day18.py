import timeit
import heapq

file_path = 'day18/input.txt'

def read_positions(file_path):
    positions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            x, y = int(parts[0]), int(parts[1])
            positions.append((x, y))

    return(positions)

def draw_memory_space(positions, X_dim, Y_dim):
    grid = [["."] * X_dim for _ in range(Y_dim)]
    return(grid)

def add_corrupted_coordinates(memory_space, positions, num_bytes):
    for i in range(num_bytes):
        memory_space[positions[i][0]][positions[i][1]] = '#'
    return(memory_space)


## ----- PART 1 ----- ##

def solve_part1(maze, start, end):

    # Directions: 0=North, 1=East, 2=South, 3=West
    # We start facing East
    start_dir = 1

    # Movement offsets for forward steps
    # Order corresponds to directions: N, E, S, W
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    rows = len(maze)
    cols = len(maze[0])

    # dist[x][y][dir] = best known cost to reach (x,y) with direction dir
    # Initialize with None or large values
    dist = [[[None for _ in range(4)] for _ in range(cols)] for _ in range(rows)]
    dist[start[0]][start[1]][start_dir] = 0

    # Priority queue: (cost, x, y, dir)
    pq = []
    heapq.heappush(pq, (0, start[0], start[1], start_dir))

    while pq:
        cost, x, y, d = heapq.heappop(pq)

        # If this is not the best known distance, skip
        if dist[x][y][d] != cost:
            continue

        # If we reached the end, return the cost
        if (x, y) == end:
            return cost

        # 1) Try to move forward
        dx, dy = moves[d]
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#':
            ncost = cost + 1
            if dist[nx][ny][d] is None or ncost < dist[nx][ny][d]:
                dist[nx][ny][d] = ncost
                heapq.heappush(pq, (ncost, nx, ny, d))

        # 2) Turn left (d-1 mod 4)
        ld = (d - 1) % 4
        lcost = cost + 0
        if dist[x][y][ld] is None or lcost < dist[x][y][ld]:
            dist[x][y][ld] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # 3) Turn right (d+1 mod 4)
        rd = (d + 1) % 4
        rcost = cost + 0
        if dist[x][y][rd] is None or rcost < dist[x][y][rd]:
            dist[x][y][rd] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # If we exhaust the queue without reaching E, something's wrong
    return None

positions = read_positions(file_path=file_path)
original_memory_space = draw_memory_space(positions, 71, 71)
corrupted_memory_space = add_corrupted_coordinates(memory_space=original_memory_space, positions=positions, num_bytes=1024)

start = timeit.default_timer()
part1_sol = solve_part1(corrupted_memory_space, (0,0),  (70,70))
elapsed_time = timeit.default_timer()-start
print(f'Day 18 Part 1 Solution = {part1_sol}')
print(f'Day 18 Part 1 Run Time = {str(elapsed_time)}')


##  ----- PART 2 ----- ##

def  solve_part2(corrupted_memory_space, positions):
    for i in  range(1024, len(positions)):
        corrupted_memory_space[positions[i][0]][positions[i][1]] = '#'
        if solve_part1(corrupted_memory_space, (0,0),  (70,70)) == None:
            return(positions[i])

start = timeit.default_timer()
part2_sol = solve_part2(original_memory_space, positions)
elapsed_time = timeit.default_timer()-start
print(f'Day 18 Part 2 Solution = {part2_sol}')
print(f'Day 18 Part 2 Run Time = {str(elapsed_time)}')
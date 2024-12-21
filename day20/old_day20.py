

import heapq
import timeit

with open("day20/input.txt", "r") as f:
    maze = [list(line.strip()) for line in f.readlines()]


## ----- PART 1 ----- ##

def solve_part1(maze):
    # Maze is a list of strings
    # Find start (S) and end (E) positions
    start = None
    end = None

    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                start = (i, j)
            elif ch == 'E':
                end = (i, j)

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

start = timeit.default_timer()
part1_sol = solve_part1(maze)
elapsed_time = timeit.default_timer()-start
print(f'Day 20 Part 1 Solution = {part1_sol}')
print(f'Day 20 Part 1 Run Time = {str(elapsed_time)}')

contador = 0
original_cost = solve_part1(maze)

sol_part1 = 0

start = timeit.default_timer()

for i in range(1, len(maze)-1):
    for j in range(1, len(maze[0])-1):
        if maze[i+1][j] == '#':
            contador += 1
        if maze[i-1][j] == '#':
            contador += 1
        if maze[i][j+1] == '#':
            contador += 1
        if maze[i][j-1] == '#':
            contador += 1
        if maze[i][j] == '#' and contador < 3:
            maze[i][j] = '.'
            cost = solve_part1(maze)
            if cost <= original_cost-100:
                sol_part1 += 1
            maze[i][j] = '#'
        contador = 0

elapsed_time = timeit.default_timer()-start

print(f'Day 20 Part 1 Run Time = {str(elapsed_time)}')
print(sol_part1)
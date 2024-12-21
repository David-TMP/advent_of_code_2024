from collections import deque
import sys
import timeit

with open("day20/input.txt", "r") as f:
    maze = [list(line.strip()) for line in f.readlines()]

rows = len(maze)
cols = len(maze[0])

def find_positions(maze):
    start = end = None
    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                start = (i, j)
            elif ch == 'E':
                end = (i, j)
    return start, end

start, end = find_positions(maze)

# Directions
dirs = [(-1,0),(1,0),(0,1),(0,-1)]

def valid(x,y):
    return 0 <= x < rows and 0 <= y < cols

def bfs_normal(start_pos):
    """ BFS for shortest distance with walls blocking. """
    dist = [[sys.maxsize]*cols for _ in range(rows)]
    dist[start_pos[0]][start_pos[1]] = 0
    q = deque([start_pos])
    while q:
        x,y = q.popleft()
        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if valid(nx,ny) and maze[nx][ny] != '#' and dist[nx][ny] == sys.maxsize:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx,ny))
    return dist

# Precompute distances from S and to E
dist_from_S = bfs_normal(start)
dist_to_E = bfs_normal(end)

base_cost = dist_from_S[end[0]][end[1]]

if base_cost == sys.maxsize:
    # No path at all
    print("No path found from S to E under normal conditions.")
    sys.exit()


def bfs_ignore_walls_limited(start_x, start_y, limit):
    """
    BFS ignoring walls, but only up to `limit` steps.
    Returns a dictionary of { (x,y): steps } for reachable cells within `limit`.
    """
    dist = [[sys.maxsize]*cols for _ in range(rows)]
    dist[start_x][start_y] = 0
    q = deque([(start_x,start_y)])
    reachable = {}
    while q:
        x,y = q.popleft()
        d = dist[x][y]
        if d <= limit:
            reachable[(x,y)] = d
        if d == limit:
            continue
        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if valid(nx,ny) and dist[nx][ny] == sys.maxsize:
                # Ignore walls during cheat
                dist[nx][ny] = d+1
                q.append((nx,ny))
    return reachable

# We will consider all track cells as potential start/end of cheat.
track_cells = [(i,j) for i in range(rows) for j in range(cols) if maze[i][j] != '#' and dist_from_S[i][j] != sys.maxsize and dist_to_E[i][j] != sys.maxsize]

def solve_day20(count_saving_100, C):
    for A in track_cells:
        Ax, Ay = A
        # Find all cells reachable from A within C steps ignoring walls
        reachable_cells = bfs_ignore_walls_limited(Ax, Ay, C)
        for B, cheat_cost in reachable_cells.items():
            Bx, By = B
            # Must end cheat on a track cell (which we ensured by B in reachable_cells)
            # Check that we don't break normal movement conditions:
            if dist_from_S[Ax][Ay] == sys.maxsize or dist_to_E[Bx][By] == sys.maxsize:
                continue
            if cheat_cost > 0:  # A != B or we consider starting and ending at the same cell?
                # Calculate time saved
                # Normal route: base_cost
                # Cheat route: dist_from_S[A] + cheat_cost(A,B) + dist_to_E[B]
                cheat_route_cost = dist_from_S[Ax][Ay] + cheat_cost + dist_to_E[Bx][By]
                time_saved = base_cost - cheat_route_cost
                if time_saved >= 100:
                    count_saving_100 += 1
    return(count_saving_100)


## ----- PART 1 ----- ##
start = timeit.default_timer()
part1_sol = solve_day20(0, 2)
elapsed_time = timeit.default_timer()-start
print(f'Day 20 Part 1 Solution = {part1_sol}')
print(f'Day 20 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ## 
start = timeit.default_timer()
part2_sol = solve_day20(0, 20)
elapsed_time = timeit.default_timer()-start
print(f'Day 20 Part 2 Solution = {part2_sol}')
print(f'Day 20 Part 2 Run Time = {str(elapsed_time)}')
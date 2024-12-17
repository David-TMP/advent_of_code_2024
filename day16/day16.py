import heapq
import timeit

with open("day16/input.txt", "r") as f:
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
        lcost = cost + 1000
        if dist[x][y][ld] is None or lcost < dist[x][y][ld]:
            dist[x][y][ld] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # 3) Turn right (d+1 mod 4)
        rd = (d + 1) % 4
        rcost = cost + 1000
        if dist[x][y][rd] is None or rcost < dist[x][y][rd]:
            dist[x][y][rd] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # If we exhaust the queue without reaching E, something's wrong
    return None

start = timeit.default_timer()
part1_sol = solve_part1(maze)
elapsed_time = timeit.default_timer()-start
print(f'Day 16 Part 1 Solution = {part1_sol}')
print(f'Day 16 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

def solve_part2(maze):
    start = None
    end = None
    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                start = (i, j)
            elif ch == 'E':
                end = (i, j)

    # Directions: 0=North, 1=East, 2=South, 3=West
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    start_dir = 1  # facing East

    rows, cols = len(maze), len(maze[0])
    dist = [[[None]*4 for _ in range(cols)] for _ in range(rows)]
    dist[start[0]][start[1]][start_dir] = 0
    pq = [(0, start[0], start[1], start_dir)]
    heapq.heapify(pq)

    while pq:
        cost, x, y, d = heapq.heappop(pq)
        if dist[x][y][d] != cost:
            continue
        if (x, y) == end:
            # First time we pop end from PQ = minimal cost
            min_end_cost = cost
            break

        # Move forward
        dx, dy = moves[d]
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#':
            ncost = cost + 1
            if dist[nx][ny][d] is None or ncost < dist[nx][ny][d]:
                dist[nx][ny][d] = ncost
                heapq.heappush(pq, (ncost, nx, ny, d))

        # Turn left
        ld = (d - 1) % 4
        lcost = cost + 1000
        if dist[x][y][ld] is None or lcost < dist[x][y][ld]:
            dist[x][y][ld] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # Turn right
        rd = (d + 1) % 4
        rcost = cost + 1000
        if dist[x][y][rd] is None or rcost < dist[x][y][rd]:
            dist[x][y][rd] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # min_end_cost is now known. Find all directions from end that achieve this cost:
    end_states = []
    for d in range(4):
        if dist[end[0]][end[1]][d] == min_end_cost:
            end_states.append((end[0], end[1], d))

    # Backtrack to find all tiles in best paths
    in_best_path = set()
    visited_back = set()
    from collections import deque
    queue = deque(end_states)

    while queue:
        x, y, d = queue.popleft()
        if (x, y, d) in visited_back:
            continue
        visited_back.add((x, y, d))

        # Mark tile as part of best path
        in_best_path.add((x, y))

        # Check forward predecessor:
        dx, dy = moves[d]
        px, py = x - dx, y - dy
        if 0 <= px < rows and 0 <= py < cols and dist[px][py][d] is not None:
            # Forward came with cost +1
            if dist[x][y][d] == dist[px][py][d] + 1:
                queue.append((px, py, d))

        # Check turn predecessors:
        # Turn left means previous direction was (d+1)%4
        d_left_from = (d + 1) % 4
        if dist[x][y][d] is not None and dist[x][y][d_left_from] is not None:
            if dist[x][y][d] == dist[x][y][d_left_from] + 1000:
                queue.append((x, y, d_left_from))

        # Turn right means previous direction was (d-1)%4
        d_right_from = (d - 1) % 4
        if dist[x][y][d] is not None and dist[x][y][d_right_from] is not None:
            if dist[x][y][d] == dist[x][y][d_right_from] + 1000:
                queue.append((x, y, d_right_from))

    return min_end_cost, len(in_best_path)

start = timeit.default_timer()
part2_sol = solve_part2(maze)
elapsed_time = timeit.default_timer()-start
print(f'Day 16 Part 2 Solution = {part2_sol}')
print(f'Day 16 Part 2 Run Time = {str(elapsed_time)}')
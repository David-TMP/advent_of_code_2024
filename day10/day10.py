def solve_part1():

    # Read all lines from stdin (the input map)
    with open("day10/input_test.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print(0)
            return
    
    grid = [list(map(int, list(row))) for row in lines]
    rows = len(grid)
    cols = len(grid[0])
    
    # Directions for neighbors (up, down, left, right)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    
    # Identify all cells with height 9
    nine_positions = []
    nine_id_map = {}  # Map from (r,c) to an ID for each 9-cell
    nine_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 9:
                nine_positions.append((r,c))
                nine_id_map[(r,c)] = nine_count
                nine_count += 1
    
    # If there are no 9's, the score is 0
    if nine_count == 0:
        print(0)
        return
    
    # DP array: For each cell, store a set of reachable 9-cell IDs
    # Initialize for height 9 cells: each can reach only itself
    reachable_from = [[set() for _ in range(cols)] for _ in range(rows)]
    for (r,c) in nine_positions:
        reachable_from[r][c].add(nine_id_map[(r,c)])


    # Process heights from 8 down to 0
    for h in range(8, -1, -1):
        # For each cell of height h, gather reachable sets from neighbors of height h+1
        # We can do this in a second pass to avoid immediate overwrite issues.
        
        # Actually, we don't overwrite reachable sets for higher height cells, we only read them.
        # But to be safe and possibly more memory friendly, we just compute on the fly.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == h:
                    # Combine sets from neighbors of height h+1
                    combined = set()
                    for dr, dc in directions:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == h+1:
                            combined |= reachable_from[nr][nc]
                    
                    # Store combined set
                    reachable_from[r][c] = combined

    # Now, all cells of height 0 are trailheads. Sum up the scores (the size of reachable set)
    total_score = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total_score += len(reachable_from[r][c])

    print(total_score)


solve_part1()


def solve_part2():
    
    with open("day10/input.txt", "r") as f:    
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print(0)
            return
        
    grid = [list(map(int, list(row))) for row in lines]
    rows = len(grid)
    cols = len(grid[0])
    
    # Directions for neighbors (up, down, left, right)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    
    # Initialize path_count array
    # path_count[r][c]: number of distinct paths from (r,c) to any cell of height 9
    path_count = [[0]*(cols) for _ in range(rows)]
    
    # For height 9 cells, path_count = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 9:
                path_count[r][c] = 1
    
    # Process from height 8 down to 0
    for h in range(8, -1, -1):
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == h:
                    # Sum path counts from neighbors with height h+1
                    total_paths = 0
                    for dr, dc in directions:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == h+1:
                            total_paths += path_count[nr][nc]
                    path_count[r][c] = total_paths
    
    # Now sum path_count for all trailheads (cells of height 0)
    total_rating = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total_rating += path_count[r][c]
    
    print(total_rating)


solve_part2()


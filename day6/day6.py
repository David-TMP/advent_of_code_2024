import copy

# Reading the file content from input.txt in the day6 folder
with open("day6/input.txt", "r") as file:
    file_content = file.read()

# Splitting the content into rows, then converting each row into a list of characters
grid = [list(line) for line in file_content.strip().split("\n")]


## ----- PART 1 ----- ## 

# direction (0=up, 1=right, 2=down, 3=left)   

def find_guard(grid):
    position = ()
    for row_index, row in enumerate(grid):
        try:
            col_index = row.index("^")
            position = (row_index, col_index)
        except ValueError:
            continue
    return(position)

starting_pos = find_guard(grid = grid)
print(starting_pos)
grid[starting_pos[0]][starting_pos[1]] = "."
visited_pos = set()


def find_path(solution_found, new_pos, dir, contador):
    while(solution_found != True):
        if (new_pos, "up") in visited_pos or (new_pos, "down") in visited_pos or (new_pos, "right") in visited_pos or (new_pos, "left") in visited_pos:
             contador -= 1
        if (new_pos, dir) in visited_pos:
            n_loops_found += 1
            print(contador)
            break
        if ((dir == "left" and new_pos[1] == 0) or (dir == "right" and new_pos[1] == len(grid)-1) or (dir == "up" and new_pos[0] == 0) or (dir == "down" and new_pos[0] == len(grid)-1)):
            solution_found = True
            print(contador)
            break
        if dir == "up":
            if grid[new_pos[0]-1][new_pos[1]] == ".":
                visited_pos.add(((new_pos[0], new_pos[1]), dir))
                new_pos = (new_pos[0]-1, new_pos[1])
                print(new_pos)
                contador += 1
                continue
        if dir == "up":
            if grid[new_pos[0]-1][new_pos[1]] == "#":
                dir = "right"
                continue
        if dir == "right":
                if grid[new_pos[0]][new_pos[1]+1] == ".":
                    visited_pos.add(((new_pos[0], new_pos[1]), dir))
                    new_pos = new_pos[0], new_pos[1]+1
                    print(new_pos)
                    contador += 1
                    continue
        if dir == "right":
                if grid[new_pos[0]][new_pos[1]+1] == "#":
                    dir = "down"
                    continue
        if dir == "down":
                if grid[new_pos[0]+1][new_pos[1]] == ".":
                    visited_pos.add(((new_pos[0], new_pos[1]), dir))
                    new_pos = new_pos[0]+1, new_pos[1]
                    print(new_pos)
                    contador += 1
                    continue
        if dir == "down":
                if grid[new_pos[0]+1][new_pos[1]] == "#":
                    dir = "left"
                    continue
        if dir == "left":
                if grid[new_pos[0]][new_pos[1]-1] == ".":
                    visited_pos.add(((new_pos[0], new_pos[1]), dir))
                    new_pos = new_pos[0], new_pos[1]-1
                    print(new_pos)
                    contador += 1
                    continue
        if dir == "left":
                if grid[new_pos[0]][new_pos[1]-1] == "#":
                    dir = "up"
                    continue
    return(n_loops_found)

# find_path(solution_found = False, new_pos = starting_pos, dir = "up", contador = 1)


## ----- PART 2 ----- ##


def all_pos(solution_found, new_pos, dir, contador):
    while(solution_found != True):
        if ((new_pos[0], new_pos[1], 0) in visited_pos or (new_pos[0], new_pos[1], 2) in visited_pos or (new_pos[0], new_pos[1], 1) in visited_pos or (new_pos[0], new_pos[1], 3) in visited_pos):
             contador -= 1
        if (new_pos[0], new_pos[1], dir) in visited_pos:
            break
        if ((dir == 3 and new_pos[1] == 0) or (dir == 1 and new_pos[1] == len(grid)-1) or (dir == 0 and new_pos[0] == 0) or (dir == 2 and new_pos[0] == len(grid)-1)):
            solution_found = True
            print(contador)
            break
        if dir == 0:
            if grid[new_pos[0]-1][new_pos[1]] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                new_pos = (new_pos[0]-1, new_pos[1])
                contador += 1
                continue
        if dir == 0:
            if grid[new_pos[0]-1][new_pos[1]] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 1:
            if grid[new_pos[0]][new_pos[1]+1] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                new_pos = new_pos[0], new_pos[1]+1
                contador += 1
                continue
        if dir == 1:
            if grid[new_pos[0]][new_pos[1]+1] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 2:
            if grid[new_pos[0]+1][new_pos[1]] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                new_pos = new_pos[0]+1, new_pos[1]
                contador += 1
                continue
        if dir == 2:
            if grid[new_pos[0]+1][new_pos[1]] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 3:
            if grid[new_pos[0]][new_pos[1]-1] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                new_pos = new_pos[0], new_pos[1]-1
                contador += 1
                continue
        if dir == 3:
            if grid[new_pos[0]][new_pos[1]-1] == "#":
                dir = (dir + 1) % 4
                continue
    return(visited_pos)


x = all_pos(solution_found = False, new_pos = starting_pos, dir = 0, contador = 1)


def find_path_v2(grid, solution_found, new_pos, prev_pos, dir, contador, visited_pos):
    while(solution_found != True):
        if (new_pos[0], new_pos[1], 0) in visited_pos or (new_pos[0], new_pos[1], 2) in visited_pos or (new_pos[0], new_pos[1], 1) in visited_pos or (new_pos[0], new_pos[1], 3) in visited_pos:
             contador -= 1
        if (new_pos[0], new_pos[1], dir) in visited_pos:
            loop_found = True
            return(loop_found)
        if ((dir == 3 and new_pos[1] == 0) or (dir == 1 and new_pos[1] == len(grid)-1) or (dir == 0 and new_pos[0] == 0) or (dir == 2 and new_pos[0] == len(grid)-1)):
            solution_found = True
            # print(contador)
            break
        if dir == 0:
            if grid[new_pos[0]-1][new_pos[1]] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                prev_pos = (new_pos[0], new_pos[1])
                new_pos = (new_pos[0]-1, new_pos[1])
                contador += 1
                continue
        if dir == 0:
            if grid[new_pos[0]-1][new_pos[1]] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 1:
            if grid[new_pos[0]][new_pos[1]+1] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                prev_pos = (new_pos[0], new_pos[1])
                new_pos = new_pos[0], new_pos[1]+1
                contador += 1
                continue
        if dir == 1:
            if grid[new_pos[0]][new_pos[1]+1] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 2:
            if grid[new_pos[0]+1][new_pos[1]] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                prev_pos = (new_pos[0], new_pos[1])
                new_pos = new_pos[0]+1, new_pos[1]
                contador += 1
                continue
        if dir == 2:
            if grid[new_pos[0]+1][new_pos[1]] == "#":
                dir = (dir + 1) % 4
                continue
        if dir == 3:
            if grid[new_pos[0]][new_pos[1]-1] == ".":
                visited_pos.add((new_pos[0], new_pos[1], dir))
                prev_pos = (new_pos[0], new_pos[1])
                new_pos = new_pos[0], new_pos[1]-1
                contador += 1
                continue
        if dir == 3:
            if grid[new_pos[0]][new_pos[1]-1] == "#":
                dir = (dir + 1) % 4
                continue
    return(False)


n_loops_found = 0

def modify_grid(grid, pos):
    new_grid = copy.deepcopy(grid)  # creates a completely independent copy
    new_grid[pos[0]][pos[1]] = "#"
    return(new_grid)

# We're going to check if by placing an obstacle in one of the visited cells will create an infinite loop
def check_paths(grid, all_pos):
    n_loops_found = 0
    unique_positions = [(r, c) for (r, c, d) in all_pos]
    for i in unique_positions:
        modified_grid = modify_grid(grid, i)
        if (find_path_v2(grid = modified_grid, solution_found = False, new_pos = starting_pos, prev_pos = starting_pos, dir = 0, contador = 1, visited_pos = set())):
            n_loops_found += 1
    return(n_loops_found)

part_2_sol = check_paths(grid = grid, all_pos = x)
print(part_2_sol)


# find_path_v2(grid = grid, solution_found = False, new_pos = starting_pos, prev_pos = starting_pos, dir = 0, contador = 1)
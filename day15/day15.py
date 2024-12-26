import timeit

def read_input(file_path):

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    # Split the input into grid and commands based on the empty line
    try:
        empty_line_index = lines.index('')
    except ValueError:
        raise ValueError("Input file does not contain an empty line separating grid and commands.")

    # Parse the grid into a 2D list
    grid = [list(line) for line in lines[:empty_line_index]]

    # Concatenate all command lines into a single string
    commands = ''.join(lines[empty_line_index + 1:])

    return grid, commands

grid, commands = read_input('day15/input.txt')

def find_robot(grid):
    for row in range(len(grid[0])):
        for col in range(len(grid)):
            if grid[row][col] == "@":
                return [row, col]
            
robot_pos = find_robot(grid)

def find_walls(sub_grid, move):
    if move == '<' or move == '^':
        for i in reversed(range(len(sub_grid))):
            if sub_grid[i] == ".":
                if move == "<":
                    return i
                elif move == "^":
                    return abs(i-len(sub_grid))
            elif sub_grid[i] == "#":
                return -1
    else:
        for x, element in enumerate(sub_grid):
            if element == ".":
                return x
            elif element == "#":
                return -1

def move_robot(grid, commands, robot_pos):
    for index, move in enumerate(commands):
        if move == "^":
            sub_list = [grid[y][robot_pos[1]] for y in range(0, robot_pos[0])]
            x = find_walls(sub_list, move)
            if x == -1:
                continue
            else:
                grid[robot_pos[0]][robot_pos[1]] = "."
                grid[robot_pos[0]-1][robot_pos[1]] = "@"
                while x > 1:
                    grid[robot_pos[0]-x][robot_pos[1]] = "O"
                    x -= 1 
                robot_pos[0] -= 1 
        elif move == "v":
            sub_list = [grid[y][robot_pos[1]] for y in range(robot_pos[0]+1, len(grid[0]))]
            x = find_walls(sub_list, move)
            if x == -1:
                continue
            else:
                grid[robot_pos[0]][robot_pos[1]] = "."
                grid[robot_pos[0]+1][robot_pos[1]] = "@"
                while x > 0:
                    grid[robot_pos[0]+1+x][robot_pos[1]] = "O"
                    x -= 1          
                robot_pos[0] += 1
        elif move == "<":
            sub_list = [grid[robot_pos[0]][x] for x in range(0, robot_pos[1])]
            x = find_walls(sub_list, move)
            if x == -1:
                continue
            else:
                grid[robot_pos[0]].pop(x)
                grid[robot_pos[0]].insert(robot_pos[1], ".")
                robot_pos[1] -= 1
        elif move == ">":
            sub_list = [grid[robot_pos[0]][x] for x in range(robot_pos[1]+1, len(grid))]
            x = find_walls(sub_list, move)
            if x == -1:
                continue
            else:
                grid[robot_pos[0]].pop(x+robot_pos[1]+1)
                grid[robot_pos[0]].insert(robot_pos[1], ".")
                robot_pos[1] += 1
    return(grid)

def solve_part1(final_grid):
    return sum([y * 100 + x for y in range(len(final_grid)) for x in range(len(final_grid[0])) if final_grid[y][x] == "O"])


start = timeit.default_timer()
final_grid = move_robot(grid, commands, robot_pos)
part1_sol = solve_part1(final_grid)
elapsed_time = timeit.default_timer()-start
print(f'Day 15 Part 1 Solution = {part1_sol}')
print(f'Day 15 Part 1 Run Time = {str(elapsed_time)}')
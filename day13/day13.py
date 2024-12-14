import sympy as sp
import re
import timeit

def parse_input(file_path):
    """
    Parses the input file and extracts systems of equations.

    Each system consists of:
    - Button A: X+<a1>, Y+<a2>
    - Button B: X+<b1>, Y+<b2>
    - Prize: X=<px>, Y=<py>
    
    Returns a list of dictionaries with coefficients and prize values.
    """
    systems = []
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into blocks separated by two or more newlines
    blocks = re.split(r'\n\s*\n', content.strip())
    
    for block in blocks:
        # Initialize a dictionary to hold coefficients and prize
        system = {}
        
        # Extract Button A coefficients
        button_a_match = re.search(r'Button A:\s*X\+(\d+),\s*Y\+(\d+)', block, re.IGNORECASE)
        if button_a_match:
            system['A_X'] = int(button_a_match.group(1))
            system['A_Y'] = int(button_a_match.group(2))
        else:
            print("Error: Button A coefficients not found in block:\n", block)
            continue  # Skip to next block
        
        # Extract Button B coefficients
        button_b_match = re.search(r'Button B:\s*X\+(\d+),\s*Y\+(\d+)', block, re.IGNORECASE)
        if button_b_match:
            system['B_X'] = int(button_b_match.group(1))
            system['B_Y'] = int(button_b_match.group(2))
        else:
            print("Error: Button B coefficients not found in block:\n", block)
            continue  # Skip to next block
        
        # Extract Prize values
        prize_x_match = re.search(r'Prize:\s*X=(\d+),\s*Y=(\d+)', block, re.IGNORECASE)
        if prize_x_match:
            system['Prize_X'] = int(prize_x_match.group(1))
            system['Prize_Y'] = int(prize_x_match.group(2))
        else:
            print("Error: Prize values not found in block:\n", block)
            continue  # Skip to next block
        
        systems.append(system)
    
    return systems


## ----- PART 2 ----- ##

def solve_system(A_X, B_X, Prize_X, A_Y, B_Y, Prize_Y):
    """
    Solves the system of equations:
    A_X * A + B_X * B = Prize_X
    A_Y * A + B_Y * B = Prize_Y
    
    Returns a tuple (A, B) if solutions exist, otherwise None.
    """
    A, B = sp.symbols('A B')
    
    # Define the equations
    eq1 = A_X * A + B_X * B - Prize_X
    eq2 = A_Y * A + B_Y * B - Prize_Y
    
    # Solve the system
    solution = sp.solve((eq1, eq2), (A, B), dict=True)
    
    if solution:
        # Extract solutions
        sol = solution[0]
        A_val = sol[A]
        B_val = sol[B]
        
        # Check if solutions are integers
        if A_val.is_Integer and B_val.is_Integer:
            return (int(A_val), int(B_val))
        else:
            return None
    else:
        return None

def solve_part1():
    input_file = 'day13/input.txt'
    systems = parse_input(input_file)
    tokens_spent = 0
    
    if not systems:
        print("No valid systems of equations found in the input file.")
        return
        
    for system in systems:
        A_X = system['A_X']
        B_X = system['B_X']
        Prize_X = system['Prize_X']
        A_Y = system['A_Y']
        B_Y = system['B_Y']
        Prize_Y = system['Prize_Y']
        
        solution = solve_system(A_X, B_X, Prize_X, A_Y, B_Y, Prize_Y)

        if solution:
            A_sol, B_sol = solution
            tokens_spent += 3*A_sol + 1*B_sol
    
    return(tokens_spent)

start = timeit.default_timer()
part1_sol = solve_part1()
elapsed_time = timeit.default_timer()-start
print(f'Day 13 Part 1 Solution = {part1_sol}')
print(f'Day 13 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

def solve_part2():
    input_file = 'day13/input.txt'
    systems = parse_input(input_file)
    tokens_spent = 0
    
    if not systems:
        print("No valid systems of equations found in the input file.")
        return
        
    for system in systems:
        A_X = system['A_X']
        B_X = system['B_X']
        Prize_X = system['Prize_X'] + 10000000000000
        A_Y = system['A_Y']
        B_Y = system['B_Y']
        Prize_Y = system['Prize_Y'] + 10000000000000
        
        solution = solve_system(A_X, B_X, Prize_X, A_Y, B_Y, Prize_Y)

        if solution:
            A_sol, B_sol = solution
            tokens_spent += 3*A_sol + 1*B_sol

    return(tokens_spent)

start = timeit.default_timer()
part2_sol = solve_part2()
elapsed_time = timeit.default_timer()-start
print(f'Day 13 Part 2 Solution = {part2_sol}')
print(f'Day 13 Part 2 Run Time = {str(elapsed_time)}')
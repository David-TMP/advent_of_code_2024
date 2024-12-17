import timeit

input_file = 'day17/input.txt'

def parse_input(file_path):
    registers = {}
    program = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if line.startswith("Register"):
                # Example line: "Register A: 729"
                parts = line.split(":")
                if len(parts) == 2:
                    reg_name = parts[0].split()[1]  # Get the register name (e.g., 'A')
                    reg_value = int(parts[1].strip())  # Get the register value as integer
                    registers[reg_name] = reg_value
            elif line.startswith("Program"):
                # Example line: "Program: 0,1,5,4,3,0"
                parts = line.split(":")
                if len(parts) == 2:
                    program = [int(x.strip()) for x in parts[1].split(",")]
    
    return registers, program

registers, program = parse_input(input_file)


## ----- PART 1 ----- ##


def get_combo_operand(registers, operand):
    if operand in[0,1,2,3]:
        return operand
    elif operand == 4:
        return registers.get('A')
    elif operand == 5:
        return registers.get('B')
    elif operand == 6:
        return registers.get('C')
    elif operand == 7:
        raise ValueError("Reserved operand encountered: 7 is not valid.")


def solve_part1(registers, program):
    out = []
    pointer = 0

    while pointer < len(program):

        opcode = program[pointer]

        if pointer + 1 >= len(program):
            print("Incomplete instruction at the end of the program. Halting.")
            break

        operand = program[pointer+1]

        if opcode == 0:  # Truncated Division: A/2**combo_operand --> Write to A
            combo_operand = get_combo_operand(registers, operand)
            a_value = registers.get('A')
            write_to_a = int(a_value/(2**combo_operand))
            registers["A"] = write_to_a
            pointer += 2

        elif opcode == 1:  # bitwise XOR: R with literal_operand --> Write to B 
            b_value = registers.get('B')
            write_to_b = b_value ^ operand
            registers["B"] = write_to_b
            pointer += 2
        
        elif opcode == 2:  # combo_operand % 8 --> Write to B
            combo_operand = get_combo_operand(registers, operand)
            write_to_b = combo_operand % 8
            registers["B"] = write_to_b
            pointer += 2
        
        elif opcode == 3:  # if A != 0 --> jump
            if registers.get('A') != 0:
                pointer = operand
            else:
                pointer += 2
        
        elif opcode == 4:  # bitwise XOR: B ^ C --> Write to B
            b_value = registers.get('B')
            c_value = registers.get('C')
            write_to_b = b_value ^ c_value
            registers["B"] = write_to_b
            pointer += 2

        elif opcode == 5:  # combo_operand % 8 --> out
            combo_operand = get_combo_operand(registers, operand)
            out_value = combo_operand % 8
            out.append(out_value)
            pointer += 2

        elif opcode == 6:  # Truncated Division: A/2**combo_operand --> Write to B
            combo_operand = get_combo_operand(registers, operand)
            a_value = registers.get('A')
            write_to_b = int(a_value/(2**combo_operand))
            registers["B"] = write_to_b
            pointer += 2

        elif opcode == 7:  # Truncated Division: A/2**combo_operand --> Write to C
            combo_operand = get_combo_operand(registers, operand)
            a_value = registers.get('A')
            write_to_c = int(a_value/(2**combo_operand))
            registers["C"] = write_to_c
            pointer += 2
    
    return out

start = timeit.default_timer()
part1_sol = solve_part1(registers=registers, program=program)
elapsed_time = timeit.default_timer()-start
print(f'Day 17 Part 1 Solution = {part1_sol}')
print(f'Day 17 Part 1 Run Time = {str(elapsed_time)}')


## ----- PART 2 ----- ##

As = []

def step(A):
    """Run a single loop."""
    B = A % 8
    B = B ^ 6
    C = A // (2**B)
    B = B ^ C
    B = B ^ 7
    return B % 8


def solve_part2(A, col=0):
    if step(A) != program[-(col + 1)]:
        return

    if col == len(program) - 1:
        As.append(A)
        print(As)
    else:
        for B in range(8):
            solve_part2(A * 8 + B, col + 1)

start = timeit.default_timer()
for a in range(8):
    solve_part2(a)
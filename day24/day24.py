import timeit
import re
from collections import defaultdict, deque


## ----- PART 1 ----- ##

def solve_part1():

    # Read the entire puzzle input
    with open("day24/input.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Separate lines into two sections:
    # 1) wire initialization lines (like "x00: 1")
    # 2) gate definition lines (like "x00 AND y00 -> z00")
    wire_init_lines = []
    gate_lines = []
    
    parsing_init = True
    for line in lines:
        # If we detect the pattern of a gate, we switch
        if "->" in line:
            parsing_init = False
        
        if parsing_init:
            wire_init_lines.append(line)
        else:
            gate_lines.append(line)

    # Dictionary: wire_name -> int (0 or 1)
    wires = {}
    
    # Parse initial wire values
    # Format: "x00: 1"
    for line in wire_init_lines:
        # Split by ':'
        left, val_str = line.split(":")
        wire_name = left.strip()
        val = int(val_str.strip())
        wires[wire_name] = val

    # Dictionary of gates: output_wire -> (input_wire_A, operation, input_wire_B)
    gates = {}
    
    # For dependency graph: which gates depend on a given wire?
    # wire_dependencies[wire_name] = [output_wire1, output_wire2, ...]
    # Meaning: "whenever wire_name becomes known, we can check if gates[output_wire?] can be computed"
    wire_dependencies = defaultdict(list)

    # Parse gate definitions
    # Format: "A OP B -> C"
    # Example: "x00 AND y00 -> z00"
    gate_pattern = re.compile(r"^(\S+)\s+(AND|OR|XOR)\s+(\S+)\s+->\s+(\S+)$")

    for line in gate_lines:
        match = gate_pattern.match(line)
        if not match:
            raise ValueError(f"Invalid gate definition: {line}")
        inA, operation, inB, outWire = match.groups()
        gates[outWire] = (inA, operation, inB)
        # Record that outWire depends on inA and inB
        wire_dependencies[inA].append(outWire)
        wire_dependencies[inB].append(outWire)

    # A queue of wires that we know the value of, to propagate changes
    queue = deque(wires.keys())

    while queue:
        known_wire = queue.popleft()
        known_val = wires[known_wire]

        # Check all gates that depend on this known_wire
        for outWire in wire_dependencies[known_wire]:
            # If outWire is already known, skip
            if outWire in wires:
                continue

            inA, operation, inB = gates[outWire]

            # Check if we know both inputs
            if inA in wires and inB in wires:
                valA = wires[inA]
                valB = wires[inB]
                
                if operation == "AND":
                    result = valA & valB
                elif operation == "OR":
                    result = valA | valB
                elif operation == "XOR":
                    result = valA ^ valB
                else:
                    raise ValueError(f"Unknown operation: {operation}")

                # Store output
                wires[outWire] = result
                # Enqueue this wire name so we can propagate further
                queue.append(outWire)

    # Now gather all z-wires
    # They look like z00, z01, z02, etc.
    z_wires = [w for w in wires.keys() if w.startswith("z")]
    
    # Sort them numerically by the digits after 'z'
    # We'll assume the format is zNN, zNNN, etc. 
    # Extract the trailing digits to sort correctly.
    def z_index(w):
        # if wire is z00, numeric index is 0
        # if wire is z01, numeric index is 1, etc.
        return int(w[1:])  # since w starts with 'z', skip 'z' and parse the rest as int

    z_wires.sort(key=z_index)

    # Combine bits into a binary number
    # z00 is the least significant bit -> rightmost bit in normal binary
    # So if z_wires = ['z00', 'z01', 'z02', ...],
    # the binary representation is z00 as the rightmost bit, z01 next, etc.
    # i.e. if z00=1, that is 2^0; if z01=0, that is 2^1 with 0, etc.
    bits = []
    for zw in z_wires:
        bits.append(str(wires[zw]))  # '0' or '1'

    # Right now bits = [z00_val, z01_val, z02_val, ...]
    # But z00_val is the LSB, so in a typical binary string that is reversed.
    # Easiest approach: bits[0] is LSB, bits[1] is next ...
    # We can reverse and join to interpret in standard left-to-right order.
    binary_str = "".join(reversed(bits))  # reverse so the leftmost is the highest-order bit
    decimal_value = int(binary_str, 2) if binary_str else 0

    return(decimal_value)


start = timeit.default_timer()
part1_sol = solve_part1()
elapsed_time = timeit.default_timer()-start
print(f'Day 24 Part 1 Solution = {part1_sol}')
print(f'Day 24 Part 1 Run Time = {str(elapsed_time)}')



## ----- PART 2 ----- ##

import operator

# Map gate names (e.g. "XOR") to Python's operator functions
GATE_FUNCS = {
    "AND": operator.and_,
    "OR":  operator.or_,
    "XOR": operator.xor
}

lines_with_gates = []
with open('day24/input.txt') as f:
    for line in f:
        line = line.strip()
        if '->' in line:
            # Keep only lines describing gates: "a GATE b -> c"
            parts = line.split()
            lines_with_gates.append(parts)

def used_as_input_to_gate_type(wire_name, gate_type):
    """
    Returns True if 'wire_name' is used as an input to any gate of type
    'gate_type' in the puzzle lines.
    """
    for a, x, b, arrow, c in lines_with_gates:
        if x == gate_type and wire_name in (a, b):
            return True
    return False

def solve_part2():
    suspicious_wires = []
    for a, x, b, arrow, c in lines_with_gates:    
        cond1 = (x == "XOR" and all(d[0] not in 'xyz' for d in (a, b, c)))
        cond2 = (x == "AND" and "x00" not in (a, b)
                and used_as_input_to_gate_type(c, "XOR"))
        cond3 = (x == "XOR" and "x00" not in (a, b)
                and used_as_input_to_gate_type(c, "OR"))
        cond4 = (x != "XOR" and c.startswith('z') and c != "z45")
        
        if cond1 or cond2 or cond3 or cond4:
            suspicious_wires.append(c)

    # Print the sorted list of suspicious wires, comma-separated
    return(",".join(sorted(suspicious_wires)))

start = timeit.default_timer()
part2_sol = solve_part2()
elapsed_time = timeit.default_timer()-start
print(f'Day 24 Part 2 Solution = {part2_sol}')
print(f'Day 24 Part 2 Run Time = {str(elapsed_time)}')
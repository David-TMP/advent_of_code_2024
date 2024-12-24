from collections import defaultdict
import itertools

# Read the network map from the file
with open('day23/input.txt', 'r') as f:
    network_map = [tuple(line.strip().split("-")) for line in f.readlines()]

# Build adjacency_list (bidirectional)
adjacency_list = defaultdict(set)
for key, value in network_map:
    adjacency_list[key].add(value)
    adjacency_list[value].add(key)  # Bidirectional

# Get all unique computers
computers = list(adjacency_list.keys())

# Generate all possible combinations of 3 computers
triplets = itertools.combinations(computers, 3)

# Initialize a list to store valid triplets
valid_triplets = []

# Iterate through each triplet
for triplet in triplets:
    a, b, c = triplet
    # Check if all pairs within the triplet are connected
    if (b in adjacency_list[a]) and (c in adjacency_list[a]) and (c in adjacency_list[b]):
        valid_triplets.append(triplet)

# Initialize a counter for triplets containing at least one 't' starting computer
contador = 0

# Iterate through valid triplets
for triplet in valid_triplets:
    # Check if any computer in the triplet starts with 't'
    if any(computer.startswith('t') for computer in triplet):
        contador += 1
        print(triplet)  # Optional: Print the triplet

print(f"\nTotal number of valid triplets containing at least one 't' starting computer: {contador}")

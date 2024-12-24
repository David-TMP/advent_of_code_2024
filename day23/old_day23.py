from collections import defaultdict
import itertools

with open('day23/input.txt', 'r') as f:
    network_map = [tuple(line.strip().split("-")) for line in f.readlines()]

print(network_map)

# Build adjacency_list (bidirectional)
adjacency_list = defaultdict(set)
for key, value in network_map:
    adjacency_list[key].add(value)
    adjacency_list[value].add(key)  # Bidirectional

# Create a set of frozensets for efficient bidirectional lookup
network_set = set(frozenset(pair) for pair in network_map)

# Iterate through adjacency_list for keys starting with 't'
contador = 0
for key, values in adjacency_list.items():
    if key.startswith('t'):
        print(f"\nChecking pairs for key: '{key}'")
        
        # Convert set to list for combination generation
        values_list = list(values)
        
        # Generate all unique pairs (combinations of 2)
        pairs = itertools.combinations(values_list, 2)
        
        # Iterate through each pair and check existence in network_set
        for pair in pairs:
            pair_set = frozenset(pair)  # Unordered pair
            exists = pair_set in network_set
            print(f"Pair {pair} exists in network_map: {exists}")
            if exists:
                contador += 1

print(contador)
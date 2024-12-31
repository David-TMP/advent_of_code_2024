import timeit
from collections import defaultdict
import itertools
import networkx as nx  # For Part 2

# Read the network map from the file
with open('day23/input.txt', 'r') as f:
    network_map = [tuple(line.strip().split("-")) for line in f.readlines()]


## ----- PART 1 ----- ##

def solve_part1(network_map):

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

    return(contador)

start = timeit.default_timer()
part1_sol = solve_part1(network_map)
elapsed_time = timeit.default_timer()-start
print(f'Day 23 Part 1 Solution = {part1_sol}')
print(f'Day 23 Part 1 Run Time = {str(elapsed_time)}')



## ----- PART 2 ----- ##

def solve_part2(network_map):

    # Create an undirected graph
    G = nx.Graph()

    # Add edges to the graph from the network_map
    G.add_edges_from(network_map)

    # Find all cliques in the graph
    cliques = list(nx.find_cliques(G))

    # Identify the maximum clique(s)
    max_clique_size = max(len(clique) for clique in cliques)
    max_cliques = [clique for clique in cliques if len(clique) == max_clique_size]

    # For debugging: Print all maximum cliques
    # print(f"Maximum Clique Size: {max_clique_size}")
    # print("Maximum Clique(s):")
    # for clique in max_cliques:
    #     print(clique)

    # Assuming there's only one maximum clique, as in the example
    # If multiple, you may need to handle them accordingly
    # For this example, we'll select the first one
    lan_party_clique = max_cliques[0]

    # Sort the computer names alphabetically
    sorted_clique = sorted(lan_party_clique)

    # Generate the password by joining with commas
    password = ','.join(sorted_clique)
    
    return (password)

start = timeit.default_timer()
part2_sol = solve_part2(network_map)
elapsed_time = timeit.default_timer()-start
print(f'Day 23 Part 2 Solution = {part2_sol}')
print(f'Day 23 Part 2 Run Time = {str(elapsed_time)}')

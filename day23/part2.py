import networkx as nx

# Define the network map as a list of tuples
with open('day23/input.txt', 'r') as f:
    network_map = [tuple(line.strip().split("-")) for line in f.readlines()]

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
print(f"Maximum Clique Size: {max_clique_size}")
print("Maximum Clique(s):")
for clique in max_cliques:
    print(clique)

# Assuming there's only one maximum clique, as in the example
# If multiple, you may need to handle them accordingly
# For this example, we'll select the first one
lan_party_clique = max_cliques[0]

# Sort the computer names alphabetically
sorted_clique = sorted(lan_party_clique)

# Generate the password by joining with commas
password = ','.join(sorted_clique)
print(password)

print(f"\nPassword to get into the LAN party: {password}")

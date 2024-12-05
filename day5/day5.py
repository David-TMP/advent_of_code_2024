from collections import defaultdict, deque

# Reading the file content from input.txt in the root directory
with open("day5/input.txt", "r") as file:
    file_content = file.read()

# Splitting the content into two parts
sections = file_content.strip().split("\n\n")
dict_lines = sections[0].strip().split("\n")
list_lines = sections[1].strip().split("\n")

# Creating a set of ordering rules as pairs (X, Y)
ordering_rules = set()
for line in dict_lines:
    key, value = map(int, line.split("|"))
    ordering_rules.add((key, value))

# Converting the second part into a list of lists
list_data = [list(map(int, line.strip().split(","))) for line in list_lines]

def validate_update(update):
    """Check if the update is correctly ordered."""
    page_index = {page: idx for idx, page in enumerate(update)}
    for X, Y in ordering_rules:
        if X in page_index and Y in page_index:
            if page_index[X] > page_index[Y]:
                return False
    return True

def reorder_update(update):
    """Reorder an update based on the rules using topological sort."""
    # Create a graph for topological sorting
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    pages_in_update = set(update)

    # Build the graph for the pages in this update
    for X, Y in ordering_rules:
        if X in pages_in_update and Y in pages_in_update:
            graph[X].append(Y)
            in_degree[Y] += 1
            in_degree[X] += 0  # Ensure all pages have an in-degree entry

    # Topological sort using Kahn's algorithm
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_update = []

    while queue:
        node = queue.popleft()
        sorted_update.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

# Process updates and find results for Part 1 and Part 2
valid_middle_numbers = []
invalid_middle_numbers = []

for update in list_data:
    if validate_update(update):
        # Valid update
        middle_index = len(update) // 2
        valid_middle_numbers.append(update[middle_index])
    else:
        # Invalid update, reorder it
        reordered_update = reorder_update(update)
        middle_index = len(reordered_update) // 2
        invalid_middle_numbers.append(reordered_update[middle_index])

# Results
print(f"Part 1 Sol = {sum(valid_middle_numbers)}")  # Sum of middle numbers of valid updates
print(f"Part 2 Sol = {sum(invalid_middle_numbers)}")  # Sum of middle numbers of reordered updates

from itertools import product

def generate_combinations(n):
    """
    Generate all combinations of '*' and '+' for a given number n.

    Args:
        n (int): The number of positions to fill with '*' and '+'.

    Returns:
        list: A list of tuples containing all possible combinations.
    """
    # Use itertools.product to generate combinations
    combinations = list(product(["+", "*"], repeat=n))
    return combinations

# Example usage
number = 2
result = generate_combinations(number)
print(result)

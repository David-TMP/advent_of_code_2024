import os

def read_positions(file_path):
    """
    Reads a file containing X,Y positions and returns a list of tuples.

    Args:
        file_path (str): The path to the input file.

    Returns:
        List[Tuple[int, int]]: A list of (X, Y) tuples.
    """
    positions = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                # Remove any surrounding whitespace and newline characters
                stripped_line = line.strip()
                
                # Skip empty lines
                if not stripped_line:
                    continue
                
                # Split the line by comma
                parts = stripped_line.split(',')
                
                if len(parts) != 2:
                    print(f"Warning: Line {line_number} is malformed: '{stripped_line}'")
                    continue
                
                try:
                    x = int(parts[0])
                    y = int(parts[1])
                    positions.append((x, y))
                except ValueError:
                    print(f"Warning: Non-integer value on line {line_number}: '{stripped_line}'")
                    
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
    
    return positions

def main():
    # Define the relative path to the input file
    input_file = os.path.join('day18', 'input.txt')
    
    # Read and parse the positions
    positions = read_positions(input_file)
    
    # Output the positions
    print(positions)

if __name__ == "__main__":
    main()

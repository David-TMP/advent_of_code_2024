def read_input(file_path):
    with open(file_path, 'r') as f:
        line = f.read().strip()
    return line

def parse_disk_map(disk_map_str):
    # disk_map_str is a single line of digits
    digits = [int(d) for d in disk_map_str]
    # The format alternates: file_length, space_length, file_length, space_length, ...
    # If the number of digits is odd, the last one is a file length without trailing space.
    # Count how many files we have (which is half the number of digits if even, else (len(digits)+1)//2)
    # Actually, each pair (file_length, space_length) defines one file and one space,
    # and if there's an odd number of digits, there's a final file without following space.

    file_count = (len(digits) + 1) // 2  # Each file_length gets a file ID

    file_lengths = []
    space_lengths = []
    for i in range(0, len(digits), 2):
        flen = digits[i]
        file_lengths.append(flen)
        if i+1 < len(digits):
            slen = digits[i+1]
            space_lengths.append(slen)
        else:
            # No space after last file if odd count
            space_lengths.append(0)

    # Build the block layout
    # Example: file_length=3 (ID=0), space_length=2, file_length=4 (ID=1), space_length=1 => 
    # blocks = [0,0,0,'.','.','1','1','1','1','.']
    blocks = []
    for fid, flen in enumerate(file_lengths):
        # Add the file blocks
        for _ in range(flen):
            blocks.append(fid)
        # Add the space blocks if not the last segment
        if fid < len(space_lengths):
            for _ in range(space_lengths[fid]):
                blocks.append('.')

    return blocks, len(file_lengths)

def find_file_positions(blocks, file_id):
    # Returns the start index and length of the given file_id in the blocks
    # The file might be contiguous (as per the problem statement, each file is contiguous).
    # We'll find the first occurrence and count how many consecutive blocks match.
    # If the file has been moved before or never moved (still contiguous),
    # we just find one contiguous run of that file_id.
    start = None
    length = 0
    for i, b in enumerate(blocks):
        if b == file_id:
            if start is None:
                start = i
            length += 1
    return start, length

def find_left_space_for_file(blocks, file_start, file_length):
    # Find a contiguous run of '.' to the left of file_start that can fit file_length
    # Search from left to right for a run of '.' that ends < file_start and run length >= file_length
    # We only consider runs that are entirely to the left: run_end < file_start
    dot_runs = []
    in_run = False
    run_start = 0
    # Identify all runs of '.' to the left of file_start
    for i in range(file_start):
        if blocks[i] == '.':
            if not in_run:
                in_run = True
                run_start = i
        else:
            if in_run:
                # run ends at i-1
                run_length = i - run_start
                dot_runs.append((run_start, run_length))
                in_run = False
    # If ended in a run
    if in_run:
        run_length = file_start - run_start
        dot_runs.append((run_start, run_length))

    # Now find the first run that can hold file_length
    for (s, l) in dot_runs:
        if l >= file_length:
            return s
    return None

def move_file(blocks, file_id):
    # Move the file if possible according to Part 2 rules
    # 1) Get file position
    fstart, flen = find_file_positions(blocks, file_id)
    if fstart is None or flen == 0:
        # File with length 0 or not found, no move
        return

    # 2) Find a suitable space to the left
    new_start = find_left_space_for_file(blocks, fstart, flen)
    if new_start is None:
        # No suitable space found, do nothing
        return

    # 3) Move the file:
    # Clear old position (replace with '.')
    for i in range(fstart, fstart + flen):
        blocks[i] = '.'
    # Place file in the new position
    for i in range(new_start, new_start + flen):
        blocks[i] = file_id

def compute_checksum(blocks):
    # checksum = sum of (index * file_id for each file block)
    result = 0
    for i, b in enumerate(blocks):
        if b != '.':
            # b is file_id (int)
            result += i * b
    return result

if __name__ == "__main__":
    file_path = "day9/input.txt"
    disk_map_str = read_input(file_path)
    blocks, file_count = parse_disk_map(disk_map_str)

    # Move files in order of decreasing file ID
    for fid in range(file_count - 1, -1, -1):
        move_file(blocks, fid)

    # Compute checksum
    checksum = compute_checksum(blocks)
    print(checksum)

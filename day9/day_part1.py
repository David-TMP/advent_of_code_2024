from collections import deque

file_path = "day9/input.txt"

with open(file_path, 'r') as f:
    disk_map = [int(digit) for digit in f.read().strip()]

# Separate the disk map into files and spaces.
# files: a deque of (file_length, file_id)
# space: a deque of space_length
files = deque()
space = deque()

file_id = 0
# We assume the input always starts with a file-length and alternates file-length, space-length, etc.
for i in range(0, len(disk_map), 2):
    flen = disk_map[i]
    if flen > 0:
        files.append((flen, file_id))
    else:
        # Even if file length is 0, it still consumes a file ID
        # but it won't produce any blocks.
        files.append((0, file_id))
    file_id += 1
    if i + 1 < len(disk_map):
        space.append(disk_map[i + 1])

sol = []

def solve_part1():
    contador = -1
    # contador steps through each segment: even steps are files, odd steps are spaces.
    # We'll consume from the left (files and space) and from the right (files) as needed.

    # Make local copies since we'll consume from them
    current_files = deque(files)
    current_spaces = deque(space)

    # Process until we run out of file segments from the left.
    while current_files or current_spaces:
        contador += 1
        # Even contador => File segment from the left
        if (contador % 2) == 0:
            if not current_files:
                # No more files to process
                break
            flen, fid = current_files.popleft()
            # This just places that file segment in the sol array as is, no movement needed yet.
            for _ in range(flen):
                sol.append(fid)
        else:
            # Odd contador => Space segment
            if not current_spaces:
                # No more spaces
                break
            sp = current_spaces.popleft()
            
            # We now need to fill this space from the end of the disk.
            # That means taking from the last file in current_files (the rightmost one)
            # until the space is filled.
            while sp > 0 and current_files:
                # Look at the last file segment
                last_flen, last_fid = current_files.pop()
                
                if last_flen == 0:
                    # This file segment is empty, just continue
                    continue

                if sp == last_flen:
                    # Perfect match: move all blocks of this file segment into space
                    for _ in range(last_flen):
                        sol.append(last_fid)
                    sp = 0
                    # last file segment fully consumed
                elif sp > last_flen:
                    # Space is larger than this file segment
                    # Move entire file segment
                    for _ in range(last_flen):
                        sol.append(last_fid)
                    sp -= last_flen
                    # last file segment fully consumed
                else:
                    # sp < last_flen
                    # Move only part of the file segment
                    for _ in range(sp):
                        sol.append(last_fid)
                    # Put back the remaining part of the file segment
                    remaining = last_flen - sp
                    sp = 0
                    # The remainder of this file segment is put back at the end
                    current_files.append((remaining, last_fid))
    
    return sol

x = solve_part1()

# Compute the checksum
checksum = sum(index * value for index, value in enumerate(x))
print(x)
print(checksum)

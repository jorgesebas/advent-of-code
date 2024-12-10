import sys
import time


def parse_disk_map(line):
    """Parse a disk map string into a list of blocks."""
    disk = []
    is_file = True
    file_id = 0

    for char in line:
        length = int(char)
        if is_file:
            disk.extend([file_id] * length)  # Add file blocks
            file_id += 1
        else:
            disk.extend([-1] * length)  # Add free space
        is_file = not is_file

    return disk


def compact_disk(disk):
    """Compact the disk by moving file blocks to the left."""
    last_position = 0
    for i in range(len(disk) - 1, -1, -1):
        if disk[i] >= 0:  # Found a file block
            for j in range(last_position, i):
                if disk[j] < 0:  # Found a free space
                    disk[j] = disk[i]
                    disk[i] = -1
                    last_position = j + 1
                    break
    return disk


def calculate_checksum(disk):
    """Calculate the checksum of the compacted disk."""
    return sum(i * block for i, block in enumerate(disk) if block >= 0)


def main():
    start = time.time()

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <map_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as file:
            total_checksum = 0

            for line in file:
                line = line.strip()

                # Parse the disk map
                disk = parse_disk_map(line)

                # Compact the disk
                disk = compact_disk(disk)

                # Calculate the checksum
                total_checksum += calculate_checksum(disk)

        print(f"Processing time: {1000 * (time.time() - start):.3f} ms")
        print(f"Total checksum: {total_checksum}")

    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid data in file.")
        sys.exit(1)


if __name__ == "__main__":
    main()

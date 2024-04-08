# file_operations.py


def read_file_in_chunks(file_descriptor, chunk_size=25 * 1024 * 1024):
    """Read a file in incremental chunks."""
    while True:
        chunk = file_descriptor.read(chunk_size)
        if not chunk:
            break
        yield chunk


def write_file(file_descriptor, data, chunk_size=25 * 1024 * 1024):
    """Write data to a file in incremental chunks."""
    for i in range(0, len(data), chunk_size):
        file_descriptor.write(data[i : i + chunk_size])


def open_file(file_path, mode="r"):
    """Open a file and return the file object."""
    try:
        file = open(file_path, mode)
        return file
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error opening file '{file_path}': {e}")
        return None

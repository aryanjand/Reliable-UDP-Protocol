# file_operations.py
from typing import IO, Any


def read_file_in_chunks(file_descriptor, chunk_size=512) -> bytes:
    """Read a file in incremental chunks."""
    while True:
        chunk = file_descriptor.read(chunk_size)
        if not chunk:
            break
        yield chunk


def write_file(file_path, data, chunk_size=512):
    """Write data to a file in incremental chunks."""
    with open(file_path, "a") as file_descriptor:
        for i in range(0, len(data), chunk_size):
            file_descriptor.write(data[i : i + chunk_size])


def open_file(file_path, mode="r") -> IO[Any] | None:
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

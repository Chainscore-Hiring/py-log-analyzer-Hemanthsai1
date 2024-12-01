import os

def chunk_file(filepath: str, chunk_size: int):
    """Chunk a large log file into smaller pieces."""
    file_size = os.path.getsize(filepath)
    chunks = []

    with open(filepath, "r") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)

    return chunks

def split_file(filepath: str, num_chunks: int):
    """Split the file into a specific number of chunks."""
    file_size = os.path.getsize(filepath)
    chunk_size = file_size // num_chunks

    return chunk_file(filepath, chunk_size)

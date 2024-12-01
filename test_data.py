import random

def generate_test_data(size_mb: int, path: str) -> None:
    """
    Generates a test log file of the specified size.

    Args:
        size_mb (int): Size of the log file to generate in megabytes.
        path (str): Path where the log file should be saved.
    """
    log_patterns = [
        "INFO - Request processed in {}ms",
        "ERROR - Request failed with status code {}",
        "WARNING - Slow response time: {}ms"
    ]

    # Calculate the number of lines to generate based on file size
    num_lines = size_mb * 1024 * 1024 // 100 

    with open(path, 'w') as log_file:
        for _ in range(num_lines):
            log_pattern = random.choice(log_patterns)
            response_time = random.randint(50, 500) 
            status_code = random.choice([200, 500, 404]) 
            log_entry = log_pattern.format(response_time if 'Request processed' in log_pattern else status_code)
            log_file.write(log_entry + '\n')

    print(f"Test data of size {size_mb}MB generated at {path}")

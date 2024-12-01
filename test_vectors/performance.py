import time
import psutil
from coordinator import Coordinator
from worker import Worker
from test_data import generate_test_data

async def test_processing_speed():
    """Test processing speed meets requirements"""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker(port=8001, worker_id="worker1", coordinator_url="http://localhost:8000"),
        Worker(port=8002, worker_id="worker2", coordinator_url="http://localhost:8000"),
        Worker(port=8003, worker_id="worker3", coordinator_url="http://localhost:8000")
    ]
    
    generate_test_data(size_mb=1024, path="test_vectors/logs/large.log")
    
    start_time = time.time()
    await coordinator.distribute_work("test_vectors/logs/large.log")
    
    # Calculate duration to process the file
    duration = time.time() - start_time
    
    processing_speed = 1024 / duration
    print(f"Processing speed: {processing_speed} MB/sec")
    assert processing_speed >= 100, f"Processing speed too low: {processing_speed} MB/sec"

async def test_memory_usage():
    """Test memory stays within limits"""
    import psutil
    
    worker = Worker(port=8001, worker_id="worker1", coordinator_url="http://localhost:8000")
    process = psutil.Process()
    
    initial_memory = process.memory_info().rss
    
    await worker.process_chunk("test_vectors/logs/large.log", start=0, size=1024*1024*100)
    
    peak_memory = process.memory_info().rss
    
    memory_used = peak_memory - initial_memory
    print(f"Memory used: {memory_used / (1024 * 1024)} MB")
    assert memory_used < 500 * 1024 * 1024, f"Memory usage exceeded limit: {memory_used / (1024 * 1024)} MB"

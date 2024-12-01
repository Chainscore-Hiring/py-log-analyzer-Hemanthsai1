import pytest
<<<<<<< HEAD
from network import Worker, Coordinator


@pytest.mark.asyncio
async def test_normal_processing():
    """Test normal log processing with all workers."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000", "http://localhost:8000"),
        Worker("worker2", "localhost:8001", "http://localhost:8000"),
        Worker("worker3", "localhost:8002", "http://localhost:8000"),
    ]

    await coordinator.start()
    for worker in workers:
        await coordinator.add_worker(worker)

    logs = ["log1", "log2", "log3"]
    results = await coordinator.process_logs(logs)
    assert len(results) == len(logs)
    for result in results:
        assert "Processed by" in result

    await coordinator.stop()


@pytest.mark.asyncio
async def test_worker_failure():
    """Test recovery from worker failure."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000", "http://localhost:8000"),
        Worker("worker2", "localhost:8001", "http://localhost:8000"),
        Worker("worker3", "localhost:8002", "http://localhost:8000"),
    ]

    await coordinator.start()
    for worker in workers:
        await coordinator.add_worker(worker)

    # Simulate worker failure
    workers[1].healthy = False

    logs = ["log1", "log2", "log3"]
    results = await coordinator.process_logs(logs)
    assert len(results) == len(logs)
    assert any("Error" in result for result in results)

    await coordinator.stop()


@pytest.mark.asyncio
async def test_malformed_logs():
    """Test handling of malformed logs."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000", "http://localhost:8000"),
        Worker("worker2", "localhost:8001", "http://localhost:8000"),
    ]

    await coordinator.start()
    for worker in workers:
        await coordinator.add_worker(worker)

    # Simulate malformed log
    logs = ["log1", "", None]
    results = await coordinator.process_logs(logs)
    assert len(results) == len(logs)
    assert any("Processed by" in result for result in results)

    await coordinator.stop()
=======
import asyncio

async def test_normal_processing():
    """Test normal log processing with all workers"""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000"),
        Worker("worker2", "localhost:8000"),
        Worker("worker3", "localhost:8000")
    ]
    
    # Start system
    await coordinator.start()
    for w in workers:
        await w.start()
    
    # Process normal logs
    results = await coordinator.process_file("test_vectors/logs/normal.log")
    
    # Verify results
    assert results["avg_response_time"] == pytest.approx(109.0, rel=1e-2)
    assert results["error_rate"] == 0.0
    assert results["requests_per_second"] == pytest.approx(50.0, rel=1e-2)

async def test_worker_failure():
    """Test recovery from worker failure"""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000"),
        Worker("worker2", "localhost:8000"),
        Worker("worker3", "localhost:8000")
    ]
    
    # Start with failing worker scenario
    await NetworkScenarios.worker_failure()
    
    # Process should complete despite failure
    results = await coordinator.process_file("test_vectors/logs/normal.log")
    
    # Verify results still accurate
    assert results["total_requests"] == 3000

async def test_malformed_logs():
    """Test handling of malformed logs"""
    coordinator = Coordinator(port=8000)
    workers = [Worker("worker1", "localhost:8000")]
    
    results = await coordinator.process_file("test_vectors/logs/malformed.log")
    
    assert results["malformed_lines"] == 30
    assert results["total_requests"] == 200
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef

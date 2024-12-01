import pytest
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

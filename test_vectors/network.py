<<<<<<< HEAD
class Worker:
    def __init__(self, name, address, coordinator_url):
        self.name = name
        self.address = address
        self.coordinator_url = coordinator_url
        self.healthy = True

    async def start(self):
        """Simulates starting the worker."""
        print(f"Worker {self.name} started at {self.address}.")

    async def stop(self):
        """Simulates stopping the worker."""
        print(f"Worker {self.name} stopped.")

    async def process(self, data):
        """Simulates processing data."""
        if not self.healthy:
            raise RuntimeError(f"Worker {self.name} failed during processing.")
        return f"Processed by {self.name}: {data}"


class Coordinator:
    def __init__(self, port):
        self.port = port
        self.workers = []

    async def start(self):
        """Simulates starting the coordinator."""
        print(f"Coordinator started on port {self.port}.")

    async def stop(self):
        """Simulates stopping the coordinator."""
        print("Coordinator stopped.")

    async def add_worker(self, worker):
        """Adds a worker to the coordinator."""
        self.workers.append(worker)
        await worker.start()

    async def process_logs(self, logs=None):
        """Simulates log processing."""
        if logs is None:
            logs = ["log1", "log2", "log3"]
        results = []
        for i, log in enumerate(logs):
            worker = self.workers[i % len(self.workers)]
            try:
                result = await worker.process(log)
                results.append(result)
            except RuntimeError as e:
                print(e)
                results.append(f"Error: {e}")
        return results


class NetworkScenarios:
    @staticmethod
    async def normal():
        """All workers responsive."""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 12},
=======
class NetworkScenarios:
    @staticmethod
    async def normal():
        """All workers responsive"""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 12}
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef
        }

    @staticmethod
    async def worker_failure():
<<<<<<< HEAD
        """Worker 2 fails after 50% processing."""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": False, "fail_at": 0.5},
            "worker3": {"healthy": True, "latency": 12},
=======
        """Worker 2 fails after 50% processing"""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": False, "fail_at": 0.5},
            "worker3": {"healthy": True, "latency": 12}
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef
        }

    @staticmethod
    async def high_latency():
<<<<<<< HEAD
        """Worker 3 has high latency."""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 1000},
        }
=======
        """Worker 3 has high latency"""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 1000}
        }
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef

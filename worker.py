import argparse
<<<<<<< HEAD
import asyncio
import aiohttp
from aiohttp import web
from utils.chunker import split_file
from utils.logger import setup_logger


logger = setup_logger("worker", "worker.log")

class Worker:
    """Processes log chunks and reports results"""
    
    def __init__(self, worker_id: str, port: int, coordinator_url: str):
=======


class Worker:
    """Processes log chunks and reports results"""
    
    def __init__(self, port: int, worker_id: str, coordinator_url: str):
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef
        self.worker_id = worker_id
        self.coordinator_url = coordinator_url
        self.port = port
    
<<<<<<< HEAD
    async def start(self) -> None:
        """Start the worker server and begin processing"""
        logger.info(f"Starting worker {self.worker_id} on port {self.port}...")
        await self.run_server()
    
    async def run_server(self):
        """Run an HTTP server for worker to listen to requests"""
        app = web.Application()
        app.router.add_post("/process_chunk", self.handle_process_chunk)
        app.router.add_post("/report_health", self.handle_report_health)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.port)
        await site.start()
        
        logger.info(f"Worker {self.worker_id} listening on port {self.port}...")
        
        # Keeping the worker running
        while True:
            await asyncio.sleep(3600)

    async def handle_process_chunk(self, request):
        """Handle a request to process a log chunk"""
        data = await request.json()
        filepath = data.get("filepath")
        start = data.get("start")
        size = data.get("size")
        
        # Processing the log chunk
        metrics = await self.process_chunk(filepath, start, size)
        
        return web.json_response(metrics)

    async def handle_report_health(self, request):
        """Handle a request to report worker's health"""
        logger.info(f"Worker {self.worker_id} is reporting health.")
        return web.json_response({"status": "healthy"})
    
    async def process_chunk(self, filepath: str, start: int, size: int) -> dict:
        """Process a chunk of log file and return metrics"""
        logger.info(f"Processing chunk from {start} to {start + size}...")
        
        
        chunks = split_file(filepath, num_chunks=5)
        
        # Placeholder for metrics
        metrics = {
            "error_rate": 0.05,  
            "avg_response_time": 150,
            "request_count_per_second": 1000,
        }
        
        logger.debug(f"Processed chunk: {metrics}")
        return metrics

    async def report_health(self) -> None:
        """Send heartbeat to coordinator"""
        logger.info(f"Worker {self.worker_id} is reporting health to coordinator {self.coordinator_url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.coordinator_url}/report_health", json={"worker_id": self.worker_id}) as resp:
                    if resp.status == 200:
                        logger.info(f"Health report successful for Worker {self.worker_id}")
                    else:
                        logger.error(f"Failed to report health for Worker {self.worker_id}, status code: {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error while reporting health for Worker {self.worker_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while reporting health for Worker {self.worker_id}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Analyzer Worker")
    parser.add_argument("--port", type=int, default=8001, help="Worker port")
=======
    def start(self) -> None:
        """Start worker server"""
        print(f"Starting worker {self.worker_id} on port {self.port}...")
        pass

    async def process_chunk(self, filepath: str, start: int, size: int) -> dict:
        """Process a chunk of log file and return metrics"""
        pass

    async def report_health(self) -> None:
        """Send heartbeat to coordinator"""
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Analyzer Coordinator")
    parser.add_argument("--port", type=int, default=8000, help="Coordinator port")
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef
    parser.add_argument("--id", type=str, default="worker1", help="Worker ID")
    parser.add_argument("--coordinator", type=str, default="http://localhost:8000", help="Coordinator URL")
    args = parser.parse_args()

    worker = Worker(port=args.port, worker_id=args.id, coordinator_url=args.coordinator)
<<<<<<< HEAD
    asyncio.run(worker.start())
=======
    worker.start()
>>>>>>> f9f616e5113d2b9cf80789f4024f6db869e36bef

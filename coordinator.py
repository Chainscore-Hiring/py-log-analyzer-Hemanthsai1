import os
import argparse
import asyncio
import aiohttp
from aiohttp import web
from typing import List, Dict
from utils.chunker import split_file
from utils.logger import setup_logger
from unittest.mock import AsyncMock


logger = setup_logger("coordinator", "coordinator.log")

class Coordinator:
    """Manages workers and aggregates results"""
    
    def __init__(self, port: int):
        self.workers = {}
        self.results = {}
        self.port = port
        self.failed_workers = set()
    
    async def run_server(self):
        """Run HTTP server for coordinator"""
        app = web.Application()
        app.router.add_post("/distribute_work", self.handle_distribute_work)
        app.router.add_post("/report_health", self.handle_report_health)
        app.router.add_post("/receive_results", self.handle_receive_results)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.port)
        await site.start()
        
        logger.info(f"Coordinator listening on port {self.port}...")
        
        while True:
            await asyncio.sleep(3600)
    
    async def handle_distribute_work(self, request):
        """Handle a request to distribute work to workers"""
        data = await request.json()
        filepath = data.get("filepath")
        
        if not filepath:
            return web.json_response({"status": "error", "message": "No file path provided"}, status=400)

        chunks = split_file(filepath, num_chunks=len(self.workers))
        logger.info(f"File {filepath} has been split into {len(chunks)} chunks")
        
        for i, (worker_id, worker) in enumerate(self.workers.items()):
            start = i * (len(chunks) // len(self.workers))
            size = (len(chunks) // len(self.workers)) if i < len(self.workers) - 1 else len(chunks) - start
            await self.send_chunk_to_worker(worker, filepath, start, size)
        
        return web.json_response({"status": "success", "message": "Work distributed to workers"})

    async def send_chunk_to_worker(self, worker, filepath: str, start: int, size: int):
        """Send chunk of log file to a worker for processing"""
        logger.info(f"Sending chunk from {start} to {start + size} to Worker {worker['worker_id']}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{worker['url']}/process_chunk", json={"filepath": filepath, "start": start, "size": size}) as resp:
                    if resp.status == 200:
                        logger.info(f"Chunk sent successfully to Worker {worker['worker_id']}")
                    else:
                        logger.error(f"Failed to send chunk to Worker {worker['worker_id']}, status code: {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error while sending chunk to Worker {worker['worker_id']}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while sending chunk to Worker {worker['worker_id']}: {e}")

    async def handle_report_health(self, request):
        """Handle health reports from workers"""
        data = await request.json()
        worker_id = data.get("worker_id")
        
        if worker_id:
            logger.info(f"Worker {worker_id} is healthy")
            if worker_id in self.failed_workers:
                self.failed_workers.remove(worker_id)
            return web.json_response({"status": "healthy"})
        
        return web.json_response({"status": "error", "message": "Missing worker_id"}, status=400)

    async def handle_receive_results(self, request):
        """Receive the results from workers and aggregate them"""
        try:
            data = await request.json()
            logger.info(f"Received data: {data}")
            worker_id = data.get("worker_id")
            metrics = data.get("metrics")
            
            if worker_id and metrics:
                self.results[worker_id] = metrics
                logger.info(f"Received results from Worker {worker_id}: {metrics}")
                
                if len(self.results) == len(self.workers):
                    aggregated_metrics = self.aggregate_results()
                    logger.info(f"All workers completed. Aggregated metrics: {aggregated_metrics}")
                    return web.json_response({"status": "success", "aggregated_metrics": aggregated_metrics})
                return web.json_response({"status": "success", "message": "Results received"})
            else:
                logger.error("Missing worker_id or metrics in received results")
                return web.json_response({"status": "error", "message": "Missing worker_id or metrics"}, status=400)
        except Exception as e:
            logger.error(f"Error processing received results: {e}")
            return web.json_response({"status": "error", "message": "Internal server error"}, status=500)

    def aggregate_results(self) -> Dict:
        """Aggregate results from all workers"""
        aggregated = {
            "error_rate": 0.0,
            "avg_response_time": 0.0,
            "request_count_per_second": 0.0,
        }
        
        # Calculating average error rate, average response time, etc.
        for worker_metrics in self.results.values():
            aggregated["error_rate"] += worker_metrics.get("error_rate", 0.0)
            aggregated["avg_response_time"] += worker_metrics.get("avg_response_time", 0.0)
            aggregated["request_count_per_second"] += worker_metrics.get("request_count_per_second", 0.0)
        
        # Normalize if necessary
        num_workers = len(self.results)
        aggregated["error_rate"] /= num_workers
        aggregated["avg_response_time"] /= num_workers
        aggregated["request_count_per_second"] /= num_workers
        
        return aggregated
    
    async def process_file(self, filepath: str):
        """Distribute work and wait for results"""
        request = AsyncMock()
        request.json.return_value = {"filepath": filepath}
        await self.handle_distribute_work(request)
        
        # Waiting for all results to be aggregated
        while len(self.results) < len(self.workers):
            await asyncio.sleep(1)
        
        return self.aggregate_results()
    
    async def start(self):
        """Start the coordinator server"""
        await self.run_server()

    def add_worker(self, worker_id: str, worker_url: str) -> None:
        """Add a worker to the coordinator"""
        self.workers[worker_id] = {"worker_id": worker_id, "url": worker_url}
        logger.info(f"Worker {worker_id} added with URL {worker_url}")
    
    def remove_worker(self, worker_id: str) -> None:
        """Remove a worker and handle failure"""
        if worker_id in self.workers:
            del self.workers[worker_id]
            self.failed_workers.add(worker_id)
            logger.warning(f"Worker {worker_id} removed due to failure")


async def main():
    parser = argparse.ArgumentParser(description="Log Analyzer Coordinator")
    parser.add_argument("--port", type=int, default=8000, help="Coordinator port")
    args = parser.parse_args()

    coordinator = Coordinator(port=args.port)
    
    # Eg of Add workers to the coordinator
    coordinator.add_worker("worker1", "http://localhost:8001")
    coordinator.add_worker("worker2", "http://localhost:8002")
    coordinator.add_worker("worker3", "http://localhost:8003")
    
    await coordinator.start()

if __name__ == "__main__":
    asyncio.run(main())

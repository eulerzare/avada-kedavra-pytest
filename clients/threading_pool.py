from queue import Queue, Empty
from threading import Thread
from typing import List, Any

from clients.base import BaseGrpcClient


class ThreadingClientPool:
    def __init__(self, num_of_workers: int):
        self.num_of_workers = num_of_workers
        self.clients: List[BaseGrpcClient] = [BaseGrpcClient() for _ in range(self.num_of_workers)]
        self.workers: List[Thread] = [
            Thread(target=self._worker_main_loop, args=(i,), daemon=True) for i in range(self.num_of_workers)
        ]
        self.watchdog: Thread = Thread(target=self._watchdog, daemon=True)
        self.work_queues = Queue()
        self.is_running = True
        self.jobs_started = False
        self.jobs_ended = False

        for worker in self.workers:
            worker.start()
        self.watchdog.start()

    def apply_async(self, method: str, arg_list: List[Any]) -> None:
        for arg in arg_list:
            self.work_queues.put((method, arg))
        self.jobs_started = True

    def _watchdog(self):
        while self.is_running:
            if not self.jobs_started:
                continue

            if self.work_queues.empty():
                break
        self.jobs_ended = True

    def _worker_main_loop(self, shard_id: int):
        client = self.clients[shard_id]
        while self.is_running:
            try:
                method, args = self.work_queues.get(timeout=1)
                func = getattr(client, method)
                func(args)

            except Empty:
                break
            except Exception:
                continue

    def join(self):
        for worker in self.workers:
            worker.join()

from multiprocessing import Pool
from typing import List, Any

import grpc
from decouple import config

from protobuf import transactions_pb2_grpc

host = config("GRPC_HOST", cast=str)
port = config("GRPC_PORT", cast=int)
channel = grpc.insecure_channel(f"{host}:{port}")
transaction_stub = transactions_pb2_grpc.TransactionServiceStub(channel)


def to_do(request):
    transaction_stub.SubmitTransaction(request)


class MultiprocessingClientPool:
    def __init__(self, num_of_workers: int, client):
        self.num_of_workers = num_of_workers
        self.client = client()
        self.pool: Pool = Pool(processes=self.num_of_workers)

    def map(self, method: str, arg_list: List[Any]) -> None:
        self.pool.map(getattr(self.client, method), arg_list)
        # self.pool.map(to_do, arg_list)

    def join(self):
        self.pool.close()
        self.pool.join()

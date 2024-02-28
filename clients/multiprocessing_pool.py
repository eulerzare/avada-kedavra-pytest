import random
import time
from multiprocessing import Pool
from typing import List, Any

import grpc
from decouple import config

from protobuf import transactions_pb2_grpc

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from thrift_classes.transactions.TransactionService import Client
from thrift_classes.transactions.ttypes import Transaction as ThriftTransaction
from thrift_classes.transactions.ttypes import TransactionBulk as ThriftTransactionBulk

# host = config("GRPC_HOST", cast=str)
# port = config("GRPC_PORT", cast=int)
# transaction_stubs = []
# for i in range(16):
#     channel = grpc.insecure_channel(f"{host}:{port}")
#     transaction_stubs.append(transactions_pb2_grpc.TransactionServiceStub(channel))
#
#
# def to_do(request):
#     random.choice(transaction_stubs).SubmitTransaction(request)


host = config("THRIFT_HOST", cast=str)
port = config("THRIFT_PORT", cast=int)
transport = TSocket.TSocket(host, port)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Client(protocol)
transport.open()


def to_do(request):
    # random.choice(transaction_stubs).SubmitTransaction(request)
    transaction1 = ThriftTransaction(
        number=0,
        amount=100,
        freezeAmount=50,
        currency="usdt",
        entity="internal",
        subsidiaryAccount="main",
        entityType=1,
        minAmount=1,
        description="first transaction",
    )
    transaction2 = ThriftTransaction(
        number=1,
        amount=200,
        freezeAmount=50,
        currency="usdt",
        entity="internal",
        subsidiaryAccount="main",
        entityType=1,
        minAmount=1,
        description="second transaction",
    )
    transaction3 = ThriftTransaction(
        number=2,
        amount=300,
        freezeAmount=50,
        currency="usdt",
        entity="internal",
        subsidiaryAccount="main",
        entityType=1,
        minAmount=1,
        description="third transaction",
    )

    request = ThriftTransactionBulk(
        uniqueId="this_is_unique",
        timestamp=int(time.time()),
        objectId=1,
        eventType="new",
        transactions=[transaction1, transaction2, transaction3]
    )
    client.submitTransaction(request)


class MultiprocessingClientPool:
    def __init__(self, num_of_workers: int, client):
        self.num_of_workers = num_of_workers
        self.client = client()
        self.pool: Pool = Pool(processes=self.num_of_workers)

    def map(self, method: str, arg_list: List[Any]) -> None:
        # self.pool.map(getattr(self.client, method), arg_list)
        self.pool.map(to_do, [0 for i in arg_list])

    def join(self):
        self.pool.close()
        self.pool.join()

    def __del__(self):
        self.pool.close()

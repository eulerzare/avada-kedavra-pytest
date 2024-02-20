import time
import unittest

from clients.base import BaseGrpcClient, BaseWebserverClient
from clients.threading_pool import ThreadingClientPool
from data_classes.transactions import Transaction, TransactionBulk

from protobuf import transactions_pb2


class BaseConcurrentTest(unittest.TestCase):
    def setUp(self):
        self.threading_client = ThreadingClientPool(16, BaseWebserverClient)

    def test_submit_transaction_grpc(self):
        transaction1 = transactions_pb2.Transaction(
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
        transaction2 = transactions_pb2.Transaction(
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
        transaction3 = transactions_pb2.Transaction(
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

        bulk_transaction = transactions_pb2.TransactionBulk(
            uniqueId="this_is_unique",
            timestamp=int(time.time()),
            objectId=1,
            eventType="new",
            transactions=[transaction1, transaction2, transaction3]
        )
        self.threading_client.apply_async("submit_transaction", [bulk_transaction] * 1000)
        start_time = time.time()
        while not self.threading_client.jobs_ended:
            pass
        print(time.time() - start_time)
        self.threading_client.join()

    def test_submit_transaction_webserver(self):
        transaction1 = Transaction(
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
        transaction2 = Transaction(
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
        transaction3 = Transaction(
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

        bulk_transaction = TransactionBulk(
            uniqueId="this_is_unique",
            timestamp=int(time.time()),
            objectId=1,
            eventType="new",
            transactions=[transaction1, transaction2, transaction3]
        )
        self.threading_client.apply_async("submit_transaction", [bulk_transaction] * 1000)
        start_time = time.time()
        while not self.threading_client.jobs_ended:
            pass
        print(time.time() - start_time)
        self.threading_client.join()

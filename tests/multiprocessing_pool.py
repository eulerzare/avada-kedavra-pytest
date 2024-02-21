import time
import unittest

from clients.base import BaseGrpcClient, BaseWebserverClient, BaseThriftClient
from clients.multiprocessing_pool import MultiprocessingClientPool
from data_classes.transactions import Transaction, TransactionBulk
from thrift_classes.transactions.ttypes import Transaction as ThriftTransaction
from thrift_classes.transactions.ttypes import TransactionBulk as ThriftTransactionBulk

from protobuf import transactions_pb2


class BaseMultiprocessTest(unittest.TestCase):
    def setUp(self):
        self.multiprocessing_client = MultiprocessingClientPool(16, BaseWebserverClient)

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
        start_time = time.time()
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 10000)
        self.multiprocessing_client.join()
        print(time.time() - start_time)

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
        start_time = time.time()
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 10000)
        self.multiprocessing_client.join()
        print(time.time() - start_time)

    def test_submit_transaction_thrift(self):
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

        bulk_transaction = ThriftTransactionBulk(
            uniqueId="this_is_unique",
            timestamp=int(time.time()),
            objectId=1,
            eventType="new",
            transactions=[transaction1, transaction2, transaction3]
        )
        start_time = time.time()
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 10000)
        self.multiprocessing_client.join()
        print(time.time() - start_time)

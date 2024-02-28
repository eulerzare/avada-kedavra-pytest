import time
import unittest
import uuid
from multiprocessing import Pool

from decouple import config
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

from clients.base import BaseGrpcClient, BaseWebserverClient, BaseThriftClient
from clients.multiprocessing_pool import MultiprocessingClientPool
from data_classes.transactions import Transaction, TransactionBulk
from thrift_classes.transactions.TransactionService import Client
from thrift_classes.transactions.ttypes import Transaction as ThriftTransaction
from thrift_classes.transactions.ttypes import TransactionBulk as ThriftTransactionBulk

from protobuf import transactions_pb2

host = config("THRIFT_HOST", cast=str)
port = config("THRIFT_PORT", cast=int)
transport = TSocket.TSocket(host, port)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Client(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "TransactionService"))
transport.open()

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


def to_do(unique_id):
    request = ThriftTransactionBulk(
        uniqueId=unique_id,
        timestamp=1234,
        objectId=1,
        eventType="new",
        transactions=[transaction1, transaction2, transaction3]
    )
    return client.submitTransaction(request)


def to_do_memory(none):
    request = ThriftTransactionBulk(
        uniqueId="0",
        timestamp=1234,
        objectId=1,
        eventType="new",
        transactions=[transaction1, transaction2, transaction3]
    )
    counter = 0
    start_time_of_batch = time.time()
    while True:
        counter += 1
        request.uniqueId = str(uuid.uuid4())
        client.submitTransaction(request)
        if counter % 10_000 == 0:
            print(time.time() - start_time_of_batch)
            start_time_of_batch = time.time()


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
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 100000)
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
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 100000)
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
            entityType=1,  # margin / main
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
        self.multiprocessing_client.map("submit_transaction", [bulk_transaction] * 100000)
        self.multiprocessing_client.join()
        print(time.time() - start_time)

    def test_all_unique_submitted(self):
        list_of_ids = [str(uuid.uuid4()) for _ in range(100000)]
        list_of_ids = list_of_ids + [list_of_ids[0], list_of_ids[1]]

        pool: Pool = Pool(processes=1)
        start_time = time.time()
        responses = pool.map(to_do, list_of_ids)
        print(time.time() - start_time)
        print([(i, r.message) for i, r in enumerate(responses) if r.message != "Unique Id checked"])
        pool.close()

    def test_memory_leak(self):
        pool: Pool = Pool(processes=12)
        responses = pool.map(to_do_memory, [None] * 12)
        pool.close()

    def tearDown(self):
        del self.multiprocessing_client
        transport.close()

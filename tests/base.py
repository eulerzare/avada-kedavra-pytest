import time
import unittest

from clients.base import BaseGrpcClient

from protobuf import transactions_pb2


class BaseGrpcTest(unittest.TestCase):
    def setUp(self):
        self.grpc_client = BaseGrpcClient()

    def test_submit_transaction(self):
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
        response = self.grpc_client.submit_transaction(bulk_transaction)
        print(response)

    def tearDown(self):
        del self.grpc_client

import pickle
import time
import unittest
import uuid
from multiprocessing import Pool

from decouple import config
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from thrift.transport.TTransport import TTransportException

from thrift_classes.base.ttypes import Genre, AccountType, Currency
from thrift_classes.entities.ttypes import RequestGetEntityAccount
from thrift_classes.transactions.TransactionService import Client as TransactionClient
from thrift_classes.entities.EntityService import Client as EntityClient
from thrift_classes.transactions.ttypes import Transaction
from thrift_classes.transactions.ttypes import TransactionBulk

TEST_INSTANCE = 1

host = config("THRIFT_HOST", cast=str)
port = config("THRIFT_PORT", cast=int)
transport = TSocket.TSocket(host, port)
transport.setTimeout(10000.)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

transaction_client = TransactionClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "TransactionService"))
entity_client = EntityClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "EntityService"))
transport.open()


def submit_transaction_parse_response(request: TransactionBulk):
    try:
        if transaction_client.submitTransaction(request).status == 1:
            return request.uniqueId
        else:
            return None
    except TTransportException:
        return None


def get_entities_accounts(request: RequestGetEntityAccount):
    return entity_client.getEntitiesAccounts(request)


class FaultToleranceTest(unittest.TestCase):
    def prepare_data(self):
        number_of_transactions = 250_000
        entity_id1 = TEST_INSTANCE * 2
        entity_id2 = TEST_INSTANCE * 2 + 1
        usdt_value = 10000.
        number_of_fragments = number_of_transactions * 2
        usdt_fragment = usdt_value / number_of_fragments

        whole_transactions = []
        for i_transaction in range(number_of_transactions):
            trx = list()
            trx.append(
                Transaction(
                    entityId=entity_id1,
                    genre=Genre.MAIN,
                    accountType=AccountType.EXTERNAL,
                    pairId=1,
                    currency=Currency.USDT,
                    amount=str(usdt_fragment),
                    freezeAmount=str(usdt_fragment),
                    minAmount=str(-usdt_value),
                )
            )
            trx.append(
                Transaction(
                    entityId=entity_id2,
                    genre=Genre.MAIN,
                    accountType=AccountType.EXTERNAL,
                    pairId=1,
                    currency=Currency.USDT,
                    amount=str(-usdt_fragment),
                    freezeAmount=str(-usdt_fragment),
                    minAmount=str(-usdt_value),
                )
            )
            whole_transactions.append(
                TransactionBulk(
                    uniqueId=str(uuid.uuid4()),
                    timestamp=1234,
                    transactions=trx
                )
            )

        with open("data.spec", "wb") as f:
            pickle.dump(whole_transactions, f)

    def loadtest(self):
        number_of_workers = 8

        with open("data.spec", "rb") as f:
            whole_transactions = pickle.load(f)

        pool: Pool = Pool(processes=number_of_workers)
        start_time = time.time()
        responses = pool.map(submit_transaction_parse_response, whole_transactions)
        print(time.time() - start_time)
        pool.close()

        responses = [r for r in responses if r is not None]
        with open("responses.spec", "wb") as f:
            pickle.dump(responses, f)

    def check_correctness(self):
        entity_id1 = TEST_INSTANCE * 2
        entity_id2 = TEST_INSTANCE * 2 + 1
        number_of_workers = 8

        resp = get_entities_accounts(
            RequestGetEntityAccount(
                uniqueIds=[entity_id1, entity_id2]
            )
        )
        print("accounts before")
        for a in resp.entityAccount:
            print(a)

        with open("data.spec", "rb") as f:
            whole_transactions = pickle.load(f)

        with open("responses.spec", "rb") as f:
            responses = pickle.load(f)

        whole_transactions = [item for item in whole_transactions if item.uniqueId in responses]
        pool: Pool = Pool(processes=number_of_workers)
        pool.map(submit_transaction_parse_response, whole_transactions)
        pool.close()

        resp = get_entities_accounts(
            RequestGetEntityAccount(
                uniqueIds=[entity_id1, entity_id2]
            )
        )
        print("accounts after")
        for a in resp.entityAccount:
            print(a)

    def tearDown(self):
        transport.close()

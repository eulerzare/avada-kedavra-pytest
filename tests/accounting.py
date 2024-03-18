import time
import unittest
import uuid
from decimal import Decimal
from multiprocessing import Pool

from decouple import config
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

# from thrift_classes.accounts.ttypes import AddAccount
from thrift_classes.base.ttypes import Genre, AccountType, Currency
# from thrift_classes.currencies.ttypes import AddCurrency
# from thrift_classes.accounts.AccountService import Client as AccountClient
# from thrift_classes.currencies.CurrencyService import Client as CurrencyClient
from thrift_classes.entities.ttypes import RequestGetEntityAccount
from thrift_classes.transactions.TransactionService import Client as TransactionClient
from thrift_classes.entities.EntityService import Client as EntityClient
from thrift_classes.transactions.ttypes import Transaction
from thrift_classes.transactions.ttypes import TransactionBulk

host = config("THRIFT_HOST", cast=str)
port = config("THRIFT_PORT", cast=int)
transport = TSocket.TSocket(host, port)
transport.setTimeout(10000.)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

transaction_client = TransactionClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "TransactionService"))
# currency_client = CurrencyClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "CurrencyService"))
# account_client = AccountClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "AccountService"))
entity_client = EntityClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "EntityService"))
transport.open()


def submit_transaction(request: TransactionBulk):
    return transaction_client.submitTransaction(request)


# def add_currency(request: AddCurrency):
#     return currency_client.addCurrency(request)
#
#
# def add_account(request: AddAccount):
#     return account_client.addAccount(request)
#
#
# def add_entity(request: AddEntity):
#     return entity_client.addEntity(request)


def get_entities_accounts(request: RequestGetEntityAccount):
    return entity_client.getEntitiesAccounts(request)


class AccountingTest(unittest.TestCase):

    def test_add_currency(self):
        pass
        # r = AddCurrency(
        #     symbol="usdT",
        #     name="tether",
        # )
        # print(add_currency(r))

    def test_add_account(self):
        # r = AddAccount(
        #     id=1,
        #     currencySymbol="Usdt",
        #     genre=Genre.MAIN,
        #     accountType=AccountType.EXTERNAL
        # )
        # print(add_account(r))

        pass
        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(add_account, [AddAccount(id=i, currency_id=1) for i in range(100_000, 200_000)])
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_add_entity(self):
        pass
        # r = AddEntity(
        #     uniqueId="0"
        # )
        # print(add_entity(r))
        #
        # r = AddEntity(
        #     uniqueId="1"
        # )
        # print(add_entity(r))

        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(add_account, [AddAccount(id=i, currency_id=1) for i in range(100_000, 200_000)])
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_transaction_submitted(self):
        transaction1 = Transaction(
            entityId=0,
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            pairId=1,
            currency=Currency.USDT,
            amount=str(-100),
            freezeAmount=str(-100),
            minAmount=str(-100),
        )
        transaction2 = Transaction(
            entityId=1,
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            pairId=1,
            currency=Currency.USDT,
            amount=str(50),
            freezeAmount=str(50),
            minAmount=str(-100),
        )
        transaction3 = Transaction(
            entityId=1,
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            pairId=1,
            currency=Currency.USDT,
            amount=str(50),
            freezeAmount=str(50),
            minAmount=str(-100),
        )
        request = TransactionBulk(
            uniqueId=str(uuid.uuid4()),
            timestamp=1234,
            transactions=[transaction1, transaction2, transaction3]
        )

        print(submit_transaction(request))

        # requests = [TransactionBulk(uniqueId=str(uuid.uuid4()), timestamp=1234, transactions=[transaction1, transaction2]) for i in range(200_000)]
        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(submit_transaction, requests)
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_get_entities_accounts(self):
        r = RequestGetEntityAccount(
            uniqueIds=[0, 1, 2]
        )
        resp = get_entities_accounts(r)
        for a in resp.entityAccount:
            print(a)

        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(add_account, [AddAccount(id=i, currency_id=1) for i in range(100_000, 200_000)])
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_benchmark1(self):
        number_of_transactions = 100_000
        number_of_entities = number_of_transactions
        number_of_batches = 20_000
        number_of_workers = 8
        usdt_value = 10000.
        btc_value = .1
        eth_value = 1.

        number_of_entities_in_batch = number_of_entities // number_of_batches

        # add_currency(AddCurrency(symbol="usdt", name="tether"))
        # add_currency(AddCurrency(symbol="btc", name="bitcoin"))
        # add_currency(AddCurrency(symbol="eth", name="ethereum"))

        # whole_entities = [AddEntity(uniqueId=str(i)) for i in range(number_of_entities)]
        # pool: Pool = Pool(processes=number_of_workers)
        # start_time = time.time()
        # pool.map(add_entity, whole_entities)
        # print(time.time() - start_time)
        # pool.close()

        whole_transactions = []
        for i_level in range(number_of_entities_in_batch):
            sign1 = -1. if i_level % 2 == 0 else 1.
            sign2 = 1. if i_level % 2 == 0 else -1.
            for i_batch in range(number_of_batches):
                trx = list()
                trx.append(
                    Transaction(
                        entityId=0 + i_batch * number_of_entities_in_batch,
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        pairId=1,
                        currency=Currency.USDT,
                        amount=str(usdt_value * sign1),
                        freezeAmount=str(usdt_value * sign1),
                        minAmount=str(-usdt_value),
                    )
                )
                trx.append(
                    Transaction(
                        entityId=0 + i_batch * number_of_entities_in_batch,
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        pairId=1,
                        currency=Currency.BTC,
                        amount=str(btc_value * sign1),
                        freezeAmount=str(btc_value * sign1),
                        minAmount=str(-btc_value),
                    )
                )
                trx.append(
                    Transaction(
                        entityId=0 + i_batch * number_of_entities_in_batch,
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        pairId=1,
                        currency=Currency.ETH,
                        amount=str(eth_value * sign1),
                        freezeAmount=str(eth_value * sign1),
                        minAmount=str(-eth_value),
                    )
                )
                for i_entity_in_batch in range(1, number_of_entities_in_batch):
                    trx.append(
                        Transaction(
                            entityId=i_entity_in_batch + i_batch * number_of_entities_in_batch,
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            pairId=1,
                            currency=Currency.USDT,
                            amount=str(usdt_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(usdt_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            minAmount=str(-usdt_value),
                        )
                    )
                    trx.append(
                        Transaction(
                            entityId=i_entity_in_batch + i_batch * number_of_entities_in_batch,
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            pairId=1,
                            currency=Currency.BTC,
                            amount=str(btc_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(btc_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            minAmount=str(-btc_value),
                        )
                    )
                    trx.append(
                        Transaction(
                            entityId=i_entity_in_batch + i_batch * number_of_entities_in_batch,
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            pairId=1,
                            currency=Currency.ETH,
                            amount=str(eth_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(eth_value / (number_of_entities_in_batch - 1) * sign2).zfill(7),
                            minAmount=str(-eth_value),
                        )
                    )
                whole_transactions.append(
                    TransactionBulk(
                        uniqueId=str(uuid.uuid4()),
                        timestamp=1234,
                        transactions=trx
                    )
                )
        # print(submit_transaction(whole_transactions[0]))

        pool: Pool = Pool(processes=number_of_workers)
        start_time = time.time()
        responses = pool.map(submit_transaction, whole_transactions, number_of_batches)
        print(time.time() - start_time)
        # for rr in responses:
        #     print(rr)
        pool.close()

        resp = get_entities_accounts(
            RequestGetEntityAccount(
                uniqueIds=[0, 1, 2, 3, 4, 5, 6]
            )
        )
        for a in resp.entityAccount:
            print(a)

    def test_threadsafe1(self):
        number_of_transactions = 250_000
        number_of_workers = 8
        usdt_value = 10000.
        number_of_fragments = 250_000
        usdt_fragment = usdt_value / number_of_fragments

        # add_currency(AddCurrency(symbol="usdt", name="tether"))
        #
        # add_entity(AddEntity(uniqueId="0"))
        # add_entity(AddEntity(uniqueId="1"))

        whole_transactions = []
        for i_transaction in range(number_of_transactions):
            trx = list()
            trx.append(
                Transaction(
                    entityId=0,
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
                    entityId=1,
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
        # print(submit_transaction(whole_transactions[0]))

        pool: Pool = Pool(processes=number_of_workers)
        start_time = time.time()
        responses = pool.map(submit_transaction, whole_transactions)
        print(responses[0])
        print("number of successful transactions: ", sum([r.status == 1 for r in responses]))
        print(time.time() - start_time)
        # for rr in responses:
        #     print(rr)
        pool.close()

        resp = get_entities_accounts(
            RequestGetEntityAccount(
                uniqueIds=[0, 1]
            )
        )
        for a in resp.entityAccount:
            print(a)

    def tearDown(self):
        transport.close()

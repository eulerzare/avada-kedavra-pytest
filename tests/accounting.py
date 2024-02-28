import time
import unittest
import uuid
from multiprocessing import Pool

from decouple import config
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

from thrift_classes.accounts.ttypes import AddAccount
from thrift_classes.base.ttypes import Genre, AccountType
from thrift_classes.currencies.ttypes import AddCurrency
from thrift_classes.accounts.AccountService import Client as AccountClient
from thrift_classes.currencies.CurrencyService import Client as CurrencyClient
from thrift_classes.traders.ttypes import AddTrader
from thrift_classes.transactions.TransactionService import Client as TransactionClient
from thrift_classes.traders.TraderService import Client as TraderClient
from thrift_classes.transactions.ttypes import Transaction
from thrift_classes.transactions.ttypes import TransactionBulk

host = config("THRIFT_HOST", cast=str)
port = config("THRIFT_PORT", cast=int)
transport = TSocket.TSocket(host, port)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

transaction_client = TransactionClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "TransactionService"))
currency_client = CurrencyClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "CurrencyService"))
account_client = AccountClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "AccountService"))
trader_client = TraderClient(TMultiplexedProtocol.TMultiplexedProtocol(protocol, "TraderService"))
transport.open()


def submit_transaction(request: TransactionBulk):
    return transaction_client.submitTransaction(request)


def add_currency(request: AddCurrency):
    return currency_client.addCurrency(request)


def add_account(request: AddAccount):
    return account_client.addAccount(request)


def add_trader(request: AddTrader):
    return trader_client.addTrader(request)


class AccountingTest(unittest.TestCase):
    def test_unique_transaction_submitted(self):
        transaction1 = Transaction(
            traderId="0",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
            amount=100,
            freezeAmount=100,
            minAmount=-100,
        )
        transaction2 = Transaction(
            traderId="0",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
            amount=-100,
            freezeAmount=-100,
            minAmount=-100,
        )
        list_of_ids = [str(uuid.uuid4()) for _ in range(100000)]
        list_of_ids = list_of_ids + [list_of_ids[0], list_of_ids[1]]
        requests = [TransactionBulk(
            uniqueId=unique_id,
            timestamp=1234,
            transactions=[transaction1, transaction2]
        ) for unique_id in list_of_ids]

        pool: Pool = Pool(processes=12)
        start_time = time.time()
        responses = pool.map(submit_transaction, requests)
        print(time.time() - start_time)
        print([(i, r.message) for i, r in enumerate(responses) if r.message != "Unique Id checked"])
        pool.close()

    def test_add_currency(self):
        r = AddCurrency(
            symbol="usdT",
            name="tether",
        )
        print(add_currency(r))

    def test_add_account(self):
        r = AddAccount(
            id=1,
            currencySymbol="Usdt",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL
        )
        print(add_account(r))

        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(add_account, [AddAccount(id=i, currency_id=1) for i in range(100_000, 200_000)])
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_add_trader(self):
        r = AddTrader(
            uniqueId="0"
        )
        print(add_trader(r))

        # pool: Pool = Pool(processes=12)
        # start_time = time.time()
        # responses = pool.map(add_account, [AddAccount(id=i, currency_id=1) for i in range(100_000, 200_000)])
        # print(time.time() - start_time)
        # # for rr in responses:
        # #     print(rr)
        # pool.close()

    def test_transaction_submitted(self):
        transaction1 = Transaction(
            traderId="0",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
            amount=100,
            freezeAmount=100,
            minAmount=-100,
        )
        transaction2 = Transaction(
            traderId="0",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
            amount=-100,
            freezeAmount=-100,
            minAmount=-100,
        )
        # request = TransactionBulk(
        #     uniqueId=str(uuid.uuid4()),
        #     timestamp=1234,
        #     transactions=[transaction1, transaction2]
        # )

        # print(submit_transaction(request))
        requests = [TransactionBulk(uniqueId=str(uuid.uuid4()), timestamp=1234, transactions=[transaction1, transaction2]) for i in range(200_000)]

        pool: Pool = Pool(processes=12)
        start_time = time.time()
        responses = pool.map(submit_transaction, requests)
        print(time.time() - start_time)
        # for rr in responses:
        #     print(rr)
        pool.close()

    def tearDown(self):
        transport.close()

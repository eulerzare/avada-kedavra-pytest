import time
import unittest
import uuid
from decimal import Decimal
from multiprocessing import Pool

from decouple import config
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

from thrift_classes.accounts.ttypes import AddAccount
from thrift_classes.base.ttypes import Genre, AccountType
from thrift_classes.currencies.ttypes import AddCurrency
from thrift_classes.accounts.AccountService import Client as AccountClient
from thrift_classes.currencies.CurrencyService import Client as CurrencyClient
from thrift_classes.traders.ttypes import AddTrader, RequestGetTraderAccount
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


def get_traders_accounts(request: RequestGetTraderAccount):
    return trader_client.getTradersAccounts(request)


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

    def test_add_trader(self):
        r = AddTrader(
            uniqueId="0"
        )
        print(add_trader(r))

        r = AddTrader(
            uniqueId="1"
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
            amount=str(-100),
            freezeAmount=str(-100),
            minAmount=str(-100),
        )
        transaction2 = Transaction(
            traderId="1",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
            amount=str(50),
            freezeAmount=str(50),
            minAmount=str(-100),
        )
        transaction3 = Transaction(
            traderId="1",
            genre=Genre.MAIN,
            accountType=AccountType.EXTERNAL,
            currencySymbol="usdt",
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

    def test_get_traders_accounts(self):
        r = RequestGetTraderAccount(
            traderIds=["0", "1", "2"]
        )
        resp = get_traders_accounts(r)
        for a in resp.traderAccount:
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
        number_of_traders = number_of_transactions
        number_of_batches = 20_000
        number_of_workers = 8
        usdt_value = 10000.
        btc_value = .1
        eth_value = 1.

        number_of_traders_in_batch = number_of_traders // number_of_batches

        add_currency(AddCurrency(symbol="usdt", name="tether"))
        add_currency(AddCurrency(symbol="btc", name="bitcoin"))
        add_currency(AddCurrency(symbol="eth", name="ethereum"))

        whole_traders = [AddTrader(uniqueId=str(i)) for i in range(number_of_traders)]
        pool: Pool = Pool(processes=number_of_workers)
        start_time = time.time()
        pool.map(add_trader, whole_traders)
        print(time.time() - start_time)
        pool.close()

        whole_transactions = []
        for i_level in range(number_of_traders_in_batch):
            sign1 = -1. if i_level % 2 == 0 else 1.
            sign2 = 1. if i_level % 2 == 0 else -1.
            for i_batch in range(number_of_batches):
                trx = list()
                trx.append(
                    Transaction(
                        traderId=str(0 + i_batch * number_of_batches),
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        currencySymbol="usdt",
                        amount=str(usdt_value * sign1),
                        freezeAmount=str(usdt_value * sign1),
                        minAmount=str(-usdt_value),
                    )
                )
                trx.append(
                    Transaction(
                        traderId=str(0 + i_batch * number_of_batches),
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        currencySymbol="btc",
                        amount=str(btc_value * sign1),
                        freezeAmount=str(btc_value * sign1),
                        minAmount=str(-btc_value),
                    )
                )
                trx.append(
                    Transaction(
                        traderId=str(0 + i_batch * number_of_batches),
                        genre=Genre.MAIN,
                        accountType=AccountType.EXTERNAL,
                        currencySymbol="eth",
                        amount=str(eth_value * sign1),
                        freezeAmount=str(eth_value * sign1),
                        minAmount=str(-eth_value),
                    )
                )
                for i_trader_in_batch in range(1, number_of_traders_in_batch):
                    trx.append(
                        Transaction(
                            traderId=str(i_trader_in_batch + i_batch * number_of_batches),
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            currencySymbol="usdt",
                            amount=str(usdt_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(usdt_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
                            minAmount=str(-usdt_value),
                        )
                    )
                    trx.append(
                        Transaction(
                            traderId=str(i_trader_in_batch + i_batch * number_of_batches),
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            currencySymbol="btc",
                            amount=str(btc_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(btc_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
                            minAmount=str(-btc_value),
                        )
                    )
                    trx.append(
                        Transaction(
                            traderId=str(i_trader_in_batch + i_batch * number_of_batches),
                            genre=Genre.MAIN,
                            accountType=AccountType.EXTERNAL,
                            currencySymbol="eth",
                            amount=str(eth_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
                            freezeAmount=str(eth_value / (number_of_traders_in_batch - 1) * sign2).zfill(7),
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
        responses = pool.map(submit_transaction, whole_transactions)
        print(time.time() - start_time)
        # for rr in responses:
        #     print(rr)
        pool.close()

        resp = get_traders_accounts(
            RequestGetTraderAccount(
                traderIds=["0", "1", "2", "3", "4", "5", "6"]
            )
        )
        for a in resp.traderAccount:
            print(a)

    def tearDown(self):
        transport.close()

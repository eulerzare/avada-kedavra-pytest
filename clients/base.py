from typing import Dict

import grpc
import requests
from decouple import config
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from data_classes.transactions import TransactionBulk
from protobuf import transactions_pb2_grpc, transactions_pb2
from thrift_classes.transactions.TransactionService import Client
from thrift_classes.transactions.ttypes import TransactionBulk as ThriftTransactionBulk


class BaseGrpcClient:
    def __init__(self):
        self.host = config("GRPC_HOST", cast=str)
        self.port = config("GRPC_PORT", cast=int)

        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.transaction_stub = transactions_pb2_grpc.TransactionServiceStub(self.channel)

    def submit_transaction(self, request: transactions_pb2.Transaction) -> transactions_pb2.StatusResponse:
        return self.transaction_stub.SubmitTransaction(request)

    def __del__(self):
        self.channel.close()


class BaseWebserverClient:
    def __init__(self):
        self.host = config("WEBSERVER_HOST", cast=str)
        self.port = config("WEBSERVER_PORT", cast=int)
        self.base_url = f"http://{self.host}:{self.port}"

        self.session = requests.Session()

    def submit_transaction(self, request: TransactionBulk) -> Dict:
        url = f"{self.base_url}/submit-transaction"
        return self.session.post(url, json=request.model_dump()).json()


class BaseThriftClient:
    def __init__(self):
        self.host = config("THRIFT_HOST", cast=str)
        self.port = config("THRIFT_PORT", cast=int)
        self.transport = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        self.client = Client(protocol)
        self.transport.open()

    def submit_transaction(self, request: ThriftTransactionBulk):
        return self.client.submitTransaction(request)

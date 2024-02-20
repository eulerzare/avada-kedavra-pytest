from typing import Dict

import grpc
import requests
from decouple import config

from data_classes.transactions import TransactionBulk, StatusResponse
from protobuf import transactions_pb2_grpc, transactions_pb2


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
        path = f"{self.base_url}/submit-transaction"
        return self.session.post(path, json=request.model_dump()).json()

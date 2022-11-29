import unittest
import decimal
from fx_py_sdk.grpc_client import GRPCClient, DEFAULT_GRPC_NONE, DEFAULT_DEC
from google.protobuf.timestamp_pb2 import Timestamp
import base64
import hashlib

class MyTestCase(unittest.TestCase):

    def test_decimal(self):
        base_quantity = decimal.Decimal('1.281999999999997730')
        base_quantity = base_quantity * decimal.Decimal(DEFAULT_DEC)
        base_quantity = str(base_quantity)
        base_quantity_split = base_quantity.split('.', 1)
        print(base_quantity_split)


    def test_decimal_neg(self):
        base_quantity = decimal.Decimal('-1.281999999999997730')
        base_quantity = base_quantity * decimal.Decimal(DEFAULT_DEC)
        base_quantity = str(base_quantity)
        base_quantity_split = base_quantity.split('.', 1)
        print(base_quantity_split)


    def test_proto_time(self):
        time1 = "2021-12-24T07:09:12.504154Z"
        time2 = Timestamp()
        time2.FromJsonString(time1)
        print(time2)
        time3 = Timestamp().FromJsonString(time1)  # return None
        print(time3)


    def test_txHash(self):
        txHash = "ClUKUwoWL2Z4LmRleC5Nc2dDcmVhdGVPcmRlchI5ChQSAialXAf769jHo6c6hUOLeOAJpxIJVFNMQTpVU0RUGAIiCTkxMDEwMDAwMCoHMTE5OTk5OTAKEmcKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQPTv2q291gispQoYVcXwNSBVwZ34vDbQDHZ6EfR+VZQLBIECgIIARgDEhMKDAoEVVNEVBIEMzAwMBDAlrECGkDIFwI42lN772BkjtwjLK7G5omFXerBs0u1TU7UTxlUyjnaj5AUVGUC71WqNWGhWEETkGWpW/Tfpb0a0i5tJgBt"
        txHashByte = base64.b64decode(txHash)
        print(txHashByte)
        data_sha = hashlib.sha256(txHashByte).hexdigest().upper()
        print(data_sha)
import re
import threading
import time
from typing import List

from eth_account import Account
from fx_py_sdk.grpc_client import GRPCClient
from fx_py_sdk.builder import TxBuilder
from fx_py_sdk.codec.cosmos.base.v1beta1.coin_pb2 import Coin
import decimal
from fx_py_sdk.codec.cosmos.tx.v1beta1.service_pb2 import BROADCAST_MODE_BLOCK, BROADCAST_MODE_SYNC
from google.protobuf.json_format import MessageToJson

BASE_ASSET = "NFLX"
mnemonic1 = ""
mnemonic2 = ""

def main():
    client = GRPCClient(f"https://testnet-{BASE_ASSET.lower()}-grpc-normal.marginx.io:9090")
    loop_number = 100
    t0 = time.time()

    def sell_order():
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(mnemonic1)
        print(account.address)

        chain_id = client.query_chain_id()
        print('chain_id:', chain_id)

        account_info = client.query_account_info(account.address)
        print('account number:', account_info.account_number,
              'sequence:', account_info.sequence)

        tx_builder = TxBuilder(account, None, chain_id, account_info.account_number,
                               Coin(amount='600', denom='USDT'))

        account_info = client.query_account_info(account.address)
        print('account number:', account_info.account_number,
              'sequence:', account_info.sequence)
        sequence = account_info.sequence
        for i in range(0, loop_number):
            tx_response = client.create_order(tx_builder, BASE_ASSET + ":USDT", "SELL", decimal.Decimal(
                900), decimal.Decimal(1.2), 5, sequence, mode=BROADCAST_MODE_SYNC)

            if tx_response.code == 20:
                continue

            if tx_response.code == 32:
                if "account sequence mismatch" in tx_response.raw_log:
                    find = re.findall(r"expected ([0-9]+)", tx_response.raw_log)
                    sequence = int(find[0])
                    continue

            res_str = MessageToJson(tx_response)
            print(res_str)
            sequence = sequence + 1

    def buy_order():
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(mnemonic2)
        print(account.address)

        chain_id = client.query_chain_id()
        print('chain_id:', chain_id)

        account_info = client.query_account_info(account.address)
        print('account number:', account_info.account_number,
              'sequence:', account_info.sequence)

        tx_builder = TxBuilder(account, None, chain_id, account_info.account_number, Coin(
            amount='600', denom='USDT'))

        account_info = client.query_account_info(account.address)
        print('account number:', account_info.account_number,
              'sequence:', account_info.sequence)
        sequence = account_info.sequence
        for i in range(0, loop_number):
            tx_response = client.create_order(tx_builder, BASE_ASSET + ":USDT", "BUY", decimal.Decimal(
                900), decimal.Decimal(1.2), 5, sequence, mode=BROADCAST_MODE_SYNC)

            if tx_response.code == 20:
                continue

            if tx_response.code == 32:
                if "account sequence mismatch" in tx_response.raw_log:
                    find = re.findall(r"expected ([0-9]+)", tx_response.raw_log)
                    sequence = int(find[0])
                    continue

            res_str = MessageToJson(tx_response)
            print(res_str)
            sequence = sequence + 1


    thread_list: List[threading.Thread] = []
    t_sell = threading.Thread(target=sell_order)
    t_buy = threading.Thread(target=buy_order)
    thread_list.append(t_buy)
    thread_list.append(t_sell)
    t_sell.start()
    t_buy.start()
    for t in thread_list:
        t.join()

    t1 = time.time()
    print(f"{t1 - t0:.3f} seconds elapsed")

if __name__ == "__main__":
    main()

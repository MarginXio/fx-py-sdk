from typing import Iterable, NamedTuple
from decimal import Decimal
import os
import logging
import datetime

class EnvVar:
    NETWORK = "NETWORK"
    DB_URI = "DB_URI"


class NetworkENV:
    LOCAL = "local"
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet"

class ChainType:
    FX = "fx"
    Marginx = "marginx"

class DefaultGas:
    FX_GAS_LIMIT = 200000
    MarginX_GAS_LIMIT = 50000000
    FX_GAS_PRICE = "4000000000000"
    MarginX_GAS_PRICE = "60"

class Network:
    LOCAL_RPC = "http://127.0.0.1:26657"
    DEVNET_RPC = "http://44.196.199.119:26657"
    TESTNET_RPC = ""
    MAINNET_RPC = ""

    LOCAL_GRPC = "127.0.0.1:9090"
    DEVNET_GRPC = "44.196.199.119:9090"
    TESTNET_GRPC = ""
    MAINNET_GRPC = ""

    LOCAL_WS = "ws://127.0.0.1:26657/"
    DEVNET_WS = "ws://44.196.199.119:26657/"
    TESTNET_WS = ""
    MAINNET_WS = ""

    @staticmethod
    def get_rpc_url() -> str:
        network = os.environ.get(EnvVar.NETWORK, NetworkENV.DEVNET)
        if network == NetworkENV.LOCAL:
            rpc_url = Network.LOCAL_RPC
        elif network == NetworkENV.DEVNET:
            rpc_url = Network.DEVNET_RPC
        elif network == NetworkENV.TESTNET:
            rpc_url = os.environ.get('TESTNET_RPC_URL', Network.TESTNET_RPC)
            logging.info(rpc_url)
        elif network == NetworkENV.MAINNET:
            rpc_url = Network.MAINNET_RPC
        return rpc_url

    @staticmethod
    def get_grpc_url() -> str:
        network = os.environ.get(EnvVar.NETWORK, NetworkENV.DEVNET)
        if network == NetworkENV.LOCAL:
            grpc_url = Network.LOCAL_GRPC
        elif network == NetworkENV.DEVNET:
            grpc_url = Network.DEVNET_GRPC
        elif network == NetworkENV.TESTNET:
            grpc_url = os.environ.get('TESTNET_GRPC_URL', Network.TESTNET_GRPC)
            logging.info(grpc_url)
        elif network == NetworkENV.MAINNET:
            grpc_url = Network.MAINNET_GRPC
        return grpc_url

    @staticmethod
    def get_ws_url() -> str:
        network = os.environ.get(EnvVar.NETWORK, NetworkENV.DEVNET)
        if network == NetworkENV.LOCAL:
            wss_url = Network.LOCAL_WS
        elif network == NetworkENV.DEVNET:
            wss_url = Network.DEVNET_WS
        elif network == NetworkENV.TESTNET:
            wss_url = os.environ.get('TESTNET_WS_URL', Network.TESTNET_WS)
            logging.info(wss_url)
        elif network == NetworkENV.MAINNET:
            wss_url = Network.MAINNET_WS
        return wss_url

class DB:
    Database = "database"
    User = "user"
    Password = "password"
    Host = "host"
    Port = "port"


class Order(NamedTuple):
    Id: str
    Owner: str
    PairId: str
    Direction: str
    Price: Decimal
    BaseQuantity: Decimal
    QuoteQuantity: Decimal
    FilledQuantity: Decimal
    FilledAvgPrice: Decimal
    Leverage: int
    Status: str
    OrderType: str
    CostFee: Decimal
    LockedFee: Decimal
    FeeDenom: str
    LastFilledQuantity: Decimal = None
    LastUpdated: datetime.datetime = None
    Trades: Iterable = None

class Position(NamedTuple):
    Id: int
    Owner: str
    PairId: str
    Direction: str
    EntryPrice: Decimal
    MarkPrice: Decimal
    LiquidationPrice: Decimal
    BaseQuantity: Decimal
    Margin: Decimal
    Leverage: int
    UnrealizedPnl: Decimal
    MarginRate: Decimal
    InitialMargin: Decimal
    PendingOrderQuantity: Decimal

class Trade(NamedTuple):
    DealPrice: Decimal
    MatchedQuantity: Decimal
    FilledTime: datetime.datetime

class BackEndApi:
    query_order_page = "http://44.195.213.51:30225/api/address/queryOrderPage"

PAIR_IDS = [
    "BTC:USDT",
    "TSLA:USDT",
    "AAPL:USDT",
    "NFLX:USDT",
    "GOOG:USDT",
    "FB:USDT",
    "AMZN:USDT",
    "SPY:USDT",
    "FX:USDT",
    "IWM:USDT",
    "TQQQ:USDT",
]

BASE_URL = "https://trade.testnet.marginx.io/dex/common/"
ORDERBOOK_ENDPOINT = "queryOrderBook"
PRICING_ENDPOINT = "queryPair"
FUNDING_ENDPOINT = "getFundingRateRealTime"

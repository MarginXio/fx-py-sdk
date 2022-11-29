import base64
import hashlib
from collections import defaultdict, deque
import datetime
from typing import Callable
import websocket
import json
import logging
import os
from fx_py_sdk import constants
import threading
from fx_py_sdk.model.block import *
from fx_py_sdk.model.model import *
from fx_py_sdk.model.crud import *
from fx_py_sdk.fx_rpc.rpc import *
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy import and_
from fx_py_sdk.grpc_client import GRPCClient
import traceback
import time
from fx_py_sdk.notify_service import send_mail
from fx_py_sdk.scan_block import ScanBlock, ScanBlockBase

reconnect_block_count = 0
reconnect_tx_count = 0
tm_event_NewBlock = "tm.event='NewBlock'"
tm_event_Tx = "tm.event='Tx'"

history_file_prefix = 'fxdex_blocks'

class ScanManager:
    def __init__(self, rpc_page_size=5, rpc_max_retries=3):
        self.pair_id = os.environ.get('PAIR_ID')
        self.scan = ScanBlock(self.pair_id)

        self.ws_scan = WebsocketScan(self)
        self.rpc_scan = RpcScan(self,
                                page_size=rpc_page_size,
                                rpc_max_retries=rpc_max_retries)
                                
        self.account_scan = AccountScan(self, update_interval_seconds=60)
        self.error_scan = ErrorScan(self,
                                    update_interval_seconds=1,
                                    rpc_max_retries=rpc_max_retries)    # rpc only, ws has no code

class RpcScan:
    """use rpc connect fxdex, scan block event"""

    def __init__(self, scan_manager: ScanManager, page_size=10, rpc_max_retries=3):
        self.manager = scan_manager
        self.pair_id = scan_manager.pair_id

        self.scan = ScanBlock(self.pair_id)
        self.page_size = page_size

        self.rpc_url = constants.Network.get_rpc_url()
        self.rpc_client = HttpRpcClient(self.rpc_url, max_retries=rpc_max_retries)

        self.process_block_threaded()

    def process_block_threaded(self):
        threading.Thread(target=self.process_block).start()

    def process_block(self):
        start_block = None

        while True:
            """parse block data"""

            abci_info = self.rpc_client.get_abci_info()
            latest_block_height = int(
                abci_info["response"]["last_block_height"])

            """get last sync block height from sql"""
            if not start_block:
                start_block = int(os.environ.get('START_BLOCK', '1'))

            block_heights = [blk_ht for blk_ht, in (self.scan.crud.session.query(Block)
                                                                          .filter(Block.height >= start_block, Block.pair_id == self.pair_id)
                                                                          .with_entities(Block.height)
                                                                          .order_by(Block.height))]
            missing_blocks = list(sorted(
                set(range(start_block, latest_block_height+1)).difference(set(block_heights))
            ))

            # Switching from RPC to WebSockets logic
            use_ws = False
            if not missing_blocks:  # use WebSockets if fully synced
                if use_ws:
                    logging.info(
                        'Synced with latest block. Switching to WebSockets...')
                    self.manager.ws_scan.rpc_ready = True
                    return
                else:
                    # 17/06/22: Occasionally sockets don't push TxEvent, or report "events not in tx_result"
                    #           Code block below lets it remain on RPC polling
                    time.sleep(60)
                    continue
            
            first_block_height = missing_blocks[0]  # min
            last_block_height = missing_blocks[-1]  # max
            logging.info("Rpc scan from %d to %d (%d blocks)",
                         first_block_height, last_block_height, len(missing_blocks))

            def get_block_results(block_height, results_arr):
                while True:
                    try:
                        block_result = self.rpc_client.get_block_results(block_height)
                        block_rpc = self.rpc_client.get_block(block_height)
                        results_arr.append((block_result, block_rpc))
                        return
                    except Exception as ex:
                        logging.error(f'Error retrieving block: {ex}')
                        time.sleep(10)

            for i in range(0, len(missing_blocks), self.page_size):
                if i > 0 and i % 10000 <= self.page_size:
                    logging.info(str(i))

                thread_list = []
                results = []

                next_chunk = missing_blocks[i:i+self.page_size]
                for block_height in next_chunk:
                    thread_list.append(threading.Thread(target=get_block_results, args=(block_height, results)))

                for t in thread_list:
                    t.start()
                for t in thread_list:
                    t.join()

                # process sequentially
                for block_result, block_rpc in sorted(results, key=lambda x: x[0]['height']):
                    block_height = int(block_result['height'])
                    block_time = block_rpc[BlockResponse.BLOCK][BlockResponse.HEADER][BlockResponse.Time]
                    timestamp = Timestamp()
                    timestamp.FromJsonString(block_time),
                    block_datetime = datetime.datetime.utcfromtimestamp(timestamp.ToSeconds())

                    # If txs_results is not None, process each tx_event
                    if block_result[BlockResponse.Txs_results] is not None:
                        for index, tx_result in enumerate(block_result[BlockResponse.Txs_results]):
                            txMsg = block_rpc[BlockResponse.BLOCK][BlockResponse.DATA][BlockResponse.Txs][index]
                            txHashByte = base64.b64decode(txMsg)
                            tx_hash = hashlib.sha256(txHashByte).hexdigest().upper()
                            tx_events = tx_result[BlockResponse.EVENTS]
                            self.scan.process_tx_events(tx_events, block_height, tx_hash)
                    # Else update block height in any case
                    else:
                        block = Block(height=block_height, time=block_datetime, tx_events_processed=True, pair_id=self.pair_id)
                        self.scan.process_block_height(block)

                    if block_result[BlockResponse.Begin_block_events] is not None:
                        self.scan.process_begin_block(
                            block_result[BlockResponse.Begin_block_events], block_height)

                    self.scan.realized_positions[block_height] = deque()
                    if block_result[BlockResponse.End_block_events] is not None:
                        self.scan.process_end_block(
                            block_result[BlockResponse.End_block_events], block_height)

                    self.scan.process_best_bid_ask(block_height, True)
                    self.scan.process_cumulative_realized_pnl(block_height)

                    # Update latest block on chain
                    block = Block(height=block_height, time=block_datetime, block_processed=True, pair_id=self.pair_id)
                    self.scan.process_block_height(block)

            # Read the block directly after all missing blocks previously acquired
            start_block = last_block_height + 1

class WebsocketScan:
    """use websocket connect fxdex, scan block event"""

    def __init__(self, 
                 scan_manager: ScanManager=None,
                 subscribe_events: List[str]=None,
                 scan: ScanBlockBase = None,
                 ws_url = None):
        self.manager = scan_manager
        self.scan: ScanBlockBase = scan or ScanBlock(scan_manager.pair_id)

        self.wss_url = ws_url or constants.Network.get_ws_url()
        logging.info(self.wss_url)

        self.ws_block = None
        self.rpc_ready = False
        self._subscribed_endpoints = None

        self.subscribe_events = subscribe_events or [tm_event_NewBlock, tm_event_Tx]
        threading.Thread(target=self.subscribe_block).start()

    def _get_ws_endpoint_url(self):
        return f"{self.wss_url}websocket"

    def _handle_exception(self, error, send_email=True):
        was_ready = self.rpc_ready
        self.rpc_ready = False

        title = f'WS error: {str(error)} (Blk Ht: {self.scan.max_block_height}) [{self.scan.pair_id}]'
        exception_traceback = traceback.format_exc()
        logging.warning(title)
        logging.warning(exception_traceback)
        if was_ready:
            send_mail(title, exception_traceback, recipients='matthew.ang@pundix.com')

        global reconnect_block_count
        print("websocket caught: ", error)
        if (isinstance(error, ConnectionRefusedError) or
            isinstance(error, ConnectionResetError) or
            isinstance(error, websocket._exceptions.WebSocketConnectionClosedException)):

            time.sleep(1.0 * 2**reconnect_block_count)   # wait a while so we don't spam the server
            logging.info("正在尝试第 %d 次重连" % reconnect_block_count)
            reconnect_block_count += 1

            """
            if we were processing WS data before, then we need to resume RPC
            else, RPC is probably already running - we don't need to do anything extra
            """
            if was_ready and self.manager and isinstance(self.scan, ScanBlock):
                # reinstate connection (in case of idle-in-transaction timeout)
                self.manager.rpc_scan.scan.crud.init_session()
                # delete all data from the most recent block height with incomplete data
                self.manager.rpc_scan.scan.crud.delete_data_from_lowest_incomplete_height(
                    pair_id = self.scan.pair_id,
                    default_block_height = self.scan.max_block_height
                )
                # process RPC data sequentially
                self.manager.rpc_scan.process_block_threaded()

            """reinstate websocket connection"""
            self.subscribe_block()
        else:
            print("error: ", error)

    def on_error(self, error):
        self._handle_exception(error)

    def on_message(self, message):
        global reconnect_block_count
        reconnect_block_count = 0
        msg = json.loads(message)

        try:
            connect_id = msg["id"]
            if connect_id not in self._subscribed_endpoints:
                self._subscribed_endpoints.add(connect_id)
                logging.info(f"Successfully subscribed to {self.subscribe_events[connect_id]}")

            current_time = time.time()
            if not len(self._subscribed_endpoints) == len(self.subscribe_events) and (current_time - self._subscribe_time) > 2.5:
                logging.warning("Have not successfully subscribed to all endpoints, resending...")
                self._subscribe_time = current_time
                self._send_subscribe()

            if self.manager and not self.rpc_ready:
                return

            reconnect_block_count = 0

            if BlockResponse.RESULT in msg and str(msg[BlockResponse.RESULT]) != '{}':
                if msg[BlockResponse.RESULT][BlockResponse.QUERY] == tm_event_Tx:
                    if BlockResponse.RESULT not in msg:
                        logging.info(f"result not in message yet {msg}")
                        return
                    if BlockResponse.DATA not in msg[BlockResponse.RESULT]:
                        logging.info(f"data not in message yet {msg}")
                        return
                    if BlockResponse.VALUE not in msg[BlockResponse.RESULT][BlockResponse.DATA]:
                        logging.info(f"value not in message yet {msg}")
                        return
                    if BlockResponse.TxResult not in msg[BlockResponse.RESULT][BlockResponse.DATA][
                        BlockResponse.VALUE]:
                        logging.info(f"tx_result not in message yet {msg}")
                        return
                    
                    tx_result = msg[BlockResponse.RESULT][BlockResponse.DATA][BlockResponse.VALUE][
                        BlockResponse.TxResult]
                    if BlockResponse.EVENTS not in tx_result[BlockResponse.RESULT]:
                        logging.info(f"events not in tx_result yet {msg}")

                    block_height = int(tx_result[BlockResponse.HEIGHT])
                    if tx_result is not None and BlockResponse.EVENTS in tx_result[BlockResponse.RESULT]:
                        tx_events = tx_result[BlockResponse.RESULT][BlockResponse.EVENTS]
                    else:
                        tx_events = []
                    tx_hash = msg["result"]["events"]["tx.hash"][0]
                    self.scan.process_tx_events(tx_events, block_height, tx_hash)
                elif msg[BlockResponse.RESULT][BlockResponse.QUERY] == tm_event_NewBlock:
                    self.scan.process_block(msg)
        except Exception as ex:
            self._handle_exception(ex)

    def on_open(self):
        logging.info("connection to fxdex...")
        self._send_subscribe()

    def _send_subscribe(self, wait_interval: float = .25):
        for id, event in enumerate(self.subscribe_events):
            data = {
                "jsonrpc": "2.0",
                "method": "subscribe",
                "params": [event],
                "id": id
            }
            data = json.dumps(data).encode()
            self.ws_block.send(data)
            logging.info(f"Subscribed to {event} (id: {id})")
            time.sleep(wait_interval)

    def on_close(self):
        logging.info("connection to fxdex websocket is closed")

    def subscribe_block(self):
        self._subscribe_time = time.time()
        self._subscribed_endpoints = set()

        websocket.enableTrace(False)    # prevent debug messages
        logging.info(self._get_ws_endpoint_url())
        self.ws_block = websocket.WebSocketApp(self._get_ws_endpoint_url(),
                                               on_message=self.on_message,
                                               on_error=self.on_error,
                                               on_close=self.on_close,
                                               on_open=self.on_open)

        try:
            self.ws_block.run_forever()
        except KeyboardInterrupt:
            self.ws_block.close()
        except:
            self.ws_block.close()

class AccountScan:
    def __init__(self, scan_manager: ScanManager, update_interval_seconds=60):
        self.manager = scan_manager
        self.pair_id = scan_manager.pair_id

        self.owners = None
        self.last_updated = None

        self.client = scan_manager.scan.client or GRPCClient(constants.Network.get_grpc_url())
        self.update_interval = update_interval_seconds

        threading.Thread(target=self.update_account_balances_looped).start()

    def update_account_balances(self):
        logging.info('Updating account balances...')
        now = datetime.datetime.utcnow()

        if not self.owners or (now - self.last_updated) > datetime.timedelta(seconds=self.update_interval*9.5):
            query_owners = 'SELECT DISTINCT owner FROM trade'
            if self.pair_id:
                query_owners += ' WHERE pair_id=:pair_id'

            query_result = self.manager.scan.crud.session.execute(
                statement = query_owners,
                params = { 'pair_id': self.pair_id }
            ).fetchall()

            self.owners = [res[0] for res in query_result]
            self.last_updated = now

        if not self.owners:
            return

        all_balances = []
        batch_time = datetime.datetime.utcnow()

        def append_balances(owner: str):
            try:
                time_updated = datetime.datetime.utcnow()
                balances = self.client.query_all_balances(owner)
                
                for symbol, balance_amount in balances.items():
                    bal = Balance(
                        owner=owner,
                        token=symbol,
                        amount=balance_amount,
                        batch_time=batch_time,
                        time=time_updated,
                        pair_id=self.pair_id
                    )
                    all_balances.append(bal)
            except Exception as ex:
                logging.info(f"Error encountered when getting balance for {owner}. Retrying... {ex}")
            finally:
                pass

        threads = [threading.Thread(target=append_balances, args=(owner,))
                   for owner in self.owners]
        for t in threads:
            t.start()
        for t in threads:
            t.join(15.0)
        
        self.client.crud.insert_many(all_balances)

    def update_account_balances_looped(self, retry_times=3):
        while True:
            for _ in range(retry_times):
                try:
                    self.update_account_balances()
                    break
                except Exception as ex:
                    logging.error(f'Error updating balances: {ex}')
                    self.client = GRPCClient(constants.Network.get_grpc_url())  # refresh client
                    time.sleep(5)

            time.sleep(self.update_interval)

class PricingScan:
    def __init__(self,
                 base_url: str = None,
                 update_interval_seconds=1):
        self._update_interval_seconds = update_interval_seconds
        self.crud = Crud()
        self._pricing_dict: Dict[str, Pricing] = None
        self._funding_dict: Dict[str, FundingRate] = None

        base_url = base_url or constants.BASE_URL
        self._orderbook_url = base_url + constants.ORDERBOOK_ENDPOINT
        self._pricing_url = base_url + constants.PRICING_ENDPOINT
        self._funding_url = base_url + constants.FUNDING_ENDPOINT

    def _orderbook_callback(self, data: Dict):
        pair_id: str = data["pair"]
        block_height = int(data["blockHeight"])
        bids = data["bidOrderBookList"]
        asks = data["askOrderBookList"]

        pricing = self._pricing_dict[pair_id]
        pricing.pair_id = pair_id
        pricing.block_height = block_height
        if bids:
            pricing.best_bid = Decimal(bids[0]["price"])
        if asks:
            pricing.best_ask = Decimal(asks[0]["price"])

        funding_rate = self._funding_dict[pair_id]
        funding_rate.pair_id = pair_id
        funding_rate.block_height = block_height

    def _pricing_callback(self, data: Dict):
        for pair_data in data:
            pair_id: str = pair_data["pair"]

            pricing = self._pricing_dict[pair_id]
            pricing.oracle_price = Decimal(pair_data["oraclePrice"])
            pricing.mark_price = Decimal(pair_data["markPrice"])

    def _funding_callback(self, data: Dict):
        pair_id: str = data["pair"]
        funding_rate: FundingRate = self._funding_dict[pair_id]
        funding_rate.rate = Decimal(data["latestFundingRate"])

    def response_with_callback(
        self,
        rest_url: str,
        json_payload: Dict,
        response_callback: Callable,
    ):

        try:
            response = requests.post(
                url=rest_url,
                json=json_payload,
            )

            if response.ok:
                data = response.json()["data"]
                response_callback(data)
            else:
                logging.error(f"Error response from {rest_url}: {response.json()}")
        except Exception as ex:
            logging.error(f"Error updating from {rest_url}: {ex}")
        finally:
            time.sleep(1)


    def update_pricings(self):
        self._pricing_dict = defaultdict(lambda: Pricing())
        self._funding_dict = defaultdict(lambda: FundingRate())
        thread_list: List[threading.Thread] = []

        """Orderbook queries"""
        for pair_id in constants.PAIR_IDS:
            thread_list.append(threading.Thread(
                target=self.response_with_callback,
                args=(self._orderbook_url, { "pair": pair_id }, self._orderbook_callback),
            ))

        """Oracle + mark price queries"""
        thread_list.append(threading.Thread(
            target=self.response_with_callback,
            args=(self._pricing_url, {}, self._pricing_callback),
        ))

        """Funding rate queries"""
        for pair_id in constants.PAIR_IDS:
            thread_list.append(threading.Thread(
                target=self.response_with_callback,
                args=(self._funding_url, { "pair": pair_id }, self._funding_callback),
            ))

        """Make requests asynchronously"""
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()

        """Save records to database"""
        # Pricing (bid, ask, oracle, mark)
        for pricing in self._pricing_dict.values():
            sql_pricing = self.crud.filterone(
                Pricing,
                Pricing.pair_id == pricing.pair_id, Pricing.block_height == pricing.block_height            
            )

            if not sql_pricing:
                self.crud.insert(pricing)

        # Funding rate
        for funding in self._funding_dict.values():
            sql_funding = self.crud.filterone(
                FundingRate,
                FundingRate.pair_id == funding.pair_id, FundingRate.block_height == funding.block_height
            )
            if not sql_funding:
                self.crud.insert(funding)

    def update_pricings_looped(self):
        while True:
            try:
                self.update_pricings()
            except Exception as ex:
                logging.error(f"Error updating pricings {ex}")
            finally:
                time.sleep(self._update_interval_seconds)

class ErrorScan:
    def __init__(self, scan_manager: ScanManager, update_interval_seconds=1, rpc_max_retries=3):
        self.manager = scan_manager
        self.pair_id = scan_manager.pair_id
        self.owners = None
        self.last_updated = None

        self.scan = ScanBlock()
        self.crud = self.scan.client.crud
        self.update_interval = update_interval_seconds

        self.rpc_url = constants.Network.get_rpc_url()
        self.rpc_max_retries = rpc_max_retries

        threading.Thread(target=self.update_error_logs_looped).start()

    def update_error_logs(self):
        max_block_height = self.crud.session.query(func.max(Block.height)).scalar()
        if not max_block_height:
            return  # wait until we at least have a single block
        max_error_height = self.crud.filterone(ErrorLog, ErrorLog.pair_id == self.pair_id).height

        for block_height in range(max_error_height+1, max_block_height+1):
            self.rpc_client = HttpRpcClient(self.rpc_url, max_retries=self.rpc_max_retries)
            block_result = self.rpc_client.get_block_results(block_height)

            if block_result[BlockResponse.Txs_results] is not None:
                for tx_result in block_result[BlockResponse.Txs_results]:
                    self.scan.process_tx_errors(tx_result, block_height)

            # Update current error log height
            sql_log = self.crud.filterone(ErrorLog, ErrorLog.pair_id == self.pair_id)
            error_log = ErrorLog(height=block_height, pair_id=self.pair_id)

            if sql_log:
                self.crud.update(ErrorLog,
                    filter=(ErrorLog.height==sql_log.height, ErrorLog.pair_id==self.pair_id),
                    updic=error_log.to_dict()
                )
            else:
                self.crud.insert(error_log)

    def update_error_logs_looped(self):
        while True:
            self.update_error_logs()


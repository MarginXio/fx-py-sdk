import base64
from collections import defaultdict, deque
import datetime as dt
from sqlite3 import IntegrityError
from typing import Tuple
from fx_py_sdk.model.block import *
from fx_py_sdk.model.crud import *
from fx_py_sdk.fx_rpc.rpc import *
from decimal import Decimal
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy import and_
from fx_py_sdk.grpc_client import GRPCClient
import traceback
import re

from fx_py_sdk.notify_service import send_mail

class ScanBlockBase:
    """process block event, then update to sql"""
    max_block_height: int = None

    def __init__(self, pair_id: Optional[str] = None):
        # maps block height to deque
        self.realized_positions: Dict[int, deque] = defaultdict(lambda: deque())

        # maintain reference to pair_id
        self.pair_id: str = pair_id

    """
     ************************ process Block ************************
     """

    def process_block(self, message: str):
        try:
            if BlockResponse.DATA not in message[BlockResponse.RESULT]:
                logging.info(f"data not in message: {message}")
                return
            block_height = message[BlockResponse.RESULT][BlockResponse.DATA][BlockResponse.VALUE][
                BlockResponse.BLOCK][BlockResponse.HEADER][BlockResponse.HEIGHT]
            block_height = int(block_height)
            block_time = message[BlockResponse.RESULT][BlockResponse.DATA][BlockResponse.VALUE][
                BlockResponse.BLOCK][BlockResponse.HEADER][BlockResponse.Time]

            timestamp = Timestamp()
            timestamp.FromJsonString(block_time),
            block_datetime = dt.datetime.utcfromtimestamp(
                timestamp.ToSeconds())

            begin_block_events = message[BlockResponse.RESULT][BlockResponse.DATA][BlockResponse.VALUE][
                BlockResponse.RESULT_BEGIN_BLOCK][BlockResponse.EVENTS]
            self.process_begin_block(begin_block_events, block_height)

            end_block_events = message[BlockResponse.RESULT][BlockResponse.DATA][BlockResponse.VALUE][
                BlockResponse.RESULT_END_BLOCK][BlockResponse.EVENTS]

            self.process_end_block(end_block_events, block_height)
            self.process_best_bid_ask(block_height, True)
            self.process_cumulative_realized_pnl(block_height)

            # Update latest block on chain
            block = Block(height=block_height, time=block_datetime, block_processed=True, pair_id=self.pair_id)
            self.process_block_height(block)

        except Exception as e:
            #logging.error(f"error process block: {e}")
            logging.error(f"error process block: {traceback.format_exc()}")

    # Placeholder methods (to be implemented in actual implementation)
    def process_block_height(self, block: Block):
        pass
    
    def process_tx_events(self, tx_events, block_height, tx_hash):
        pass

    def process_begin_block(self, begin_block_events, block_height):
        return

    def process_end_block(self, end_block_events, block_height):
        pass

    def process_best_bid_ask(self, block_height, process_positioning=False):
        pass

    def process_cumulative_realized_pnl(self, block_height):
        pass

    def integrity_check(self, block_height):
        pass

    position_id_keys = set([EventKeys.id, EventKeys.position_id])
    def get_position(self, attributes: [], is_new_position=False) -> Position:
        """decode position data"""
        position = Position()
        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')

            if key in self.position_id_keys:
                position.position_id = int(value)
            elif key == EventKeys.owner:
                position.owner = value
            elif key == EventKeys.pair_id:
                position.pair_id = value
            elif key == EventKeys.direction:
                position.direction = value
            elif key == EventKeys.entry_price:
                position.entry_price = Decimal(value)
            elif key == EventKeys.mark_price:
                position.mark_price = Decimal(value)
            elif key == EventKeys.liquidation_price:
                position.liquidation_price = Decimal(value)
            elif key == EventKeys.base_quantity:
                position.base_quantity = Decimal(value)
            elif key == EventKeys.margin:
                position.margin = Decimal(value)
            elif key == EventKeys.leverage:
                position.leverage = int(value)
            elif key == EventKeys.unrealized_pnl:
                position.unrealized_pnl = Decimal(value)
            elif key == EventKeys.realized_pnl:
                position.realized_pnl = Decimal(value)
            elif key == EventKeys.margin_rate:
                position.margin_rate = Decimal(value)
            elif key == EventKeys.initial_margin:
                position.initial_margin = Decimal(value)
            elif key == EventKeys.pending_order_quantity:
                position.pending_order_quantity = Decimal(value)
        return position

    def _get_fee(self, value: str) -> Tuple[Decimal, str]:
        """Given a fee string (e.g. '2000USDT'), returns a tuple of (fee_amount, fee_denom) (e.g. Decimal('2000'), 'USDT')"""
        amount = re.search(r'^[0-9]*', value).group()
        fee_amount = Decimal(amount) if amount else Decimal("0")
        fee_denom = re.search(r'[A-Za-z]+', value).group()
        return fee_amount, fee_denom

    def get_order(self, attributes: []) -> Order:
        """decode order data"""
        order = Order()
        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(
                attribute[BlockResponse.VALUE]).decode('utf8')
            if key == EventKeys.order_id:
                order.order_id = value
            elif key == EventKeys.owner:
                order.owner = value
            elif key == EventKeys.pair_id:
                order.pair_id = value
            elif key == EventKeys.direction:
                order.direction = value
            elif key == EventKeys.price:  # to decimal
                order.price = Decimal(value)
            elif key == EventKeys.base_quantity:
                order.base_quantity = Decimal(value)
            elif key == EventKeys.quote_quantity:
                order.quote_quantity = Decimal(value)
            elif key == EventKeys.filled_quantity:
                order.filled_quantity = Decimal(value)
            elif key == EventKeys.filled_avg_price:
                order.filled_avg_price = Decimal(value)
            elif key == EventKeys.created_at:
                if value.__contains__('T') and value.__contains__('Z'):
                    timestamp = Timestamp()
                    timestamp.FromJsonString(value),
                    block_datetime = dt.datetime.utcfromtimestamp(
                        timestamp.ToSeconds())
                    order.created_at = block_datetime
                else:
                    UTC_FORMAT = "%Y-%m-%d %H:%M:%S.%f +0000 UTC"
                    # microseconds truncated to 6 decimals
                    date_value = re.sub(
                        '(\d{7,9})', lambda x: x.group()[:6], value)
                    block_datetime = dt.datetime.strptime(
                        date_value, UTC_FORMAT)
                    order.created_at = block_datetime
            elif key == EventKeys.leverage:
                order.leverage = int(value)
            elif key == EventKeys.status:
                order.status = value
            elif key == EventKeys.order_type:
                order.order_type = value
            elif key == EventKeys.cost_fee:
                order.cost_fee, order.fee_denom = self._get_fee(value)
            elif key == EventKeys.locked_fee:
                order.locked_fee, order.fee_denom = self._get_fee(value)
            elif key == EventKeys.cancel_time:  # only cancel order or expire order have cancel_time
                timestamp = Timestamp()
                timestamp.FromJsonString(value),
                block_datetime = dt.datetime.utcfromtimestamp(
                    timestamp.ToSeconds())
                order.cancel_time = block_datetime
            elif key == EventKeys.position_id:
                order.position_id = int(value)
            elif key == EventKeys.deal_fee:
                order.deal_fee, order.fee_denom = self._get_fee(value)
            elif key == EventKeys.maker:
                order.maker = value == "true"

        return order

    def get_trade(self, attributes: []) -> Trade:
        """decode trade data"""

        trade = Trade()
        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(
                attribute[BlockResponse.VALUE]).decode('utf8')
            if key == EventKeys.deal_price:
                trade.deal_price = Decimal(value)
            elif key == EventKeys.matched_quantity:
                trade.matched_quantity = Decimal(value)
            elif key == EventKeys.order_id:
                trade.order_id = value
            elif key == EventKeys.owner:
                trade.owner = value
            elif key == EventKeys.pair_id:
                trade.pair_id = value
            elif key == EventKeys.direction:
                trade.direction = value
            elif key == EventKeys.price:  # to decimal
                trade.price = Decimal(value)
            elif key == EventKeys.base_quantity:
                trade.base_quantity = Decimal(value)
            elif key == EventKeys.quote_quantity:
                trade.quote_quantity = Decimal(value)
            elif key == EventKeys.filled_quantity:
                trade.filled_quantity = Decimal(value)
            elif key == EventKeys.filled_avg_price:
                trade.filled_avg_price = Decimal(value)
            elif key == EventKeys.order_type:
                trade.order_type = value
            elif key == EventKeys.cost_fee:
                trade.cost_fee, trade.fee_denom = self._get_fee(value)
            elif key == EventKeys.locked_fee:
                trade.locked_fee, trade.fee_denom = self._get_fee(value)
            elif key == EventKeys.position_id:
                trade.position_id = int(value)
            elif key == EventKeys.deal_fee:
                trade.deal_fee, trade.fee_denom = self._get_fee(value)
            elif key == EventKeys.maker:
                trade.maker = value == "true"

        return trade

    def get_funding_rate(self, attributes: []) -> FundingRate:
        """decode funding rate data"""
        funding_rate = FundingRate()
        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')

            if key == EventKeys.pair_id:
                funding_rate.pair_id = value
            elif key == EventKeys.funding_rate:
                funding_rate.rate = Decimal(value)
            elif key == EventKeys.funding_times:
                funding_rate.funding_times = int(value)
        return funding_rate

    def get_transfer(self, attributes: []) -> FundingRate:
        """decode transfer data"""
        transfer = Transfer()
        for attribute in attributes:
            try:
                key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
                value = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')

                if key == EventKeys.recipient:
                    transfer.recipient = value
                elif key == EventKeys.sender:
                    if value=='dex17xpfvakm2amg962yls6f84z3kell8c5l5s9l0c':
                        return None
                    transfer.sender = value                    
                elif key == EventKeys.amount:
                    amount, token = re.findall(r'(\d+)([^\d.]+)', value)[0]
                    transfer.amount = Decimal(amount) / Decimal('1E+18')
                    transfer.token = token
            except:
                if key=='amount':
                    if attribute[BlockResponse.VALUE]:
                        logging.error(f'Error parsing transfer: amount value = {attribute[BlockResponse.VALUE]}')
                    return None

        return transfer

    __class_field_mappings = dict()
    def decode_attributes(self, attributes, crud_cls):
        if crud_cls in self.__class_field_mappings:
            mappings = self.__class_field_mappings[crud_cls]
        else:
            mappings = { col.name: col.type.python_type
                         for col in crud_cls.__table__.columns
                         if col != 'id' }
            self.__class_field_mappings[crud_cls] = mappings

        crud_obj = crud_cls()
        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')

            if key in mappings:
                attr_type = mappings[key]
                setattr(crud_obj, key, attr_type(value))

        return crud_obj

    def get_margin(self, attributes: []):
        return self.decode_attributes(attributes, Margin)

    def get_oracle_price(self, attributes: []):
        oracle_price = OraclePrice()

        for attribute in attributes:
            key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
            value = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')

            if key == EventKeys.market_id:
                oracle_price.market_id = value
            elif key == EventKeys.oracle_price:
                oracle_price.price = value

        return oracle_price


# Implements business logic for handling block events
class ScanBlock(ScanBlockBase):
    """process block event, then update to sql"""

    def __init__(self, pair_id: Optional[str] = None):
        super().__init__(pair_id)
        self.client = GRPCClient(constants.Network.get_grpc_url())
        self.crud = self.client.crud

    def process_block_height(self, block: Block):
        """
        Updates block height fields in database, and sets `self.max_block_height`.
        """
        block_filters = [Block.height == block.height, Block.pair_id == self.pair_id]
        sql_block = self.crud.filterone(Block, *block_filters)

        if sql_block is None:
            self.crud.insert(block)
        else:
            update_dict = block.to_dict()
            self.crud.update(Block,
                filter=block_filters,
                updic=update_dict
            )

        try:    self.max_block_height = max(self.max_block_height or -1, block.height)
        except: pass

    def __update_position(self, position: Position, sql_position: Position):
        # we want to keep only latest position in database
        if position.block_height >= sql_position.block_height:
            update_dict = position.to_dict()
        elif sql_position.open_height is None or position.block_height < sql_position.open_height:
            update_dict = {'open_height': position.block_height}
        else:
            update_dict = None

        if update_dict:
            self.crud.update(Position,
                filter=(Position.position_id == position.position_id, Position.pair_id == position.pair_id),
                updic=update_dict
            )

    def __insert_order(self, order: Order):
        if order.status=='ORDER_FILLED':
            order.base_quantity = order.quote_quantity = Decimal('0')
        self.crud.insert(order)

    _order_statuses_to_ignore = set(['ORDER_FILLED', 'ORDER_CANCELLED', 'ORDER_PARTIAL_FILLED_CANCELLED', 'ORDER_PARTIAL_FILLED_EXPIRED', 'ORDER_EXPIRED'])
    def __update_order(self, order: Order, sql_order: Order):
        # we want to keep only latest order in database
        if sql_order.status in self._order_statuses_to_ignore and sql_order.maker is not None:
            return
        
        order.id = sql_order.id
        if order.block_height >= sql_order.block_height:
            if order.status=='ORDER_FILLED':
                order.base_quantity = order.quote_quantity = Decimal('0')
            update_dict = order.to_dict()
            if 'owner' in update_dict:
                del update_dict['owner']    # we don't want to overwrite owner
        else:
            update_dict = {}
            for attr in ['open_block_height']:
                attr_val = getattr(order, attr)
                if attr_val is not None and getattr(sql_order, attr) is None:
                    update_dict[attr] = attr_val

        if update_dict:
            self.crud.update(Order,
                filter=(Order.order_id == order.order_id, Order.pair_id == self.pair_id),
                updic=update_dict
            )

    def update_from_order_fill(self, event: Dict, block_height: int):
        order = self.get_order(event[BlockResponse.Attributes])
        trade = self.get_trade(event[BlockResponse.Attributes])

        order.block_height = block_height
        order.filled_block_height = block_height
        order.last_filled_quantity = trade.matched_quantity

        sql_order: Order = self.crud.filterone(
            Order,
            Order.order_id == order.order_id, Order.pair_id == self.pair_id
        )
        if order.status=='ORDER_PENDING':
            # fully filled on same block order was sent
            if order.open_block_height==block_height and order.base_quantity==order.filled_quantity:
                order.status = 'ORDER_FILLED'
            else:
                order.status = 'ORDER_PARTIAL_FILLED'

        trade.block_height = block_height
        if order.order_type=='ORDER_TYPE_LIQUIDATION':
            trade.liquidation_owner = trade.owner
            trade.owner = sql_order.owner if sql_order else order.owner

        # Insert order
        if sql_order is None:
            order.open_block_height = block_height  # could be incorrect
            order.initial_base_quantity = order.base_quantity
            self.__insert_order(order)
        else:
            self.__update_order(order, sql_order)

        # Then trade
        self.crud.insert(trade)

    def update_position(self, event: Dict, block_height: int):
        event_type: str = event[BlockResponse.TYPE]

        # Get Position object from attributes
        position = self.get_position(
            attributes = event[BlockResponse.Attributes],
            is_new_position = event_type == EventTypes.New_position,
        )
        position_status = PositionStatus.Open

        # Assign event-specific attributes (open_height, last_order_fill_height, close_height, status)
        if event_type == EventTypes.New_position:
            position.open_height = block_height
        elif event_type == EventTypes.Part_close_position:
            position.last_order_fill_height = block_height
        elif event_type == EventTypes.Full_close_position:
            position.last_order_fill_height = block_height
            position.close_height = block_height
            position_status = PositionStatus.Close
        elif event_type == EventTypes.Forced_liquidation_position:
            position.close_height = block_height
            position_status = PositionStatus.Liquidated

        position.block_height = block_height
        position.status = position_status

        # Update in database if exists, else create
        sql_position = self.crud.filterone(
            Position,
            Position.position_id == position.position_id, Position.pair_id == self.pair_id
        )

        if sql_position is None:
            self.crud.insert(position)
        else:
            self.__update_position(position, sql_position)

        # Mark positions to be considered for realized P&L logging
        if event_type in [EventTypes.Part_close_position, EventTypes.Full_close_position]:
            self.realized_positions[block_height].append(position)

        return position

    def process_end_block(self, events: str, block_height: int):
        """process fxdex chain EndBlock events"""
        for event in events:
            if event[BlockResponse.TYPE] in EventTypes.Position_events:
                self.update_position(event, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Cancel_order_expire:
                """update order status to expiration"""
                order = self.get_order(event[BlockResponse.Attributes])
                order.block_height = block_height
                order.cancel_block_height = block_height

                sql_order = self.crud.filterone(
                    Order,
                    Order.order_id == order.order_id, Order.pair_id == self.pair_id
                )
                if sql_order is None:
                    self.__insert_order(order)
                else:
                    self.__update_order(order, sql_order)

                self.process_orderbook(order, False, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Order_fill:
                """store order & trade"""
                self.update_from_order_fill(event, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Transfer:
                transfer = self.get_transfer(event[BlockResponse.Attributes])

                if transfer:
                    transfer.block_height = block_height
                    transfer.pair_id = self.pair_id
                    self.crud.insert(transfer)

        return

    def process_begin_block(self, events: str, block_height: int):
        """process fxdex chain BeginBlock events"""

        for i, event in enumerate(events):
            if event[BlockResponse.TYPE] == EventTypes.Forced_liquidation_position:
                position = self.get_position(event[BlockResponse.Attributes])
                position.status = PositionStatus.Liquidated
                position.block_height = block_height
                position.close_height = block_height

                sql_position = self.crud.filterone(
                    Position,
                    Position.position_id == position.position_id, Position.pair_id == self.pair_id
                )
                if sql_position is None:
                    self.crud.insert(position)
                else:
                    self.__update_position(position, sql_position)

            elif event[BlockResponse.TYPE] == EventTypes.Cancel_order_liq:
                """liquidation cancel pending close-position order, only update order"""
                order = self.get_order(event[BlockResponse.Attributes])
                order.block_height = block_height
                order.cancel_block_height = block_height

                sql_order = self.crud.filterone(
                    Order,
                    Order.order_id == order.order_id, Order.pair_id == self.pair_id
                )
                if sql_order is None:
                    self.__insert_order(order)
                else:
                    self.__update_order(order, sql_order)

                self.process_orderbook(order, False, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Liquidation_position_order:
                """liquidation generate new order, only insert order"""
                order = self.get_order(event[BlockResponse.Attributes])
                order.open_block_height = block_height
                order.block_height = block_height
                if order.base_quantity:     # remaining open quantity > 0
                    order.initial_base_quantity = order.base_quantity
                else:                       # filled on open
                    order.initial_base_quantity = order.filled_quantity
                    order.filled_block_height = block_height

                # owner of liquidation order is DEX wallet
                # overwrite with position owner
                liquidation_event = events[i+1]
                order.liquidation_owner = order.owner
                for attribute in liquidation_event[BlockResponse.Attributes]:
                    key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
                    if key=='owner':
                        order.owner = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')
                        break

                sql_order = self.crud.filterone(
                    Order,
                    Order.order_id == order.order_id, Order.pair_id == order.pair_id
                )
                if sql_order is None:
                    self.__insert_order(order)
                self.process_orderbook(order, True, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Settle_funding:
                """parse settle funding rate log"""
                funding_transfer = FundingTransfer()
                funding_transfer.block_height = block_height
                for attribute in event[BlockResponse.Attributes]:
                    key = base64.b64decode(
                        attribute[BlockResponse.Key]).decode('utf8')
                    value = base64.b64decode(
                        attribute[BlockResponse.VALUE]).decode('utf8')
                    if key == EventKeys.position_id:
                        funding_transfer.position_id = int(value)
                    elif key == EventKeys.owner:
                        funding_transfer.owner = value
                    elif key == EventKeys.pair_id:
                        funding_transfer.pair_id = value
                    elif key == EventKeys.funding_fee:
                        funding_transfer.funding_fee = Decimal(value)

                """in case of duplicate"""
                sql_transfer = self.crud.filterone(FundingTransfer, and_(FundingTransfer.pair_id == funding_transfer.pair_id,
                                                                         FundingTransfer.block_height == funding_transfer.block_height,
                                                                         FundingTransfer.owner == funding_transfer.owner,
                                                                         FundingTransfer.position_id == funding_transfer.position_id,
                                                                         ))
                if sql_transfer is None:
                    self.crud.insert(funding_transfer)
                    """if exist, do not need to update"""
            
            # elif event[BlockResponse.TYPE] == EventTypes.Log_funding_rate:
            #     funding_rate = self.get_funding_rate(event[BlockResponse.Attributes])
            #     funding_rate.block_height = block_height
            #
            #     """in case of duplicate"""
            #     sql_funding_rate = self.crud.filterone(FundingRate, and_(
            #         FundingRate.pair_id==funding_rate.pair_id, FundingRate.block_height==block_height
            #     ))
            #
            #     if not sql_funding_rate:
            #         self.crud.insert(funding_rate)

            elif event[BlockResponse.TYPE] == EventTypes.Transfer:
                transfer = self.get_transfer(event[BlockResponse.Attributes])

                if transfer:
                    transfer.block_height = block_height
                    transfer.pair_id = self.pair_id
                    self.crud.insert(transfer)

        return

    """
    ************************ process tx ************************
    """

    def process_tx_errors(self, tx_result, block_height):
        if tx_result[BlockResponse.Code] != 0:
            error = Error()
            error.log = tx_result[BlockResponse.Log]
            error.block_height = block_height
            error.pair_id = self.pair_id

            for event in tx_result[BlockResponse.EVENTS]:
                if event[BlockResponse.TYPE]==EventTypes.Message:
                    for attribute in event[BlockResponse.Attributes]:
                        key = base64.b64decode(attribute[BlockResponse.Key]).decode('utf8')
                        if key=='sender':
                            error.sender = base64.b64decode(attribute[BlockResponse.VALUE]).decode('utf8')
            
            self.crud.insert(error)

    def process_tx_events(self, tx_events, block_height, tx_hash):
        """process fxdex chain Transaction events"""
        if tx_events is not None:
            for event in tx_events:
                if event[BlockResponse.TYPE] == EventTypes.Order or event[
                        BlockResponse.TYPE] == EventTypes.Close_position_order:
                    """only insert order, if sql order is none, then do not update"""
                    order = self.get_order(event[BlockResponse.Attributes])
                    order.tx_hash = tx_hash
                    order.open_block_height = block_height
                    order.block_height = block_height
                    if order.base_quantity:     # remaining open quantity > 0
                        order.initial_base_quantity = order.base_quantity
                    else:                       # filled on open
                        order.initial_base_quantity = order.filled_quantity
                        order.filled_block_height = block_height

                    sql_order = self.crud.filterone(
                        Order,
                        Order.order_id == order.order_id, Order.pair_id == self.pair_id
                    )
                    if sql_order is None:
                        self.__insert_order(order)
                    else:
                        self.__update_order(order, sql_order)  # updates open_block_height, created_at

                    self.process_orderbook(order, True, block_height)

                elif event[BlockResponse.TYPE] == EventTypes.Cancel_order_user:
                    """only update order, but in case of not listened create order"""
                    order = self.get_order(event[BlockResponse.Attributes])
                    order.block_height = block_height
                    order.cancel_block_height = block_height

                    sql_order = self.crud.filterone(
                        Order,
                        Order.order_id == order.order_id, Order.pair_id == self.pair_id
                    )
                    if sql_order is None:
                        self.__insert_order(order)
                    else:
                        self.__update_order(order, sql_order)

                    self.process_orderbook(order, False, block_height)

                elif event[BlockResponse.TYPE] == EventTypes.Add_margin:
                    """user adds margin to existing position"""
                    margin = self.get_margin(event[BlockResponse.Attributes])
                    margin.block_height = block_height
                    self.crud.insert(margin)

                elif event[BlockResponse.TYPE] == EventTypes.Order_fill:
                    """
                    store orders & trade
                    """
                    self.update_from_order_fill(event, block_height)

                elif event[BlockResponse.TYPE] == EventTypes.Oracle_updated_price:
                    oracle_price = self.get_oracle_price(event[BlockResponse.Attributes])
                    oracle_price.block_height = block_height
                    try:
                        self.crud.insert(oracle_price)
                    except IntegrityError:  # duplicate
                        pass

                elif event[BlockResponse.TYPE] in EventTypes.Position_events:
                    self.update_position(event, block_height)

                elif event[BlockResponse.TYPE] == EventTypes.Transfer:
                    transfer = self.get_transfer(event[BlockResponse.Attributes])

                    if transfer:
                        transfer.block_height = block_height
                        transfer.pair_id = self.pair_id
                        self.crud.insert(transfer)

        block = Block(height=block_height, tx_events_processed=True, pair_id=self.pair_id)
        self.process_block_height(block)

    """
        add_or_cancel: True means add (append), False means cancel (subtract)
    """
    def process_orderbook(self, order: Order, add_or_cancel: bool, block_height):
        return

        """
        sql_orderbook = self.crud.get_latest_orderbook_record(
            order.price, order.pair_id, order.direction)

        orderbook = Orderbook(price=order.price, quantity=order.base_quantity,
                              direction=order.direction, pair_id=order.pair_id,
                              block_height=block_height)

        if sql_orderbook:
            if add_or_cancel:
                orderbook.quantity = order.base_quantity + sql_orderbook.quantity
            else:
                orderbook.quantity = sql_orderbook.quantity - order.base_quantity

        self.crud.insert(orderbook)
        """

    def process_best_bid_ask(self, block_height, process_positioning=False):
        best_bid_asks = {}
        orderbook_tops = []
        positionings = []
        locked_fees = []

        # t0 = time.time()

        # Query best bid-ask from orders table
        """
        query_result = self.crud.query_best_bid_ask(block_height)
        for pair_id, best_bid, best_ask, update_block_height in query_result:
            best_bid_ask = OrderbookTop(pair_id=pair_id,
                                        best_bid=best_bid, best_ask=best_ask,
                                        block_height=block_height)
            best_bid_asks[pair_id] = best_bid_ask

            if block_height==update_block_height:
                orderbook_tops.append(best_bid_ask)
        """

        """Process positionings (i.e. record historical realized & unrealized P&L)"""
        # Realized P&L
        realized_positions = self.realized_positions[block_height]
        if process_positioning:
            while realized_positions:
                position = realized_positions.pop()

                is_long = position.direction=='LONG'
                best_price = position.mark_price

                unrealized_pnl = position.base_quantity * (1 if is_long else -1) * (best_price - position.entry_price)

                # is_batch_update = False
                positioning = Positioning(owner=position.owner, pair_id=position.pair_id, 
                                          entry_price=position.entry_price, mark_price=position.mark_price,
                                          base_quantity=position.base_quantity, realized_pnl=position.realized_pnl,
                                          unrealized_pnl=unrealized_pnl, margin=position.margin,
                                          direction=position.direction, position_id=position.position_id,
                                          block_height=block_height, is_batch_update=False)
                if position.status!='open':
                    positioning.base_quantity = positioning.unrealized_pnl = 0

                positionings.append(positioning)

            # Unrealized P&L
            if block_height % int(os.environ.get('POSITIONING_UPDATE_INTERVAL', '250')) == 0:
                logging.info(f'Marking unrealied P&L to market... (blk ht = {block_height})')

                open_positions = self.crud.filter_many(
                    Position,
                    Position.status=='open', Position.pair_id==self.pair_id
                )
                mark_prices = { res[0]: res[1] for res in self.crud.query_mark_prices() }
                order_margin_by_owner = { res[0]: res[1] for res in self.crud.query_open_order_margin(self.pair_id) }

                for position in open_positions:
                    is_long = position.direction=='LONG'

                    best_price = mark_prices[position.pair_id]
                    unrealized_pnl = position.base_quantity * (1 if is_long else -1) * (best_price - position.entry_price)

                    # is_batch_update = True
                    order_margin = order_margin_by_owner.get(position.owner, Decimal("0"))
                    positioning = Positioning(owner=position.owner, pair_id=position.pair_id, 
                                              entry_price=position.entry_price, mark_price=best_price,
                                              base_quantity=position.base_quantity, realized_pnl=position.realized_pnl,
                                              unrealized_pnl=unrealized_pnl, margin=position.margin, order_margin=order_margin,
                                              direction=position.direction, position_id=position.position_id,
                                              block_height=block_height, is_batch_update=True)
                    
                    positionings.append(positioning)

                # Locked fees
                try:
                    all_locked_fees = self.crud.query_all_locked_fees()
                    for current_fees in all_locked_fees:
                        fee_record = LockedFee()
                        fee_record.pair_id, fee_record.owner, fee_record.direction, fee_record.fees = current_fees
                        fee_record.block_height = block_height

                        locked_fees.append(fee_record)
                except Exception as ex:
                    logging.error(f'Error processing locked fees: {ex}')

        if best_bid_asks:
            self.crud.insert_many(orderbook_tops)
        if positionings:
            self.crud.insert_many(positionings)
        if locked_fees:
            self.crud.insert_many(locked_fees)

    def process_cumulative_realized_pnl(self, block_height):
        interval = 500
        if block_height%interval==0:
            self.crud.update_realized_pnl_logs(
                start_block_height = block_height-interval+1,
                end_block_height = block_height,
                pair_id = self.pair_id
            )

    def integrity_check(self, block_height, order_diff_threshold=10):
        """
        Compare top n open order counts (grouped by `owner`, `pair_id`) between database and SDK.
        E-mail alerts will be sent for open order counts differing more than `order_diff_threshold`.
        """
        if block_height % 25 == 0:
            logging.info(f'Running integrity check... (blk ht = {block_height})')

            open_order_counts = self.crud.query_open_order_count_by_pairid_and_address(
                pair_id=self.pair_id,
                limit_records=10
            )
            alert_list = []

            for pair_id, owner, db_order_count in open_order_counts:
                try:
                    sdk_order_count = len(self.client.query_orders(owner=owner, pair_id=pair_id, page="1", limit="10000", use_db=False))
                except:
                    sdk_order_count = 0
                    
                if abs(db_order_count - sdk_order_count) > order_diff_threshold:
                    alert_msg = f'{owner} has {sdk_order_count} open orders on chain, but {db_order_count} in database'
                    alert_list.append(alert_msg)
                    logging.warn(alert_msg)

            if alert_list:
                alert_title = f'Integrity Check Alert (Blk Ht: {block_height}) [{self.pair_id}]'
                alert_text = os.linesep.join(alert_list)
                send_mail(alert_title, alert_text)
                

class TradingScanBlock(ScanBlockBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_new_order(self, order: Order, block_height: int):
        pass

    def on_new_position(self, position: Position, block_height: int):
        pass

    def on_position_change(self, position: Position, block_height: int):
        pass

    def on_position_close(self, position: Position, block_height: int):
        pass

    def on_order_fill(self, order: Order, trade: Trade, block_height: int):
        pass

    def on_order_cancel(self, order: Order, block_height: int):
        pass

    def on_oracle_price_change(self, oracle_price: OraclePrice, block_height: int):
        pass

    def process_tx_events(self, tx_events, block_height, tx_hash):
        if tx_events is not None:
            for event in tx_events:
                if event[BlockResponse.TYPE] == EventTypes.Order or event[
                        BlockResponse.TYPE] == EventTypes.Close_position_order:
                    """new order on chain (both open & closing position"""
                    order = self.get_order(event[BlockResponse.Attributes])
                    order.tx_hash = tx_hash
                    order.open_block_height = block_height
                    order.block_height = block_height
                    order.initial_base_quantity = order.base_quantity

                    self.on_new_order(order, block_height)
                elif event[BlockResponse.TYPE] == EventTypes.Cancel_order_user:
                    """order cancelled"""
                    order = self.get_order(event[BlockResponse.Attributes])
                    order.block_height = block_height
                    order.cancel_block_height = block_height

                    self.on_order_cancel(order, block_height)
                elif event[BlockResponse.TYPE] == EventTypes.Oracle_updated_price:
                    """change in oracle price"""
                    oracle_price = self.get_oracle_price(event[BlockResponse.Attributes])
                    oracle_price.block_height = block_height
                    self.on_oracle_price_change(oracle_price, block_height)

    def process_end_block(self, events: str, block_height: int):
        for event in events:
            event_type = event[BlockResponse.TYPE]

            if event[BlockResponse.TYPE] == EventTypes.New_position:
                """new position created"""
                position = self.get_position(event[BlockResponse.Attributes], is_new_position=True)
                position.status = PositionStatus.Open
                position.block_height = position.open_height = block_height

                self.on_new_position(position, block_height)

            elif event[BlockResponse.TYPE] in (EventTypes.Add_position, EventTypes.Part_close_position):
                """position change (qty increased or decreased)"""
                position = self.get_position(event[BlockResponse.Attributes])
                position.status = PositionStatus.Open
                position.block_height = block_height

                self.on_position_change(position, block_height)

            elif event[BlockResponse.TYPE] == EventTypes.Full_close_position:
                """position fully closed"""
                position = self.get_position(event[BlockResponse.Attributes])
                position.status = PositionStatus.Close
                position.block_height = block_height
                position.close_height = block_height
                position.last_order_fill_height = block_height

                self.on_position_close(position, block_height)

            elif event_type == EventTypes.Cancel_order_expire:
                """order cancelled (on expiration)"""
                order = self.get_order(event[BlockResponse.Attributes])
                order.block_height = block_height
                order.cancel_block_height = block_height

                self.on_order_cancel(order, block_height)

            elif event_type == EventTypes.Order_fill:
                """order fill (including partial fills)"""
                order = self.get_order(event[BlockResponse.Attributes])
                trade = self.get_trade(event[BlockResponse.Attributes])

                order.block_height = block_height
                order.filled_block_height = block_height
                order.last_filled_quantity = trade.matched_quantity

                if order.status=='ORDER_PENDING':
                    # fully filled on same block order was sent
                    if order.open_block_height==block_height and order.base_quantity==order.filled_quantity:
                        order.status = 'ORDER_FILLED'
                    else:
                        order.status = 'ORDER_PARTIAL_FILLED'

                self.on_order_fill(order, trade, block_height)

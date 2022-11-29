from decimal import Decimal

class BlockResponse:
    RESULT = "result"
    DATA = "data"
    QUERY = "query"
    VALUE = "value"
    BLOCK = "block"
    HEADER = "header"
    HEIGHT = "height"
    EVENTS = "events"
    RESULT_BEGIN_BLOCK = "result_begin_block"
    RESULT_END_BLOCK = "result_end_block"
    TYPE = "type"
    TxResult = "TxResult"
    Attributes = "attributes"
    Key = "key"
    Time = "time"
    Txs = "txs"

    Response = "response"
    Txs_results = "txs_results"
    Begin_block_events = "begin_block_events"
    End_block_events = "end_block_events"

    Code = "code"
    Log = "log"

class EventTypes:
    """EndBlock"""
    Add_position = "dex.add_position"
    Order_fill = "dex.order_fill"
    New_position = "fx.dex.Position"
    Part_close_position = "dex.part_close_position"
    Full_close_position = "dex.full_close_position"
    Cancel_order_expire = "dex.expire_cancel" #order because of expire
    Cancel_order_partial_order = "dex.cancel_order" # will not happen from 2021/12/21

    """BeginBlock"""
    Forced_liquidation_position = "dex.forced_liquidation_position"
    # Liq_cancel_order = "dex.liq_cancel_order"
    Liquidation_position_order = "dex.liquidation_position_order"
    Log_funding_rate = "dex.log_funding_rate"
    Settle_funding = "dex.settle_funding"
    Transfer = "transfer"

    """Tx event"""
    Order = "fx.dex.Order"
    Cancel_order_user = "dex.user_cancel" #order because of user cancel
    Cancel_order_liq = "dex.liq_cancel" #cancel order because of liquidation
    Close_position_order = "dex.close_position_order"
    Message = "message"
    Add_margin = 'dex.add_margin'
    Oracle_updated_price = 'oracle_updated_price'

    """Collections"""
    Position_events = { Add_position, New_position, Part_close_position, Full_close_position, Forced_liquidation_position }

class EventKeys:
    """orders"""
    order_id = "order_id"
    owner = "owner"
    pair_id = "pair_id"
    direction = "direction"
    price = "price"
    base_quantity = "base_quantity"
    quote_quantity = "quote_quantity"
    filled_quantity = "filled_quantity"
    filled_avg_price = "filled_avg_price"
    created_at = "created_at"
    leverage = "leverage"
    status = "status"
    order_type = "order_type"
    cost_fee = "cost_fee"
    locked_fee = "locked_fee"
    deal_fee = "deal_fee"
    cancel_time = "cancel_time"
    maker = "maker"

    """positions"""
    id = "id"
    position_id = "position_id"
    margin = "margin"
    mark_price = "mark_price"
    entry_price = "entry_price"
    liquidation_price = "liquidation_price"
    margin_rate = "margin_rate"
    deal_price = "deal_price"
    unrealized_pnl = "unrealized_pnl"
    realized_pnl = "realized_pnl"
    initial_margin = "initial_margin"
    pending_order_quantity = "pending_order_quantity"
    position_id = "position_id"

    matched_quantity = "matched_quantity"
    unfilled_quantity = "unfilled_quantity"

    funding_fee = "funding_fee"

    """funding rate"""
    funding_rate = "funding_rate"
    funding_times = "funding_times"

    """transfer"""
    recipient = "recipient"
    sender = "sender"
    amount = "amount"

    """oracle_updated_price"""
    market_id = "market_id"
    oracle_price = "oracle_price"

class PositionStatus:
    Open = "open"
    Close = "close"
    Liquidated = "liquidated"

class BlockResponseValue:
    DEX_ORDER_FILL = "dex.order_fill"
    BID = "BID"
    ASK = "ASK"

class OrderFilledFields:
    PRICE = "price"
    BASE_QUANTITY = "base_quantity"
    CREATED_AT = "created_at"
    LOCKED_FEE = "locked_fee"
    MATCHED_QUANTITY = "matched_quantity"
    PAIR_ID = "pair_id"
    DIRECTION = "direction"
    QUOTE_QUANTITY = "quote_quantity"
    ORDER_TYPE = "order_type"
    OWNER = "owner"
    DEAL_PRICE = "deal_price"
    UNFILLED_QUANTITY = "unfilled_quantity"
    STATUS = "status"
    FILLED_QUANTITY = "filled_quantity"
    COST_FEE = "cost_fee"
    LEVERAGE = "leverage"
    ORDER_ID = "order_id"
    FILLED_AVERAGE_PRICE = "filled_avg_price"
    TTL = "ttl"


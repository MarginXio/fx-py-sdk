#!/usr/bin/env python
# coding='uft8'

from fx_py_sdk.model.model import OraclePrice, Order, Trade, Position
from fx_py_sdk.scan import WebsocketScan, tm_event_NewBlock
from fx_py_sdk.scan_block import TradingScanBlock

order_list = []

class MyScanBlock(TradingScanBlock):

    def on_new_order(self, order: Order, block_height: int):
        pass

    def on_new_position(self, position: Position, block_height: int):
        pass

    def on_position_change(self, position: Position, block_height: int):
        pass

    def on_position_close(self, position: Position, block_height: int):
        pass

    def on_order_fill(self, order: Order, trade: Trade, block_height: int):
        if order.order_type=='ORDER_TYPE_OPEN_POSITION' and trade.owner=='dex179q82e7fcck4ftfvf4vfpwkg86jmxf7upext3v':
            print(f'Order filled: {order.order_id} ({order.direction}), status: {order.status}, Filled qty: {trade.matched_quantity:.3f}, Block height: {block_height}')

    def on_order_cancel(self, order: Order, block_height: int):
        print(f'Order cancelled: {order.order_id}, Block height: {block_height}')

    def on_oracle_price_change(self, oracle_price: OraclePrice, block_height: int):
        pass

if __name__ == "__main__":
    WebsocketScan(subscribe_events=[tm_event_NewBlock],
                  scan=MyScanBlock())
    
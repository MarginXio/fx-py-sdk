# -*- coding: utf-8 -*-
import decimal
import threading
import time

from eth_account import Account
from google.protobuf.json_format import MessageToJson
from hs.api.trading_api import TradingAPI
from hs.common.common_utils import now_to_str
from hs.common.protobuf_utils import parse_payload
from hs.api.constant import ExchangeType, EntrustBS, EntrustType, ModelResult, EntrustEX, SessionType, CondTrackType

from fx_py_sdk.builder import TxBuilder
from fx_py_sdk.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from fx_py_sdk.grpc_client import GRPCClient
from fx_py_sdk.codec.cosmos.tx.v1beta1.service_pb2 import BROADCAST_MODE_BLOCK, BROADCAST_MODE_SYNC
from fx_py_sdk.codec.fx.dex.v1.order_pb2 import *

class HsStockTrade(object):
    """股票交易类接口独立Demo程序"""

    def __init__(self, grpc_url: str, **kwargs):
        self._trading_api = TradingAPI(**kwargs)
        # self.marginX_client = GRPCClient(grpc_url)
        self.timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._trading_api.is_alive()

    def get_token(self):
        """获取平台Token"""
        return self._trading_api.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._trading_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._trading_api.add_notify_callback(self.notify_callback)
        return self

    def entrust(self, entrust_bs: str,
                entrust_type: str,
                stock_code: str,
                entrust_amount: str,
                entrust_price: str,
                mnemonic: str,
                pair_id: str) -> ModelResult:

        # Account.enable_unaudited_hdwallet_features()
        # account = Account.from_mnemonic(mnemonic)
        # account_info = self.marginX_client.query_account_info(account.address)
        # tx_builder = TxBuilder(account, None, self.marginX_client.chain_id, account_info.account_number, Coin(amount='60', denom="USDT"))
        #
        # marginX_direction = BUY
        # if entrust_type == EntrustBS.SELL:
        #     marginX_direction = BUY
        # elif entrust_type == EntrustBS.BUY:
        #     marginX_direction = SELL
        #
        # tx_response = self.marginX_client.create_order(tx_builder, pair_id, marginX_direction, decimal.Decimal(800), decimal.Decimal(10), 5,
        #                                   account_info.sequence, mode=BROADCAST_MODE_BLOCK)

        # if tx_response.code == 0:
        """普通订单委托下单"""
        model_result = self._trading_api.entrust(iceberg_display_size="0",
                                                 session_type=SessionType.COND_ORDER_US_DEFAULT_BEFOREAFTER,
                                                 exchange="",
                                                 exchange_type=ExchangeType.P,
                                                 entrust_bs=entrust_bs,
                                                 entrust_type=entrust_type,  # 普通订单
                                                 stock_code=stock_code,
                                                 entrust_amount=entrust_amount,
                                                 entrust_price=entrust_price)
        if model_result.is_success:
            print(f"entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust(self, entrust_id: str) -> ModelResult:
        """普通订单改单"""
        model_result = self._trading_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="561.500")
        if model_result.is_success:
            print(f"change_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust(self, entrust_id: str,
                       stock_code: str,
                       entrust_amount: str,
                       entrust_price: str,
                       order_id: str) -> ModelResult:
        """普通撤单"""
        model_result = self._trading_api.cancel_entrust(exchange_type=ExchangeType.P,
                                                        entrust_id=entrust_id,
                                                        stock_code=stock_code,
                                                        entrust_amount=entrust_amount,
                                                        entrust_price=entrust_price)
        if model_result.is_success:
            print(f"cancel_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def entrust_cond(self) -> ModelResult:
        """条件单委托下单"""
        model_result = self._trading_api.entrust(iceberg_display_size="",
                                                 session_type=SessionType.COND_ORDER_DEFAULT,  # 只支持盘中
                                                 exchange="",
                                                 exchange_type=ExchangeType.K,
                                                 entrust_bs=EntrustBS.SELL,  # 卖出
                                                 entrust_type=EntrustType.COND_STOP_PROFIT_POINT,  # 条件单-止盈限价单
                                                 stock_code="00700.HK",
                                                 entrust_amount="100",  # 委托数量
                                                 entrust_price="515",  # 委托下单指定价格，当条件触发时的委托下单价格
                                                 valid_days="10",  # 有效天数
                                                 cond_value="511",  # 止盈价格, 可能值：价格、价差、百分比数字
                                                 cond_track_type="")  # 如果为跟踪订单该值必填, 1百分比、2价差, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单改单"""
        model_result = self._trading_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="535",  # 委托下单指定价格，当条件触发时的委托下单价格
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT,
                                                        # 传原下单委托类型，不允许修改
                                                        session_type=SessionType.COND_ORDER_HK_DEFAULT_HIDDEN,
                                                        # 修改为 '支持盘中及暗盘'
                                                        valid_days="25",  # 有效期修改为15天
                                                        cond_value="533",  # 价格条件修改为533
                                                        cond_track_type="")  # 不是跟踪订单，该值为空, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"change_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单撤单"""
        model_result = self._trading_api.cancel_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="",
                                                        entrust_price="",
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT)  # 传原下单委托类型，不允许修改
        if model_result.is_success:
            print(f"cancel_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_holds_list(self):
        """查询持仓股票列表"""
        model_result = self._trading_api.query_holds_list(exchange_type=ExchangeType.P)
        if model_result.is_success:
            holds_list = model_result.get_model()
            if len(holds_list) < 0:
                print(f"在当前交易市场没有持仓！")
            else:
                for holds in holds_list:
                    print(f"持仓股票名称：{holds.stockName}, 详细信息：{holds}")
        else:
            print(f"fail to query_holds_list，code：{model_result.code}, msg：{model_result.msg}")
        return model_result.get_model()

    def query_buy_amount(self):
        """获取最大可买数量"""
        model_result = self._trading_api.query_buy_amount(exchange_type=ExchangeType.K,
                                                          stock_code="00700.HK",
                                                          entrust_price="510.00")
        if model_result.is_success:
            print(f"最大可买数量：{model_result.get_model()}")
        else:
            print(f"fail to query_buy_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_sell_amount(self):
        """获取最大可卖数量"""
        model_result = self._trading_api.query_sell_amount(exchange_type=ExchangeType.K, stock_code="00700.HK")
        if model_result.is_success:
            print(f"最大可卖数量：{model_result.get_model()}")
        else:
            print(f"fail to query_sell_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_margin_fund_info(self):
        """查询客户资金信息"""
        model_result = self._trading_api.query_margin_fund_info(exchange_type=ExchangeType.P)
        if model_result.is_success:
            print(f"客户资金信息：{model_result.get_model()}")
        else:
            print(f"fail to query_margin_fund_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_entrust_list(self, entrust_id: list):
        """查询客户当日委托信息"""
        model_result = self._trading_api.query_real_entrust_list(exchange_type=ExchangeType.P,
                                                                 query_count=20,
                                                                 query_param_str="0",
                                                                 entrust_ids=entrust_id)
        if model_result.is_success:
            print(f"客户当日委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_entrust_list(self, start_date: str):
        """查询客户历史委托信息"""
        model_result = self._trading_api.query_history_entrust_list(exchange_type=ExchangeType.P,
                                                                    query_count=20,
                                                                    query_param_str="0",
                                                                    start_date=start_date,
                                                                    end_date=now_to_str())
        if model_result.is_success:
            print(f"查询客户历史委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_deliver_list(self):
        """查询客户当日成交信息"""
        model_result = self._trading_api.query_real_deliver_list(exchange_type=ExchangeType.K,
                                                                 query_count=20,
                                                                 query_param_str="0")
        if model_result.is_success:
            print(f"客户当日成交信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_deliver_list(self):
        """查询客户历史成交信息"""
        model_result = self._trading_api.query_history_deliver_list(exchange_type=ExchangeType.K,
                                                                    query_count=20,
                                                                    query_param_str="0",
                                                                    start_date="20201210",
                                                                    end_date=now_to_str())
        if model_result.is_success:
            print(f"客户历史成交信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_fund_jour_list(self):
        """查询客户当日资金流水列表"""
        model_result = self._trading_api.query_real_fund_jour_list(exchange_type=ExchangeType.K,
                                                                   query_count=20,
                                                                   query_param_str="0")
        if model_result.is_success:
            print(f"客户当日资金流水列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_fund_jour_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_fund_jour_list(self):
        """查询客户历史资金流水列表"""
        model_result = self._trading_api.query_history_fund_jour_list(exchange_type=ExchangeType.K,
                                                                      query_count=20,
                                                                      query_param_str="0",
                                                                      start_date="20201210",
                                                                      end_date=now_to_str())
        if model_result.is_success:
            print(f"客户历史资金流水列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_fund_jour_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_before_and_after_support(self):
        """查询是否支持盘前盘后交易"""
        model_result = self._trading_api.query_before_and_after_support(stock_code="TSLA",
                                                                        exchange_type=ExchangeType.P)
        if model_result.is_success:
            print(f"是否支持盘前盘后交易：{model_result.get_model()}")
        else:
            print(f"fail to query_before_and_after_support, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_max_available_asset(self):
        """查询最大可用资产"""
        model_result = self._trading_api.query_max_available_asset(exchange_type=ExchangeType.P,
                                                                   stock_code="AAPL",
                                                                   entrust_price="142",
                                                                   entrust_type=EntrustType.MARKET)
        if model_result.is_success:
            print(f"查询最大可用资产：{model_result.get_model()}")
        else:
            print(f"fail to query_max_available_asset, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_stock_short_info(self):
        """查询股票沽空信息"""
        model_result = self._trading_api.query_stock_short_info(exchange_type=ExchangeType.P,
                                                                stock_code="AAPL")
        if model_result.is_success:
            print(f"查询股票沽空信息：{model_result.get_model()}")
        else:
            print(f"fail to query_stock_short_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_cond_order_list(self):
        """查询当日条件单列表"""
        model_result = self._trading_api.query_real_cond_order_list(exchange_type=ExchangeType.K,
                                                                    stock_code="",
                                                                    page_no=1,
                                                                    page_size=20)
        if model_result.is_success:
            print(f"查询当日条件单列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_cond_order_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_cond_order_list(self):
        """查询历史条件单列表"""
        model_result = self._trading_api.query_history_cond_order_list(start_time="2021-01-01 19:21:21",
                                                                       end_time="2021-01-02 19:21:21",
                                                                       exchange_type=ExchangeType.K,
                                                                       stock_code="",
                                                                       page_no=1,
                                                                       page_size=20)
        if model_result.is_success:
            print(f"查询历史条件单列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_cond_order_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def trade_subscribe(self):
        """订阅交易推送消息"""
        model_result = self._trading_api.trade_subscribe()
        if model_result.is_success:
            print(f"订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_subscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def trade_unsubscribe(self):
        """取消订阅交易推送消息"""
        model_result = self._trading_api.trade_unsubscribe()
        if model_result.is_success:
            print(f"取消订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_unsubscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def notify_callback(self, pb_notify):
        """
        定义处理消息推送的callback
        :param pb_notify  参考 PBNotify.proto
        """
        print(f"trading notify_callback，pb_notify：{pb_notify}，payload：{parse_payload(pb_notify)}")

    def timer_callback(self, interval=30):
        """"
        增加线程接口轮询，维持登录态
        """
        self.timer_threading = threading.Timer(interval, self.timer_callback, (interval,))
        self.timer_threading.setDaemon(False)
        self.timer_threading.start()
        self.query_holds_list()

    def stop(self):
        """退出业务API上下文环境"""
        self.timer_threading.cancel()
        self._trading_api.stop()

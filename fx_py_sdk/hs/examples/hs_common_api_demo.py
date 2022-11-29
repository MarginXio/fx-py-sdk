# -*- coding: utf-8 -*-

import threading
import time

from hs.api.constant import DataType, Direction, ExRightFlag, CycType, SecurityParam, HQSubscribeTopicId, \
    MktTmType, DepthBookType, ExchangeType, EntrustType, EntrustEX, EntrustBS, ModelResult, FuturesEntrustType, \
    FuturesValidTimeType, SessionType
from hs.api.hs_common_api import CommonAPI
from hs.common.common_utils import now_to_str
from hs.common.protobuf_utils import parse_payload


class HsCommonApiDemo(object):
    """交易、行情、期货接口统一Demo程序"""

    def __init__(self, **kwargs):
        self._common_api = CommonAPI(**kwargs)
        self.timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._common_api.is_alive()

    def get_token(self):
        """获取平台Token"""
        return self._common_api.get_token()
    
    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._common_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._common_api.add_notify_callback(self.notify_callback)
        return self

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
        time.sleep(2)
        self.query_hq_basic_qot()

    def stop(self):
        """退出业务API上下文环境"""
        self.timer_threading.cancel()
        self._common_api.stop()

    ##########################################      Trading API      ##################################################
    def entrust(self) -> ModelResult:
        """委托下单"""
        model_result = self._common_api.entrust(iceberg_display_size="0",
                                                 session_type=SessionType.GENERAL_ORDER_NO,
                                                 exchange=EntrustEX.ARCA,
                                                 exchange_type=ExchangeType.K,
                                                 entrust_bs=EntrustBS.BUY,
                                                 entrust_type=EntrustType.LIMIT,
                                                 stock_code="00700.HK",
                                                 entrust_amount="100",
                                                 entrust_price="561.500")
        if model_result.is_success:
            print(f"entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust(self, entrust_id: str) -> ModelResult:
        """改单"""
        model_result = self._common_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="561.500")
        if model_result.is_success:
            print(f"change_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust(self, entrust_id: str) -> ModelResult:
        """撤单"""
        model_result = self._common_api.cancel_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="561.500")
        if model_result.is_success:
            print(f"cancel_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def entrust_cond(self) -> ModelResult:
        """条件单委托下单"""
        model_result = self._common_api.entrust(iceberg_display_size="",
                                                 session_type=SessionType.COND_ORDER_DEFAULT, # 只支持盘中
                                                 exchange="",
                                                 exchange_type=ExchangeType.K,
                                                 entrust_bs=EntrustBS.SELL, # 卖出
                                                 entrust_type=EntrustType.COND_STOP_PROFIT_POINT, # 条件单-止盈限价单
                                                 stock_code="00700.HK",
                                                 entrust_amount="100", # 委托数量
                                                 entrust_price="515", # 委托下单指定价格，当条件触发时的委托下单价格
                                                 valid_days="10", # 有效天数
                                                 cond_value="511", # 止盈价格, 可能值：价格、价差、百分比数字
                                                 cond_track_type="") # 如果为跟踪订单该值必填, 1百分比、2价差, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单改单"""
        model_result = self._common_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="535", # 委托下单指定价格，当条件触发时的委托下单价格
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT, # 传原下单委托类型，不允许修改
                                                        session_type=SessionType.COND_ORDER_HK_DEFAULT_HIDDEN, # 修改为 '支持盘中及暗盘'
                                                        valid_days="25", # 有效期修改为15天
                                                        cond_value="533", # 价格条件修改为533
                                                        cond_track_type="") # 不是跟踪订单，该值为空, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"change_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单撤单"""
        model_result = self._common_api.cancel_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="",
                                                        entrust_price="",
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT) # 传原下单委托类型，不允许修改
        if model_result.is_success:
            print(f"cancel_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result
    
    def query_holds_list(self):
        """查询持仓股票列表"""
        model_result = self._common_api.query_holds_list(exchange_type=ExchangeType.K)
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
        model_result = self._common_api.query_buy_amount(exchange_type=ExchangeType.K,
                                                          stock_code="00700.HK",
                                                          entrust_price="510.00")
        if model_result.is_success:
            print(f"最大可买数量：{model_result.get_model()}")
        else:
            print(f"fail to query_buy_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_sell_amount(self):
        """获取最大可卖数量"""
        model_result = self._common_api.query_sell_amount(exchange_type=ExchangeType.K, stock_code="00700.HK")
        if model_result.is_success:
            print(f"最大可卖数量：{model_result.get_model()}")
        else:
            print(f"fail to query_sell_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_margin_fund_info(self):
        """查询客户资金信息"""
        model_result = self._common_api.query_margin_fund_info(exchange_type=ExchangeType.K)
        if model_result.is_success:
            print(f"客户资金信息：{model_result.get_model()}")
        else:
            print(f"fail to query_margin_fund_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_entrust_list(self, entrust_id: list):
        """查询客户当日委托信息"""
        model_result = self._common_api.query_real_entrust_list(exchange_type=ExchangeType.K,
                                                                 query_count=20,
                                                                 query_param_str="0",
                                                                 entrust_ids = entrust_id)
        if model_result.is_success:
            print(f"客户当日委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_entrust_list(self):
        """查询客户历史委托信息"""
        model_result = self._common_api.query_history_entrust_list(exchange_type=ExchangeType.K,
                                                                    query_count=20,
                                                                    query_param_str="0",
                                                                    start_date="20201010",
                                                                    end_date=now_to_str())
        if model_result.is_success:
            print(f"查询客户历史委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_deliver_list(self):
        """查询客户当日成交信息"""
        model_result = self._common_api.query_real_deliver_list(exchange_type=ExchangeType.K,
                                                                 query_count=20,
                                                                 query_param_str="0")
        if model_result.is_success:
            print(f"客户当日成交信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_deliver_list(self):
        """查询客户历史成交信息"""
        model_result = self._common_api.query_history_deliver_list(exchange_type=ExchangeType.K,
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
        model_result = self._common_api.query_real_fund_jour_list(exchange_type=ExchangeType.K,
                                                                   query_count=20,
                                                                   query_param_str="0")
        if model_result.is_success:
            print(f"客户当日资金流水列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_fund_jour_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_fund_jour_list(self):
        """查询客户历史资金流水列表"""
        model_result = self._common_api.query_history_fund_jour_list(exchange_type=ExchangeType.K,
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
        model_result = self._common_api.query_before_and_after_support(stock_code="TSLA",
                                                                        exchange_type=ExchangeType.P)
        if model_result.is_success:
            print(f"是否支持盘前盘后交易：{model_result.get_model()}")
        else:
            print(f"fail to query_before_and_after_support, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_max_available_asset(self):
        """查询最大可用资产"""
        model_result = self._common_api.query_max_available_asset(exchange_type=ExchangeType.P,
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
        model_result = self._common_api.query_stock_short_info(exchange_type=ExchangeType.P,
                                                                stock_code="AAPL")
        if model_result.is_success:
            print(f"查询股票沽空信息：{model_result.get_model()}")
        else:
            print(f"fail to query_stock_short_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_cond_order_list(self):
        """查询当日条件单列表"""
        model_result = self._common_api.query_real_cond_order_list(exchange_type=ExchangeType.K,
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
        model_result = self._common_api.query_history_cond_order_list(start_time="2021-01-01 19:21:21",
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
        model_result = self._common_api.trade_subscribe()
        if model_result.is_success:
            print(f"订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_subscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def trade_unsubscribe(self):
        """取消订阅交易推送消息"""
        model_result = self._common_api.trade_unsubscribe()
        if model_result.is_success:
            print(f"取消订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_unsubscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    ##########################################      Quote API    ##################################################
    def query_hq_basic_qot(self) -> ModelResult:
        """批量查询股票基础报价"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.query_hq_basic_qot(security_list=security_list)
        if model_result.is_success:
            print(f"hq basic quote：{model_result.get_model()}")
        else:
            print(f"fail to query hq basic quote, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_broker(self) -> ModelResult:
        """查询买卖经纪摆盘"""
        model_result = self._common_api.query_hq_broker(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"))
        if model_result.is_success:
            print(f"hq broker：{model_result.get_model()}")
        else:
            print(f"fail to query hq broker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_order_book(self) -> ModelResult:
        """查询买卖档"""
        model_result = self._common_api.query_order_book(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
                                                        mkt_tm_type=MktTmType.MID_SESSION)
        if model_result.is_success:
            print(f"order book：{model_result.get_model()}")
        else:
            print(f"fail to query order book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_ticker(self) -> ModelResult:
        """查询最近多少条的逐笔列表"""
        model_result = self._common_api.query_hq_ticker(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
                                                       limit=10)
        if model_result.is_success:
            print(f"hq ticker：{model_result.get_model()}")
        else:
            print(f"fail to query hq ticker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_kline(self) -> ModelResult:
        """查询K线数据"""
        model_result = self._common_api.query_hq_kline(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
                                                      start_date="20201203",
                                                      direction=Direction.QUERY_LEFT,
                                                      ex_right_flag=ExRightFlag.BFQ,
                                                      cyc_type=CycType.DAY,
                                                      limit=10)
        if model_result.is_success:
            print(f"hq kline：{model_result.get_model()}")
        else:
            print(f"fail to query hq kline, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_time_share(self) -> ModelResult:
        """查询分时数据"""
        model_result = self._common_api.query_hq_time_share(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"))
        if model_result.is_success:
            print(f"hq time share：{model_result.get_model()}")
        else:
            print(f"fail to query hq time share, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_depth_order_book(self):
        """查询深度摆盘数据"""
        model_result = self._common_api.query_order_book(security_param=SecurityParam(DataType.US_STOCK, "BABA"),
                                                        mkt_tm_type=MktTmType.PRE_MARKET,
                                                        depth_book_type=DepthBookType.TOTAL_VIEW)
        if model_result.is_success:
            print(f"depth order book：{model_result.get_model()}")
        else:
            print(f"fail to query depth order book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def hq_subscribe_basic_qot(self):
        """订阅基础行情推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.BASIC_QOT,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅基础行情推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe basic_qot, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_subscribe_ticker(self):
        """订阅逐笔推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.TICKER,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅逐笔推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe ticker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_subscribe_broker(self):
        """订阅买卖经纪推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.BROKER,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅买卖经纪推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe broker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_subscribe_order_book(self):
        """订阅买卖档推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.ORDER_BOOK,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅买卖档推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe orderbook, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_subscribe_total_view_book(self):
        """订阅深度摆盘TOTALVIEW推送消息"""
        security_list = [SecurityParam(DataType.US_STOCK, "BABA"),
                         SecurityParam(DataType.US_STOCK, "AAPL")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.TOTALVIEW_BOOK,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅深度摆盘TOTALVIEW推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe totalview book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_subscribe_arca_book(self):
        """订阅深度摆盘ARCABOOK推送消息"""
        security_list = [SecurityParam(DataType.US_STOCK, "BABA"),
                         SecurityParam(DataType.US_STOCK, "AAPL")]
        model_result = self._common_api.hq_subscribe(topic_id=HQSubscribeTopicId.ARCA_BOOK,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"订阅深度摆盘ARCABOOK推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_subscribe arca book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_basic_qot(self):
        """取消订阅基础行情推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.BASIC_QOT,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅基础行情推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe basic_qot, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_ticker(self):
        """取消订阅逐笔推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.TICKER,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅逐笔推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe ticker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_broker(self):
        """取消订阅买卖经纪推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.BROKER,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅买卖经纪推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe broker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_order_book(self):
        """取消订阅买卖档推送消息"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.ORDER_BOOK,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅买卖档推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe orderbook, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_total_view_book(self):
        """取消订阅深度摆盘TOTALVIEW推送消息"""
        security_list = [SecurityParam(DataType.US_STOCK, "BABA"),
                         SecurityParam(DataType.US_STOCK, "AAPL")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.TOTALVIEW_BOOK,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅深度摆盘TOTALVIEW推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe totalview book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def hq_unsubscribe_arca_Book(self):
        """取消订阅深度摆盘ARCABOOK推送消息"""
        security_list = [SecurityParam(DataType.US_STOCK, "BABA"),
                         SecurityParam(DataType.US_STOCK, "AAPL")]
        model_result = self._common_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.ARCA_BOOK,
                                                      security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅深度摆盘ARCABOOK推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe arca book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    ########################################## Futures API ##################################################
    def futures_entrust(self) -> ModelResult:
        """期货委托下单"""
        model_result = self._common_api.futures_entrust(stock_code="CUSH2",
                                                         entrust_type=FuturesEntrustType.LIMIT,
                                                         entrust_price="5.5",
                                                         entrust_amount="100",
                                                         entrust_bs=EntrustBS.BUY,
                                                         valid_time_type=FuturesValidTimeType.VALID_ON_SPECIFIED_DATE,
                                                         valid_time="20221230",
                                                         order_options="0")
        if model_result.is_success:
            print(f"futures entrust_id：{model_result.get_model()}")
        else:
            print(f"futures fail to entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def futures_change_entrust(self, entrust_id: str) -> ModelResult:
        """期货改单"""
        model_result = self._common_api.futures_change_entrust(entrust_id=entrust_id,
                                                                stock_code="CUSH2",
                                                                entrust_price="6.2",
                                                                entrust_amount="100",
                                                                entrust_bs=EntrustBS.BUY,
                                                                valid_time_type=FuturesValidTimeType.VALID_ON_SPECIFIED_DATE,
                                                                valid_time="20221230",
                                                                order_options="0")
        if model_result.is_success:
            print(f"futures change_entrust_id：{model_result.get_model()}")
        else:
            print(f"futures fail to change entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def futures_cancel_entrust(self, entrust_id: str) -> ModelResult:
        """期货撤单"""
        model_result = self._common_api.futures_cancel_entrust(entrust_id=entrust_id,
                                                                stock_code="CUSH2")
        if model_result.is_success:
            print(f"futures cancel_entrust_id：{model_result.get_model()}")
        else:
            print(f"futures fail to cancel entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def futures_query_holds_list(self):
        """期货查询持仓"""
        model_result = self._common_api.futures_query_holds_list()
        if model_result.is_success:
            model = model_result.get_model()
            print(f"期货查询持仓，资金信息：{model.fundInfo}")
            if len(model.holdsList) <= 0:
                print(f"futures query_holds_list，holds list empty.")
            else:
                for holds in model.holdsList:
                    print(f"期货查询持仓, code：{holds.stockCode}, name：{holds.stockName}")
        else:
            print(f"futures fail to query_holds_list，code：{model_result.code}, msg：{model_result.msg}")
        return model_result.get_model()

    def futures_query_fund_info(self):
        """期货查询资金信息"""
        model_result = self._common_api.futures_query_fund_info()
        if model_result.is_success:
            print(f"期货查询资金信息：{model_result.get_model()}")
        else:
            print(f"futures fail to query_fund_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_max_buy_sell_amount(self):
        """查询期货最大可买/卖"""
        model_result = self._common_api.futures_query_max_buy_sell_amount(stock_code="CUSH2")
        if model_result.is_success:
            print(f"查询期货最大可买/卖：{model_result.get_model()}")
        else:
            print(f"futures fail to query_max_buy_sell_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_real_entrust_list(self):
        """期货查询今日委托"""
        model_result = self._common_api.futures_query_real_entrust_list()
        if model_result.is_success:
            print(f"期货查询今日委托：{model_result.get_model()}")
        else:
            print(f"futures fail to query_real_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_history_entrust_list(self):
        """期货查询历史委托"""
        model_result = self._common_api.futures_query_history_entrust_list(page_no=1,
                                                                            page_size=20,
                                                                            start_date="20211220",
                                                                            end_date=now_to_str())
        if model_result.is_success:
            print(f"期货查询历史委托：{model_result.get_model()}")
        else:
            print(f"futures fail to query_history_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_real_deliver_list(self):
        """期货查询今日成交"""
        model_result = self._common_api.futures_query_real_deliver_list()
        if model_result.is_success:
            print(f"期货查询今日成交：{model_result.get_model()}")
        else:
            print(f"futures fail to query_real_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_history_deliver_list(self):
        """期货查询历史成交"""
        model_result = self._common_api.futures_query_history_deliver_list(page_no=1,
                                                                            page_size=20,
                                                                            start_date='20211220',
                                                                            end_date=now_to_str())
        if model_result.is_success:
            print(f"期货查询历史成交：{model_result.get_model()}")
        else:
            print(f"futures fail to query_history_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_product_info(self):
        """期货查询产品信息"""
        stock_code_list = list()
        stock_code_list.append("CUSH2")
        model_result = self._common_api.futures_query_product_info(stock_code_list)
        if model_result.is_success:
            print(f"期货查询产品信息：{model_result.get_model()}")
        else:
            print(f"futures fail to query_product_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_trade_subscribe(self):
        """期货订阅交易推送消息"""
        model_result = self._common_api.trade_subscribe()
        if model_result.is_success:
            print(f"订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_subscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_trade_unsubscribe(self):
        """取消订阅期货交易推送消息"""
        model_result = self._common_api.trade_unsubscribe()
        if model_result.is_success:
            print(f"取消订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_unsubscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()
    


if __name__ == '__main__':
    # 1、配置启动参数
    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                            "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                            "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ENCRYPT_RSA_PRIVATEKEY = "<<your encrypt rsa private key>>"
    params = {
        "rsa_public_key": ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://openapi-daily.hstong.com",  # 生产环境domain为：https://openapi.hstong.com
        "login_country_code": "CHN", # 如果为香港或美国地区手机号，需要修改为对应区域编码，区域编码查询：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8
        "login_mobile": "<<your login mobile>>", # 登录账号无需加区号
        "login_passwd": "<<your login password>>",
        "trading_passwd": "<<your trading password>>",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 2、初始化Common API对象、增加消息推送回调函数
    common_api_demo = HsCommonApiDemo(**params).add_notify_callback()
    # 3、执行HTTP登录、获取token及连接ip port
    token = common_api_demo.get_token()
    # 4、启动Common API上下文，并会初始化连接、交易登录
    common_api_demo.start(token)
    # 5、检查连接状态
    is_alive = common_api_demo.check_alive()

    if is_alive:
        # 增加线程接口轮询，维持登录态
        common_api_demo.timer_callback(interval=30)
        
        entrustResult = None
        # 6、命令形式展示  
        while True:
            print("###### 接口名: query_margin_fund_info，            接口描述: 交易接口-查询客户资金信息									######")
            print("###### 接口名: query_holds_list，                  接口描述: 交易接口-查询持仓股票列表									######")
            print("###### 接口名: query_buy_amount，                  接口描述: 交易接口-获取最大可买数量									######")
            print("###### 接口名: query_sell_amount，                 接口描述: 交易接口-获取最大可卖数量									######")
            print("###### 接口名: query_real_fund_jour_list，         接口描述: 交易接口-查询客户当日资金流水列表							######")
            print("###### 接口名: query_history_fund_jour_list，      接口描述: 交易接口-查询客户历史资金流水列表							######")
            print("###### 接口名: entrust，                           接口描述: 订单接口-委托/改单/撤单										######")
            print("###### 接口名: entrust_cond，                      接口描述: 订单接口-条件单委托/改单/撤单								######")
            print("###### 接口名: query_real_entrust_list，           接口描述: 订单接口-查询客户当日委托信息								######")
            print("###### 接口名: query_history_entrust_list，        接口描述: 订单接口-查询客户历史委托信息								######")
            print("###### 接口名: query_real_deliver_list，           接口描述: 订单接口-查询客户当日成交信息								######")
            print("###### 接口名: query_history_deliver_list，        接口描述: 订单接口-查询客户历史成交信息								######")
            print("###### 接口名: query_before_and_after_support，    接口描述: 订单接口-查询是否支持盘前盘后交易						    ######")
            print("###### 接口名: query_max_available_asset，         接口描述: 订单接口-查询最大可用资产						            ######")
            print("###### 接口名: query_stock_short_info，            接口描述: 订单接口-查询股票沽空信息       						    ######")
            print("###### 接口名: query_real_cond_order_list，        接口描述: 订单接口-查询当日条件单列表      						    ######")
            print("###### 接口名: query_history_cond_order_list，     接口描述: 订单接口-查询历史条件单列表       						    ######")
            print("###### 接口名: trade_subscribe，                   接口描述: 订单接口-订阅交易推送消息									######")
            print("###### 接口名: trade_unsubscribe，                 接口描述: 订单接口-取消订阅交易推送消息								######")
            print("###### 接口名: query_hq_basic_qot，                接口描述: 行情接口-基础报价                                           ######")
            print("###### 接口名: query_hq_broker，                   接口描述: 行情接口-买卖经纪摆盘                                       ######")
            print("###### 接口名: query_order_book，                  接口描述: 行情接口-查询买卖档                                         ######")
            print("###### 接口名: query_hq_ticker，                   接口描述: 行情接口-查询最近多少条的逐笔列表                           ######")
            print("###### 接口名: query_hq_kline，                    接口描述: 行情接口-K线数据                                            ######")
            print("###### 接口名: query_hq_time_share，               接口描述: 行情接口-查询分时数据                                       ######")
            print("###### 接口名: query_depth_order_book，            接口描述: 行情接口-查询深度摆盘数据                                   ######")
            print("###### 接口名: hq_subscribe_basic_qot，            接口描述: 行情接口-订阅基础行情推送消息（需要时才使用）               ######")
            print("###### 接口名: hq_subscribe_ticker，               接口描述: 行情接口-订阅逐笔推送消息（需要时才使用）                   ######")
            print("###### 接口名: hq_subscribe_broker，               接口描述: 行情接口-订阅买卖经纪推送消息（需要时才使用）               ######")
            print("###### 接口名: hq_subscribe_order_book，           接口描述: 行情接口-订阅买卖档推送消息（需要时才使用）                 ######")
            print("###### 接口名: hq_subscribe_total_view_book，      接口描述: 行情接口-订阅深度摆盘TOTALVIEW推送消息（需要时才使用）      ######")
            print("###### 接口名: hq_subscribe_arca_book，            接口描述: 行情接口-订阅深度摆盘ARCABOOK推送消息（需要时才使用）       ######")
            print("###### 接口名: hq_unsubscribe_basic_qot，          接口描述: 行情接口-取消订阅基础行情推送消息（需要时才使用）           ######")
            print("###### 接口名: hq_unsubscribe_ticker，             接口描述: 行情接口-取消订阅逐笔推送消息（需要时才使用）               ######")
            print("###### 接口名: hq_unsubscribe_broker，             接口描述: 行情接口-取消订阅买卖经纪推送消息（需要时才使用）           ######")
            print("###### 接口名: hq_unsubscribe_order_book，         接口描述: 行情接口-取消订阅买卖档推送消息（需要时才使用）             ######")
            print("###### 接口名: hq_unsubscribe_total_view_book，    接口描述: 行情接口-取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用）  ######")
            print("###### 接口名: hq_unsubscribe_arca_book，          接口描述: 行情接口-取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）   ######")
            print("###### 接口名: futures_entrust，                   接口描述: 期货接口-期货委托/改单/撤单                                 ######")
            print("###### 接口名: futures_query_holds_list，          接口描述: 期货接口-期货查询持仓                                       ######")
            print("###### 接口名: futures_query_fund_info，           接口描述: 期货接口-期货查询资金信息                                   ######")
            print("###### 接口名: futures_query_max_buy_sell_amount， 接口描述: 期货接口-查询期货最大可买/卖                                ######")
            print("###### 接口名: futures_query_real_entrust_list，   接口描述: 期货接口-期货查询今日委托                                   ######")
            print("###### 接口名: futures_query_history_entrust_list，接口描述: 期货接口-期货查询历史委托                                   ######")
            print("###### 接口名: futures_query_real_deliver_list，   接口描述: 期货接口-期货查询今日成交                                   ######")
            print("###### 接口名: futures_query_history_deliver_list，接口描述: 期货接口-期货查询历史成交                                   ######")
            print("###### 接口名: futures_query_product_info，        接口描述: 期货接口-期货查询产品信息                                   ######")
            print("###### 接口名: futures_trade_subscribe，           接口描述: 期货订阅接口-期货订阅交易推送消息                           ######")
            print("###### 接口名: futures_trade_unsubscribe，         接口描述: 期货订阅接口-取消订阅期货交易推送消息                       ######")
            print("###### 接口名: stop，                              接口描述: ！！！程序退出，该函数将退出交易登录，并断开TCP链接！！！	######")
            method_name = input("请输入需要查看的接口名: ")
    
            if method_name == "query_margin_fund_info":
                # 交易接口-查询客户资金信息
                common_api_demo.query_margin_fund_info()
            elif method_name == "query_holds_list":
                # 查询持仓股票列表
                common_api_demo.query_holds_list()
            elif method_name == "query_buy_amount":
                # 获取最大可买数量
                common_api_demo.query_buy_amount()
            elif method_name == "query_sell_amount":
                # 获取最大可卖数量
                common_api_demo.query_sell_amount()
            elif method_name == "query_real_fund_jour_list":
                # 查询客户当日资金流水列表
                common_api_demo.query_real_fund_jour_list()
            elif method_name == "query_history_fund_jour_list":
                # 查询客户历史资金流水列表
                common_api_demo.query_history_fund_jour_list()
            elif method_name == "entrust":
                # 委托下单
                entrustResult = common_api_demo.entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = common_api_demo.change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # common_api_demo.cancel_entrust(entrustResult.get_model())
            elif method_name == "entrust_cond":
                # 条件单委托下单
                entrustResult = common_api_demo.entrust_cond()
                time.sleep(1)
                # 条件单改单（需要时才改单）
                # result = common_api_demo.change_entrust_cond(entrustResult.get_model())
                time.sleep(1)
                # 条件单撤单（需要时才撤单）
                # common_api_demo.cancel_entrust_cond(entrustResult.get_model())
            elif method_name == "query_real_entrust_list":
                # 查询客户当日委托信息
                if entrustResult is not None:
                    entrustIds = list()
                    entrustIds.append(entrustResult.get_model())
                    common_api_demo.query_real_entrust_list(entrustIds)
                else:
                    common_api_demo.query_real_entrust_list(list())
            elif method_name == "query_history_entrust_list":
                # 查询客户历史委托信息
                common_api_demo.query_history_entrust_list()
            elif method_name == "query_real_deliver_list":
                # 查询客户当日成交信息
                common_api_demo.query_real_deliver_list()
            elif method_name == "query_history_deliver_list":
                # 查询客户历史成交信息
                common_api_demo.query_history_deliver_list()
            elif method_name == "query_before_and_after_support":
                # 查询是否支持盘前盘后交易
                common_api_demo.query_before_and_after_support()
            elif method_name == "query_max_available_asset":
                # 查询最大可用资产
                common_api_demo.query_max_available_asset()
            elif method_name == "query_stock_short_info":
                # 查询股票沽空信息
                common_api_demo.query_stock_short_info()
            elif method_name == "query_real_cond_order_list":
                # 查询当日条件单列表
                common_api_demo.query_real_cond_order_list()
            elif method_name == "query_history_cond_order_list":
                # 查询历史条件单列表
                common_api_demo.query_history_cond_order_list()
            elif method_name == "trade_subscribe":
                # 订阅交易推送消息（需要时才使用）
                common_api_demo.trade_subscribe()
            elif method_name == "trade_unsubscribe":
                # 取消订阅交易推送消息（需要时才使用）
                common_api_demo.trade_unsubscribe()
            if method_name == "query_hq_basic_qot":
                # 批量查询股票基础报价
                common_api_demo.query_hq_basic_qot()
            elif method_name == "query_hq_broker":
                # 查询买卖经纪摆盘
                common_api_demo.query_hq_broker()
            elif method_name == "query_order_book":
                # 查询买卖档
                common_api_demo.query_order_book()
            elif method_name == "query_hq_ticker":
                # 查询最近多少条的逐笔列表
                common_api_demo.query_hq_ticker()
            elif method_name == "query_hq_kline":
                # 查询K线数据
                common_api_demo.query_hq_kline()
            elif method_name == "query_hq_time_share":
                # 查询分时数据
                common_api_demo.query_hq_time_share()
            elif method_name == "query_depth_order_book":
                # 查询深度摆盘数据
                common_api_demo.query_depth_order_book()
            elif method_name == "hq_subscribe_basic_qot":
                # 订阅基础行情推送消息（需要时才使用）
                common_api_demo.hq_subscribe_basic_qot()
            elif method_name == "hq_subscribe_ticker":
                # 订阅逐笔推送消息（需要时才使用）
                common_api_demo.hq_subscribe_ticker()
            elif method_name == "hq_subscribe_broker":
                # 订阅买卖经纪推送消息（需要时才使用）
                common_api_demo.hq_subscribe_broker()
            elif method_name == "hq_subscribe_order_book":
                # 订阅买卖档推送消息（需要时才使用）
                common_api_demo.hq_subscribe_order_book()
            elif method_name == "hq_subscribe_total_view_book":
                # 订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                common_api_demo.hq_subscribe_total_view_book()
            elif method_name == "hq_subscribe_arca_book":
                # 订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                common_api_demo.hq_subscribe_arca_book()
            elif method_name == "hq_unsubscribe_basic_qot":
                # 取消订阅基础行情推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_basic_qot()
            elif method_name == "hq_unsubscribe_ticker":
                # 取消订阅逐笔推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_ticker()
            elif method_name == "hq_unsubscribe_broker":
                # 取消订阅买卖经纪推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_broker()
            elif method_name == "hq_unsubscribe_order_book":
                # 取消订阅买卖档推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_order_book()
            elif method_name == "hq_unsubscribe_total_view_book":
                # 取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_total_view_book()
            elif method_name == "hq_unsubscribe_arca_Book":
                # 取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_arca_Book()
            if method_name == "futures_entrust":
                # 委托下单
                entrustResult = common_api_demo.futures_entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = common_api_demo.futures_change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # common_api_demo.futures_cancel_entrust(entrustResult.get_model())
            elif method_name == "futures_query_holds_list":
                # 查询接口-期货查询持仓
                common_api_demo.futures_query_holds_list()
            elif method_name == "futures_query_fund_info":
                # 查询接口-期货查询资金信息
                common_api_demo.futures_query_fund_info()
            elif method_name == "futures_query_max_buy_sell_amount":
                # 查询接口-查询期货最大可买/卖
                common_api_demo.futures_query_max_buy_sell_amount()
            elif method_name == "futures_query_real_entrust_list":
                # 查询接口-期货查询今日委托
                common_api_demo.futures_query_real_entrust_list()
            elif method_name == "futures_query_history_entrust_list":
                # 查询接口-期货查询历史委托
                common_api_demo.futures_query_history_entrust_list()
            elif method_name == "futures_query_real_deliver_list":
                # 查询接口-期货查询今日成交
                common_api_demo.futures_query_real_deliver_list()
            elif method_name == "futures_query_history_deliver_list":
                # 查询接口-期货查询历史成交
                common_api_demo.futures_query_history_deliver_list()
            elif method_name == "futures_query_product_info":
                # 查询接口-期货查询产品信息
                common_api_demo.futures_query_product_info()
            elif method_name == "futures_trade_subscribe":
                # 订阅接口-期货订阅交易推送消息
                common_api_demo.futures_trade_subscribe()
            elif method_name == "futures_trade_unsubscribe":
                # 订阅接口-取消订阅期货交易推送消息
                common_api_demo.futures_trade_unsubscribe()
            elif method_name == "stop":
                # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
                common_api_demo.stop()
                exit(1)
            else:
                print("接口名输入有误，请参考提示重新输入！")
    else:
        # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
        common_api_demo.stop()
        exit(1)
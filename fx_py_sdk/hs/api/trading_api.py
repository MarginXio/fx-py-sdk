# -*- coding: utf-8 -*-
from hs.api.constant import ClientType, ModelResult, StatusCode, EntrustType, SessionType
from hs.common.network_utils import get_mac_address
from hs.common.pb.common.constant.RequestMsgType_pb2 import TradeEntrustRequestMsgType, \
    TradeCancelEntrustRequestMsgType, TradeQueryHoldsListRequestMsgType, TradeQueryBuyAmountRequestMsgType, \
    TradeQuerySellAmountRequestMsgType, TradeQueryMarginFundInfoRequestMsgType, \
    TradeQueryRealEntrustListRequestMsgType, TradeQueryRealFundJourListRequestMsgType, \
    TradeQueryHistoryFundJourListRequestMsgType, TradeSubscribeRequestMsgType, TradeUnsubscribeRequestMsgType, \
    TradeQueryHistoryEntrustListRequestMsgType, TradeQueryRealDeliverListRequestMsgType, \
    TradeQueryHistoryDeliverListRequestMsgType, TradeChangeEntrustRequestMsgType, \
    TradeQueryBeforeAndAfterSupportRequestMsgType, \
    TradeQueryMaxAvailableAssetRequestMsgType, TradeQueryStockShortInfoRequestMsgType, \
    TradeQueryRealCondOrderListRequestMsgType, \
    TradeQueryHistoryCondOrderListRequestMsgType
from hs.common.pb.trade.request.TradeCancelEntrustRequest_pb2 import TradeCancelEntrustRequest
from hs.common.pb.trade.request.TradeChangeEntrustRequest_pb2 import TradeChangeEntrustRequest
from hs.common.pb.trade.request.TradeEntrustRequest_pb2 import TradeEntrustRequest
from hs.common.pb.trade.request.TradeQueryBeforeAndAfterSupportRequest_pb2 import TradeQueryBeforeAndAfterSupportRequest
from hs.common.pb.trade.request.TradeQueryBuyAmountRequest_pb2 import TradeQueryBuyAmountRequest
from hs.common.pb.trade.request.TradeQueryHistoryCondOrderListRequest_pb2 import TradeQueryHistoryCondOrderListRequest
from hs.common.pb.trade.request.TradeQueryHistoryDeliverListRequest_pb2 import TradeQueryHistoryDeliverListRequest
from hs.common.pb.trade.request.TradeQueryHistoryEntrustListRequest_pb2 import TradeQueryHistoryEntrustListRequest
from hs.common.pb.trade.request.TradeQueryHistoryFundJourListRequest_pb2 import TradeQueryHistoryFundJourListRequest
from hs.common.pb.trade.request.TradeQueryHoldsListRequest_pb2 import TradeQueryHoldsListRequest
from hs.common.pb.trade.request.TradeQueryMarginFundInfoRequest_pb2 import TradeQueryMarginFundInfoRequest
from hs.common.pb.trade.request.TradeQueryMaxAvailableAssetRequest_pb2 import TradeQueryMaxAvailableAssetRequest
from hs.common.pb.trade.request.TradeQueryRealCondOrderListRequest_pb2 import TradeQueryRealCondOrderListRequest
from hs.common.pb.trade.request.TradeQueryRealDeliverListRequest_pb2 import TradeQueryRealDeliverListRequest
from hs.common.pb.trade.request.TradeQueryRealEntrustListRequest_pb2 import TradeQueryRealEntrustListRequest
from hs.common.pb.trade.request.TradeQueryRealFundJourListRequest_pb2 import TradeQueryRealFundJourListRequest
from hs.common.pb.trade.request.TradeQuerySellAmountRequest_pb2 import TradeQuerySellAmountRequest
from hs.common.pb.trade.request.TradeQueryStockShortInfoRequest_pb2 import TradeQueryStockShortInfoRequest
from hs.common.protobuf_utils import parse_payload
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.token_client import TokenClient
from hs.common.trading_socket_client import TradingSocketClient


class TradingAPI(object):
    """
    开箱即用的交易API
    交易独立程序，建议用此API
    接入文档参考：https://quant-open.hstong.com/api-docs/
    """

    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 trading_passwd: str,
                 logging_filename: str = None):
        self._device_no = get_mac_address()
        # token client
        self._token_client = TokenClient(rsa_public_key=rsa_public_key,
                                         rsa_private_key=rsa_private_key,
                                         login_domain=login_domain,
                                         login_country_code=login_country_code,
                                         login_mobile=login_mobile,
                                         login_passwd=login_passwd,
                                         device_no=self._device_no,
                                         logging_filename=logging_filename,
                                         quote_stand_alone=False)

        self._socket_client = TradingSocketClient(rsa_public_key=rsa_public_key,
                                                  rsa_private_key=rsa_private_key,
                                                  login_domain=login_domain,
                                                  login_country_code=login_country_code,
                                                  login_mobile=login_mobile,
                                                  login_passwd=login_passwd,
                                                  trading_passwd=trading_passwd,
                                                  token_client=self._token_client,
                                                  device_no=self._device_no,
                                                  logging_filename=logging_filename)

    def is_alive(self):
        """检查StockClient是否正常连接状态"""
        return self._socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        host, port = self._socket_client.get_server(p_token)
        if host is None or port is None:
            raise Exception('Got trade server info error, host/port is None.')
        self._socket_client.restart(p_token, host, port)

    def add_notify_callback(self, callback):
        """
        增加消息推送回调函数
        """
        self._socket_client.handle_notify_for_ever(callback)

    def stop(self):
        """退出业务API上下文环境，停止StockClient"""
        self._socket_client.stop()

    def trade_subscribe(self) -> ModelResult:
        """
        订阅交易推送消息，目前只有订单成交推送。初始化交易链接会默认订阅订单成交推送。
        :return model_result model: 是否订阅成功 true-是 false-否
        """
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeSubscribeRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=None)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def trade_unsubscribe(self) -> ModelResult:
        """
        取消订阅交易推送消息
        :return model_result model: 是否取消订阅成功 true-是 false-否
        """
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeUnsubscribeRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=None)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def entrust(self, iceberg_display_size: str,
                session_type: str,
                exchange: str,
                exchange_type: str,
                entrust_bs: str,
                entrust_type: str,
                stock_code: str,
                entrust_amount: str,
                entrust_price: str,
                cond_track_type: str = "",
                cond_value: str = "",
                valid_days: str = "") -> ModelResult:
        """
        委托下单
        :param cond_track_type 跟踪类型 1百分比、2价差、3价格
        :param cond_value 触发条件值 价格/价差/百分比值
        :param valid_days 有效天数
        :param iceberg_display_size 冰山单披露数量
        :param session_type 盘前盘后交易  0否 1是 3只支持盘中 6美股只支持盘前盘后 7美股支持盘中及盘前盘后 8美股只支持盘前 9美股只支持盘后
        :param exchange 交易所
        :param exchange_type 交易类型，可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param entrust_bs  买卖方向 可能值：'1'买入、'2'卖出
        :param entrust_type 委托类型 可能值：港股：'0'竞价限价、'1'竞价、'2'增强限价盘、'3'限价盘、'4'特别限价盘、'6'暗盘。
                                          美股：'3'限价盘、'5'市价盘。
                                          A股：'3'限价盘。
                                          条件单：'31'-止盈限价单、'32'-止盈市价单(美股)、'33'-止损限价单、'34'-止损市价单(美股)、'35'-追踪止损限价单、'36'-追踪止损市价单(美股)
        :param stock_code 证券代码
        :param entrust_amount 委托数量
        :param entrust_price 委托价格
        :return model_result model: 委托单号。返回长度大于0的字符串: 委托成功; 返回空字符串: 委托失败
        """
        if len(session_type) == 0 and entrust_type in (EntrustType.COND_STOP_PROFIT_POINT, 
                                                     EntrustType.COND_STOP_PROFIT_MARKET, 
                                                     EntrustType.COND_STOP_LOSS_POINT,
                                                     EntrustType.COND_STOP_LOSS_MARKET,
                                                     EntrustType.COND_TRACK_STOP_LOSS_POINT,
                                                     EntrustType.COND_TRACK_STOP_LOSS_MARKET) :
            session_type = SessionType.COND_ORDER_DEFAULT
        payload = TradeEntrustRequest()
        payload.stockCode = stock_code
        payload.exchangeType = exchange_type
        payload.entrustAmount = str(entrust_amount)
        payload.entrustPrice = str(entrust_price)
        payload.entrustBs = entrust_bs
        payload.entrustType = entrust_type
        payload.clientType = ClientType.INTERNET
        payload.exchange = exchange
        payload.sessionType = session_type
        payload.iceBergDisplaySize = iceberg_display_size
        payload.validDays = valid_days
        payload.condValue = cond_value
        payload.condTrackType = cond_track_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeEntrustRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: str
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def change_entrust(self, exchange_type: str,
                       entrust_id: str,
                       stock_code: str,
                       entrust_amount: str,
                       entrust_price: str,
                       entrust_type: str = "",
                       session_type: str = "",
                       cond_value: str = "",
                       valid_days: str = "",
                       cond_track_type: str = "") -> ModelResult:
        """
        改单
        :param cond_track_type 跟踪类型 1百分比、2价差、3价格
        :param cond_value 触发条件值 价格/价差/百分比值
        :param valid_days 有效天数
        :param session_type 盘前盘后交易 3只支持盘中 6美股只支持盘前盘后 7美股支持盘中及盘前盘后
        :param entrust_type 委托类型
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param entrust_id 要改单的原委托编号
        :param stock_code 证券代码
        :param entrust_amount 修改委托数量
        :param entrust_price 修改委托价格
        :return model_result model: 委托单号。返回长度大于0的字符串: 委托成功; 返回空字符串: 委托失败
        """
        if entrust_id is None or len(entrust_id) < 1:
            return ModelResult(False, "", "", "")
        payload = TradeChangeEntrustRequest()
        payload.exchangeType = exchange_type
        payload.entrustAmount = str(entrust_amount)
        payload.entrustPrice = str(entrust_price)
        payload.entrustId = entrust_id
        payload.stockCode = stock_code
        payload.entrustType = entrust_type
        payload.sessionType = session_type
        payload.validDays = valid_days
        payload.condValue = cond_value
        payload.condTrackType = cond_track_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeChangeEntrustRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: str
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def cancel_entrust(self, exchange_type: str,
                       entrust_id: str,
                       stock_code: str,
                       entrust_amount: str,
                       entrust_price: str,
                       entrust_type: str = "", ) -> ModelResult:
        """
        撤单
        :param entrust_type 委托类型
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param entrust_id 要撤单的原委托编号
        :param stock_code 证券代码
        :param entrust_amount 委托数量、必须传原委托的委托数量
        :param entrust_price 委托价格
        :return model_result model: 委托单号。返回长度大于0的字符串: 委托成功; 返回空字符串: 委托失败
        """
        if entrust_id is None or len(entrust_id) < 1:
            return ModelResult(False, "", "", "")
        payload = TradeCancelEntrustRequest()
        payload.exchangeType = exchange_type
        payload.entrustAmount = str(entrust_amount)
        payload.entrustPrice = str(entrust_price)
        payload.entrustId = entrust_id
        payload.stockCode = stock_code
        payload.entrustType = entrust_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeCancelEntrustRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: str
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_holds_list(self, exchange_type: str) -> ModelResult:
        """
        查询持仓股票列表
        :param exchange_type 交易类型(非必填) 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :return model_result model: 持仓列表：[HoldsVo]
        """
        payload = TradeQueryHoldsListRequest()
        payload.exchangeType = exchange_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHoldsListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.holdsList)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_buy_amount(self, exchange_type: str, stock_code: str, entrust_price: str) -> ModelResult:
        """
        获取最大可买数量
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param stock_code 证券代码
        :param entrust_price 委托价格
        :return model_result model: 最大可买数量
        """
        payload = TradeQueryBuyAmountRequest()
        payload.stockCode = stock_code
        payload.entrustPrice = str(entrust_price)
        payload.exchangeType = exchange_type
        payload.clientType = ClientType.INTERNET
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryBuyAmountRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: int
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_sell_amount(self, exchange_type: str, stock_code: str) -> ModelResult:
        """
        获取最大可卖数量
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param stock_code 证券代码
        :return model_result model: 最大可卖数量
        """
        payload = TradeQuerySellAmountRequest()
        payload.stockCode = stock_code
        payload.exchangeType = exchange_type
        payload.clientType = ClientType.INTERNET
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=TradeQuerySellAmountRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: int
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_margin_fund_info(self, exchange_type: str) -> ModelResult:
        """
        查询客户资金信息
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :return model_result model: 客户资金信息
        """
        payload = TradeQueryMarginFundInfoRequest()
        payload.exchangeType = exchange_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryMarginFundInfoRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", None)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: TradeQueryMarginFundInfoResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_real_entrust_list(self, exchange_type: str,
                                query_count: int = 20,
                                query_param_str: str = "0",
                                entrust_ids: list = []) -> ModelResult:
        """
        查询客户当日委托信息
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :param model_result model: 订单实体对象列表[OrderVo]
        """
        payload = TradeQueryRealEntrustListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.entrustId.extend(entrust_ids)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryRealEntrustListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_history_entrust_list(self, exchange_type: str,
                                   query_count: int,
                                   query_param_str: str,
                                   start_date: str,
                                   end_date: str) -> ModelResult:
        """
        查询客户历史委托信息
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :param start_date 起始日期 格式为：yyyyMMdd
        :param end_date 结束日期 格式为：yyyyMMdd
        :param model_result model: 订单实体对象列表[OrderVo]
        """
        payload = TradeQueryHistoryEntrustListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryHistoryEntrustListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_real_deliver_list(self, exchange_type: str,
                                query_count: int = 20,
                                query_param_str: str = "0") -> ModelResult:
        """
        查询客户当日成交信息
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :param model_result model: 订单实体对象列表[OrderVo]
        """
        payload = TradeQueryRealDeliverListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryRealDeliverListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_history_deliver_list(self, exchange_type: str,
                                   query_count: int,
                                   query_param_str: str,
                                   start_date: str,
                                   end_date: str) -> ModelResult:
        """
        查询客户历史成交信息
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :param start_date 起始日期 格式为：yyyyMMdd
        :param end_date 结束日期 格式为：yyyyMMdd
        :param model_result model: 订单实体对象列表[OrderVo]
        """
        payload = TradeQueryHistoryDeliverListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryHistoryDeliverListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_real_fund_jour_list(self, exchange_type: str,
                                  query_count: int = 20,
                                  query_param_str: str = "0") -> ModelResult:
        """
        查询客户当日资金流水列表
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :return model_result model: 资金流水实体对象列表[FundJourVo]
        """
        payload = TradeQueryRealFundJourListRequest()
        payload.exchangeType = exchange_type
        payload.queryParamStr = str(query_param_str)
        payload.queryCount = int(query_count)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryRealFundJourListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_history_fund_jour_list(self, exchange_type: str,
                                     query_count: int,
                                     query_param_str: str,
                                     start_date: str,
                                     end_date: str) -> ModelResult:
        """
        查询客户历史资金流水列表
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param query_count 每页返回数量 默认20（限制小于100）
        :param query_param_str 游标 初始值为0 开始
        :param start_date 起始日期 格式为：yyyyMMdd
        :param end_date 结束日期 格式为：yyyyMMdd
        :return model_result model: 资金流水实体对象列表[FundJourVo]
        """
        payload = TradeQueryHistoryFundJourListRequest()
        payload.exchangeType = exchange_type
        payload.queryParamStr = str(query_param_str)
        payload.queryCount = int(query_count)
        payload.startDate = int(start_date)
        payload.endDate = int(end_date)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryHistoryFundJourListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_before_and_after_support(self, stock_code: str, exchange_type: str) -> ModelResult:
        """
        查询是否支持盘前盘后交易
        :param stock_code 证券代码
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :return model_result model: "1": 是, "0": 否
        """
        payload = TradeQueryBeforeAndAfterSupportRequest()
        payload.stockCode = stock_code
        payload.exchangeType = exchange_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryBeforeAndAfterSupportRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: int
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_max_available_asset(self, exchange_type: str, stock_code: str, entrust_price: str, entrust_type: str):
        """
        Parameters
        ----------
        exchange_type: 'K'港股、'P'美股、'v'深股通、't'沪股通
        stock_code: 证券代码
        entrust_price: 委托价格
        entrust_type: 委托类型

        Returns
        -------
        model_result : 最大可用资产信息
        """
        payload = TradeQueryMaxAvailableAssetRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.entrustPrice = entrust_price
        payload.entrustType = entrust_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryMaxAvailableAssetRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", None)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_stock_short_info(self, exchange_type: str, stock_code: str):
        """
        Parameters
        ----------
        exchange_type: 'K'港股、'P'美股、'v'深股通、't'沪股通
        stock_code: 证券代码

        Returns
        -------
        model_result : 股票沽空信息
        """
        payload = TradeQueryStockShortInfoRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryStockShortInfoRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", None)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_real_cond_order_list(self, exchange_type: str,
                                   stock_code: str,
                                   page_no: int = 1,
                                   page_size: int = 20) -> ModelResult:
        """
        查询当日条件单列表
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param stock_code 股票代码
        :param page_no 页码，从1开始
        :param page_size 每页数量，限制小于100
        """
        payload = TradeQueryRealCondOrderListRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.pageNo = page_no
        payload.pageSize = page_size
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryRealCondOrderListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_history_cond_order_list(self, start_time: str,
                                      end_time: str,
                                      exchange_type: str,
                                      stock_code: str,
                                      page_no: int = 1,
                                      page_size: int = 20) -> ModelResult:
        """
        查询历史条件单列表
        :param start_time 查询开始时间 
        :param end_time 查询结束时间 
        :param exchange_type 交易类型 可能值：'K'港股、'P'美股、'v'深股通、't'泸股通
        :param stock_code 股票代码
        :param page_no 页码，从1开始
        :param page_size 每页数量，限制小于100
        """
        payload = TradeQueryHistoryCondOrderListRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.pageNo = page_no
        payload.pageSize = page_size
        payload.startTime = start_time
        payload.endTime = end_time
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TradeQueryHistoryCondOrderListRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    serial_no=self._socket_client._serial_no,
                    token=self._token_client.get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

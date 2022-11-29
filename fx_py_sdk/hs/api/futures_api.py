# -*- coding: utf-8 -*-
from hs.api.constant import ModelResult, StatusCode
from hs.api.trading_api import TradingAPI
from hs.common.pb.common.constant.RequestMsgType_pb2 import FuturesEntrustRequestMsgType, \
    FuturesModifyEntrustRequestMsgType, FuturesCancelEntrustRequestMsgType, \
    FuturesQueryFundInfoRequestMsgType, FuturesQueryMaxBuySellAmountRequestMsgType, \
    FuturesQueryRealEntrustListRequestMsgType, FuturesQueryHistoryEntrustListRequestMsgType, \
    FuturesQueryRealDeliverListRequestMsgType, FuturesQueryHistoryDeliverListRequestMsgType, \
    FuturesQueryProductInfoRequestMsgType, FuturesQueryHoldsListRequestMsgType
from hs.common.pb.trade.request.futures.FuturesCancelEntrustRequest_pb2 import FuturesCancelEntrustRequest
from hs.common.pb.trade.request.futures.FuturesEntrustRequest_pb2 import FuturesEntrustRequest
from hs.common.pb.trade.request.futures.FuturesModifyEntrustRequest_pb2 import FuturesModifyEntrustRequest
from hs.common.pb.trade.request.futures.FuturesQueryFundInfoRequest_pb2 import FuturesQueryFundInfoRequest
from hs.common.pb.trade.request.futures.FuturesQueryHistoryDeliverListRequest_pb2 import \
    FuturesQueryHistoryDeliverListRequest
from hs.common.pb.trade.request.futures.FuturesQueryHistoryEntrustListRequest_pb2 import \
    FuturesQueryHistoryEntrustListRequest
from hs.common.pb.trade.request.futures.FuturesQueryHoldsListRequest_pb2 import FuturesQueryHoldsListRequest
from hs.common.pb.trade.request.futures.FuturesQueryMaxBuySellAmountRequest_pb2 import \
    FuturesQueryMaxBuySellAmountRequest
from hs.common.pb.trade.request.futures.FuturesQueryProductInfoRequest_pb2 import FuturesQueryProductInfoRequest
from hs.common.pb.trade.request.futures.FuturesQueryRealDeliverListRequest_pb2 import FuturesQueryRealDeliverListRequest
from hs.common.pb.trade.request.futures.FuturesQueryRealEntrustListRequest_pb2 import FuturesQueryRealEntrustListRequest
from hs.common.protobuf_utils import parse_payload
from hs.common.request_msg_type_enum import RequestMsgTypeEnum


class FuturesAPI(TradingAPI):
    """
    开箱即用的期货交易API
    期货独立程序，建议用此API
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
        super().__init__(rsa_public_key=rsa_public_key,
                          rsa_private_key=rsa_private_key,
                          login_domain=login_domain,
                          login_country_code=login_country_code,
                          login_mobile=login_mobile,
                          login_passwd=login_passwd,
                          trading_passwd=trading_passwd,
                          logging_filename=logging_filename)

    def futures_entrust(self, stock_code: str,
                            entrust_type: str,
                            entrust_price: str,
                            entrust_amount: str,
                            entrust_bs: str,
                            valid_time_type: str,
                            valid_time: str,
                            order_options: str) -> ModelResult:
        """
        期货委托下单
        :param stock_code 代码
        :param entrust_type 交易所
        :param entrust_price 委托价格
        :param entrust_amount 委托数量
        :param entrust_bs  买卖方向 可能值：'1'买入、'2'卖出
        :param valid_time_type 生效类型[ 0 即日有效、1 成交并取消、2 全额或取消、3 到期日有效、4 指定日期有效]
        :param valid_time 当 valid_time_type==4 必填yyyyMMdd
        :param order_options 0:默认 1:T+1
        
        :return model_result model: 委托单号。返回长度大于0的字符串: 委托成功; 返回空字符串: 委托失败
        """
        payload = FuturesEntrustRequest()
        payload.stockCode = stock_code
        payload.entrustType = entrust_type
        payload.entrustPrice = str(entrust_price)
        payload.entrustAmount = str(entrust_amount)
        payload.entrustBs = entrust_bs
        payload.validTimeType = valid_time_type
        payload.validTime = valid_time
        payload.orderOptions = order_options
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesEntrustRequestMsgType,
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

    def futures_change_entrust(self, entrust_id: str,
                               stock_code: str,
                               entrust_price: str,
                               entrust_amount: str,
                               entrust_bs: str,
                               valid_time_type: str,
                               valid_time: str,
                               order_options: str) -> ModelResult:
        """
        期货改单
        :param entrust_id 委托ID
        :param stock_code 代码
        :param entrust_price 委托价格
        :param entrust_amount 委托数量
        :param entrust_bs  买卖方向 可能值：'1'买入、'2'卖出
        :param valid_time_type 生效类型[ 0 即日有效、1 成交并取消、2 全额或取消、3 到期日有效、4 指定日期有效]
        :param valid_time 当 valid_time_type==4 必填yyyyMMdd
        :param order_options 委托数量
        
        :return model_result model: 委托单号。返回长度大于0的字符串: 改单成功; 返回空字符串: 改单失败
        """
        payload = FuturesModifyEntrustRequest()
        payload.entrustId = entrust_id
        payload.stockCode = stock_code
        payload.entrustPrice = str(entrust_price)
        payload.entrustAmount = str(entrust_amount)
        payload.entrustBs = entrust_bs
        payload.validTimeType = valid_time_type
        payload.validTime = valid_time
        payload.orderOptions = order_options
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesModifyEntrustRequestMsgType,
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

    def futures_cancel_entrust(self, entrust_id: str,
                                    stock_code: str) -> ModelResult:
        """
        期货撤单
        :param entrust_id 委托ID
        :param stock_code 代码
        
        :return model_result model: 委托单号。返回长度大于0的字符串: 改单成功; 返回空字符串: 改单失败
        """
        payload = FuturesCancelEntrustRequest()
        payload.entrustId = entrust_id
        payload.stockCode = stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesCancelEntrustRequestMsgType,
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

    def futures_query_holds_list(self) -> ModelResult:
        """
        期货查询持仓
        :return model_result
        """
        payload = FuturesQueryHoldsListRequest()
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHoldsListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload) 
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_fund_info(self) -> ModelResult:
        """
        期货查询资金信息
        :return model_result
        """
        payload = FuturesQueryFundInfoRequest()
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryFundInfoRequestMsgType,
                                                                msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                serial_no=self._socket_client._serial_no,
                                                                token=self._token_client.get_token_from_cache(),
                                                                pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", None)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.fundInfo)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_max_buy_sell_amount(self, stock_code: str) -> ModelResult:
        """
        查询期货最大可买/卖
        :param stock_code 证券代码
        :return model_result
        """
        payload = FuturesQueryMaxBuySellAmountRequest()
        payload.stockCode = stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryMaxBuySellAmountRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_real_entrust_list(self) -> ModelResult:
        """
        期货查询今日委托
        :param model_result 
        """
        payload = FuturesQueryRealEntrustListRequest()
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryRealEntrustListRequestMsgType,
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

    def futures_query_history_entrust_list(self, page_no: int,
                                           page_size: int,
                                           start_date: str,
                                           end_date: str) -> ModelResult:
        """
        期货查询历史委托
        :param page_no 页码 默认1
        :param page_size 每页返回数量 默认20
        :param start_date 起始日期 格式为：yyyyMMdd
        :param end_date 结束日期 格式为：yyyyMMdd
        :param model_result model: 订单实体对象列表[OrderVo]
        """
        payload = FuturesQueryHistoryEntrustListRequest()
        payload.pageNo = int(page_no)
        payload.pageSize = int(page_size)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHistoryEntrustListRequestMsgType,
                                                                msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                serial_no=self._socket_client._serial_no,
                                                                token=self._token_client.get_token_from_cache(),
                                                                pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_real_deliver_list(self) -> ModelResult:
        """
        期货查询今日成交
        :param model_result 
        """
        payload = FuturesQueryRealDeliverListRequest()
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryRealDeliverListRequestMsgType,
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

    def futures_query_history_deliver_list(self, page_no: int,
                                           page_size: int,
                                           start_date: str,
                                           end_date: str) -> ModelResult:
        """
        期货查询历史成交
        :param page_no 页码 默认1
        :param page_size 每页返回数量 默认20
        :param start_date 起始日期 格式为：yyyyMMdd
        :param end_date 结束日期 格式为：yyyyMMdd
        :param model_result
        """
        payload = FuturesQueryHistoryDeliverListRequest()
        payload.pageNo = int(page_no)
        payload.pageSize = int(page_size)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHistoryDeliverListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_product_info(self, stock_code_list: list) -> ModelResult:
        """
        期货查询产品信息
        :param stock_code_list 期货代码列表
        :return model_result
        """
        payload = FuturesQueryProductInfoRequest()
        for stock_code in stock_code_list:
            payload.stockCode.append(stock_code)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryProductInfoRequestMsgType,
                                                                msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                serial_no=self._socket_client._serial_no,
                                                                token=self._token_client.get_token_from_cache(),
                                                                pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.productInfoVos)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_trade_subscribe(self) -> ModelResult:
        """
        订阅期货交易推送消息
        :return model_result model: 是否订阅成功 true-是 false-否
        """

    def futures_trade_unsubscribe(self) -> ModelResult:
        """
        取消订阅期货交易推送消息
        :return model_result model: 是否取消订阅成功 true-是 false-否
        """

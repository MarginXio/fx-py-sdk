# -*- coding: utf-8 -*-
from hs.api.constant import ClientType
from hs.api.constant import ModelResult, StatusCode
from hs.api.constant import SecurityParam, MktTmType
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
    FuturesEntrustRequestMsgType, \
    FuturesModifyEntrustRequestMsgType, FuturesCancelEntrustRequestMsgType, \
    FuturesQueryFundInfoRequestMsgType, FuturesQueryMaxBuySellAmountRequestMsgType, \
    FuturesQueryRealEntrustListRequestMsgType, FuturesQueryHistoryEntrustListRequestMsgType, \
    FuturesQueryRealDeliverListRequestMsgType, FuturesQueryHistoryDeliverListRequestMsgType, \
    FuturesQueryProductInfoRequestMsgType, FuturesQueryHoldsListRequestMsgType, \
    TradeQueryHistoryCondOrderListRequestMsgType, TradeQueryRealCondOrderListRequestMsgType, \
    HQBasicQotRequestMsgType, HQBrokerRequestMsgType, \
    HQOrderBookRequestMsgType, HQTickerRequestMsgType, HQKLRequestMsgType, HQTimeShareRequestMsgType
from hs.common.pb.hq.dto.Security_pb2 import Security
from hs.common.pb.hq.request.GetBasicQotRequest_pb2 import BasicQotRequest
from hs.common.pb.hq.request.GetBrokerRequest_pb2 import BrokerRequest
from hs.common.pb.hq.request.GetKLRequest_pb2 import KLRequest
from hs.common.pb.hq.request.GetOrderBookRequest_pb2 import OrderBookRequest
from hs.common.pb.hq.request.GetTickerRequest_pb2 import TickerRequest
from hs.common.pb.hq.request.GetTimeShareRequest_pb2 import TimeShareRequest
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
from hs.common.quote_socket_client import QuoteSocketClient
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.token_client import TokenClient
from hs.common.trading_socket_client import TradingSocketClient


class CommonAPI(object):
    """
    ?????????????????????API????????????????????????????????????????????????
    ??????????????????????????????????????????????????????????????????API
    ?????????????????????https://quant-open.hstong.com/api-docs/
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
                                         logging_filename=logging_filename,
                                         device_no=self._device_no,
                                         quote_stand_alone=False)
        # trading_client
        self._trading_socket_client = TradingSocketClient(rsa_public_key=rsa_public_key,
                                                          rsa_private_key=rsa_private_key,
                                                          login_domain=login_domain,
                                                          login_country_code=login_country_code,
                                                          login_mobile=login_mobile,
                                                          login_passwd=login_passwd,
                                                          trading_passwd=trading_passwd,
                                                          token_client=self._token_client,
                                                          device_no=self._device_no,
                                                          logging_filename=logging_filename)
        # quote_client
        self._quote_socket_client = QuoteSocketClient(rsa_public_key=rsa_public_key,
                                                      rsa_private_key=rsa_private_key,
                                                      login_domain=login_domain,
                                                      login_country_code=login_country_code,
                                                      login_mobile=login_mobile,
                                                      login_passwd=login_passwd,
                                                      trading_passwd=trading_passwd,
                                                      use_lv2=True,
                                                      token_client=self._token_client,
                                                      device_no=self._device_no,
                                                      logging_filename=logging_filename)

    def is_alive(self):
        """
        ??????StockClient????????????????????????
        ??????????????????????????????????????????????????????
        """
        return self._trading_socket_client.is_alive() and self._quote_socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token()

    def start(self, p_token):
        """????????????API????????????????????????StockClient"""
        # ????????????Client
        t_host, t_port = self._trading_socket_client.get_server(p_token)
        if t_host is None or t_port is None:
            raise Exception('Got trade server info error, host/port is None.')
        self._trading_socket_client.restart(p_token, t_host, t_port)

        # ????????????Client
        h_host, h_port = self._quote_socket_client.get_server(p_token)
        if h_host is None or h_port is None:
            raise Exception('Got hq server info error, host/port is None.')
        self._quote_socket_client.restart(p_token, h_host, h_port)

    def add_notify_callback(self, callback):
        """??????????????????????????????"""
        self._trading_socket_client.handle_notify_for_ever(callback)
        self._quote_socket_client.handle_notify_for_ever(callback)

    def stop(self):
        """????????????API????????????????????????StockClient"""
        self._trading_socket_client.stop()
        self._quote_socket_client.stop()

    ##########################################      Trading API      ##################################################
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
        ????????????
        :param cond_track_type ???????????? 1????????????2?????????3??????
        :param cond_value ??????????????? ??????/??????/????????????
        :param valid_days ????????????
        :param iceberg_display_size ?????????????????????
        :param session_type ??????????????????  0??? 1??? 3??????????????? 6??????????????????????????? 7????????????????????????????????? 8????????????????????? 9?????????????????????
        :param exchange ?????????
        :param exchange_type ???????????????????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param entrust_bs  ???????????? ????????????'1'?????????'2'??????
        :param entrust_type ???????????? ?????????????????????'0'???????????????'1'?????????'2'??????????????????'3'????????????'4'??????????????????'6'?????????
                                          ?????????'3'????????????'5'????????????
                                          A??????'3'????????????
                                          ????????????'31'-??????????????????'32'-???????????????(??????)???'33'-??????????????????'34'-???????????????(??????)???'35'-????????????????????????'36'-?????????????????????(??????)
        :param stock_code ????????????
        :param entrust_amount ????????????
        :param entrust_price ????????????
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
        """
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
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeEntrustRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????
        :param cond_track_type ???????????? 1????????????2?????????3??????
        :param cond_value ??????????????? ??????/??????/????????????
        :param valid_days ????????????
        :param session_type ?????????????????? 3??????????????? 6??????????????????????????? 7?????????????????????????????????
        :param entrust_type ????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param entrust_id ???????????????????????????
        :param stock_code ????????????
        :param entrust_amount ??????????????????
        :param entrust_price ??????????????????
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
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
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeChangeEntrustRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????
        :param entrust_type ????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param entrust_id ???????????????????????????
        :param stock_code ????????????
        :param entrust_amount ????????????????????????????????????????????????
        :param entrust_price ????????????
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
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
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeCancelEntrustRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: str
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_holds_list(self, exchange_type: str) -> ModelResult:
        """
        ????????????????????????
        :param exchange_type ????????????(?????????) ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :return model_result model: ???????????????[HoldsVo]
        """
        payload = TradeQueryHoldsListRequest()
        payload.exchangeType = exchange_type
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHoldsListRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.holdsList)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_buy_amount(self, exchange_type: str, stock_code: str, entrust_price: str) -> ModelResult:
        """
        ????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param stock_code ????????????
        :param entrust_price ????????????
        :return model_result model: ??????????????????
        """
        payload = TradeQueryBuyAmountRequest()
        payload.stockCode = stock_code
        payload.entrustPrice = str(entrust_price)
        payload.exchangeType = exchange_type
        payload.clientType = ClientType.INTERNET
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryBuyAmountRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: int
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_sell_amount(self, exchange_type: str, stock_code: str) -> ModelResult:
        """
        ????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param stock_code ????????????
        :return model_result model: ??????????????????
        """
        payload = TradeQuerySellAmountRequest()
        payload.stockCode = stock_code
        payload.exchangeType = exchange_type
        payload.clientType = ClientType.INTERNET
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQuerySellAmountRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: int
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_margin_fund_info(self, exchange_type: str) -> ModelResult:
        """
        ????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :return model_result model: ??????????????????
        """
        payload = TradeQueryMarginFundInfoRequest()
        payload.exchangeType = exchange_type
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryMarginFundInfoRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :param model_result model: ????????????????????????[OrderVo]
        """
        payload = TradeQueryRealEntrustListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.entrustId.extend(entrust_ids)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryRealEntrustListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :param start_date ???????????? ????????????yyyyMMdd
        :param end_date ???????????? ????????????yyyyMMdd
        :param model_result model: ????????????????????????[OrderVo]
        """
        payload = TradeQueryHistoryEntrustListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHistoryEntrustListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :param model_result model: ????????????????????????[OrderVo]
        """
        payload = TradeQueryRealDeliverListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryRealDeliverListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ??????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :param start_date ???????????? ????????????yyyyMMdd
        :param end_date ???????????? ????????????yyyyMMdd
        :param model_result model: ????????????????????????[OrderVo]
        """
        payload = TradeQueryHistoryDeliverListRequest()
        payload.exchangeType = exchange_type
        payload.queryCount = int(query_count)
        payload.queryParamStr = str(query_param_str)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHistoryDeliverListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :return model_result model: ??????????????????????????????[FundJourVo]
        """
        payload = TradeQueryRealFundJourListRequest()
        payload.exchangeType = exchange_type
        payload.queryParamStr = str(query_param_str)
        payload.queryCount = int(query_count)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryRealFundJourListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param query_count ?????????????????? ??????20???????????????100???
        :param query_param_str ?????? ????????????0 ??????
        :param start_date ???????????? ????????????yyyyMMdd
        :param end_date ???????????? ????????????yyyyMMdd
        :return model_result model: ??????????????????????????????[FundJourVo]
        """
        payload = TradeQueryHistoryFundJourListRequest()
        payload.exchangeType = exchange_type
        payload.queryParamStr = str(query_param_str)
        payload.queryCount = int(query_count)
        payload.startDate = int(start_date)
        payload.endDate = int(end_date)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHistoryFundJourListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def trade_subscribe(self) -> ModelResult:
        """
        ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        :return model_result model: ?????????????????? true-??? false-???
        """
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeSubscribeRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=None)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def trade_unsubscribe(self) -> ModelResult:
        """
        ??????????????????????????????
        :return model_result model: ???????????????????????? true-??? false-???
        """
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeUnsubscribeRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=None)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_before_and_after_support(self, stock_code: str, exchange_type: str) -> ModelResult:
        """
        ????????????????????????????????????
        :param stock_code ????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :return model_result model: "1": ???, "0": ???
        """
        payload = TradeQueryBeforeAndAfterSupportRequest()
        payload.stockCode = stock_code
        payload.exchangeType = exchange_type
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryBeforeAndAfterSupportRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        exchange_type: 'K'?????????'P'?????????'v'????????????'t'?????????
        stock_code: ????????????
        entrust_price: ????????????
        entrust_type: ????????????

        Returns
        -------
        model_result : ????????????????????????
        """
        payload = TradeQueryMaxAvailableAssetRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.entrustPrice = entrust_price
        payload.entrustType = entrust_type
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryMaxAvailableAssetRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        exchange_type: 'K'?????????'P'?????????'v'????????????'t'?????????
        stock_code: ????????????

        Returns
        -------
        model_result : ??????????????????
        """
        payload = TradeQueryStockShortInfoRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryStockShortInfoRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ???????????????????????????
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param stock_code ????????????
        :param page_no ????????????1??????
        :param page_size ???????????????????????????100
        """
        payload = TradeQueryRealCondOrderListRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.pageNo = page_no
        payload.pageSize = page_size
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryRealCondOrderListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ???????????????????????????
        :param start_time ?????????????????? 
        :param end_time ?????????????????? 
        :param exchange_type ???????????? ????????????'K'?????????'P'?????????'v'????????????'t'?????????
        :param stock_code ????????????
        :param page_no ????????????1??????
        :param page_size ???????????????????????????100
        """
        payload = TradeQueryHistoryCondOrderListRequest()
        payload.exchangeType = exchange_type
        payload.stockCode = stock_code
        payload.pageNo = page_no
        payload.pageSize = page_size
        payload.startTime = start_time
        payload.endTime = end_time
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=TradeQueryHistoryCondOrderListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    ##########################################      Quote API    ##################################################
    def query_hq_basic_qot(self, security_list: list) -> ModelResult:
        """
        ??????????????????????????????
        :param security_list list[SecurityParam] ?????? ????????????????????????
        :return model_result model: ?????????????????????[BasicQot]
        """
        pb_security_list = []
        for security_param in security_list:
            pb_security = Security()
            pb_security.dataType = security_param.data_type
            pb_security.code = security_param.stock_code
            pb_security_list.append(pb_security)
        # build pb payload
        payload = BasicQotRequest()
        for pb_security in pb_security_list:
            payload.security.append(pb_security)
        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQBasicQotRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.basicQot)  # model type: List[BasicQot]
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_broker(self, security_param: SecurityParam) -> ModelResult:
        """
        ????????????????????????
        :param security_param ????????????????????????
        :return model_result model: ?????????????????? BrokerResponse
        """
        # build pb payload
        payload = BrokerRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQBrokerRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: BrokerResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_order_book(self, security_param: SecurityParam, mkt_tm_type: int = MktTmType.MID_SESSION,
                         depth_book_type=None) -> ModelResult:
        """
        ???????????????
        :param security_param ????????????????????????
        :param mkt_tm_type ?????????????????????????????????-1 ?????????1 ?????????-2?????????????????????3??????????????????
        :param depth_book_type ????????????
        :return model_result model: ??????????????? OrderBookResponse
        """
        # build pb payload
        payload = OrderBookRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        payload.mktTmType = mkt_tm_type
        if depth_book_type is not None:
            payload.depthBookType = depth_book_type

        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQOrderBookRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: BrokerResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_ticker(self, security_param: SecurityParam, limit: int) -> ModelResult:
        """
        ????????????????????????????????????
        :param security_param ????????????????????????
        :param limit ?????????????????????????????????????????????????????????????????????,????????????1000???
        :return model_result model: ???????????? TickerResponse
        """
        # build pb payload
        payload = TickerRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        payload.limit = limit
        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQTickerRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: BrokerResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_kline(self, security_param: SecurityParam,
                       start_date: str,
                       direction: int,
                       ex_right_flag: int,
                       cyc_type: int,
                       limit: int) -> ModelResult:
        """
        ??????K?????????
        :param security_param ????????????????????????
        :param start_date ???????????? ????????????yyyyMMdd
        :param direction ???????????? ??????????????????Direction
        :param ex_right_flag ???????????? ??????????????????ExRightFlag
        :param cyc_type K????????? ??????????????????CycType
        :param limit ??????k???????????????
        :return model_result model: K????????? KLResponse
        """
        # build pb payload
        payload = KLRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        payload.startDate = int(start_date)
        payload.direction = direction
        payload.exRightFlag = ex_right_flag
        payload.cycType = cyc_type
        payload.limit = limit
        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQKLRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: KLResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_time_share(self, security_param: SecurityParam) -> ModelResult:
        """
        ??????????????????
        :param security_param ????????????????????????
        :return model_result model: ???????????? TimeShareResponse
        """
        # build pb payload
        payload = TimeShareRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        with self._quote_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._quote_socket_client.build_request_bytes_then_send(request_msg_type=HQTimeShareRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._quote_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._quote_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: TimeShareResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def hq_subscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        ??????????????????
        :param topic_id ??????/???????????????????????????TopicId ??????????????????HQSubscribeTopicId
        :param security_list list[SecurityParam] ?????? ????????????????????????
        :return model_result model: ?????????????????? true-??? false-???
        """
        with self._quote_socket_client:
            return self._quote_socket_client.hq_subscribe(topic_id=topic_id, security_list=security_list)

    def hq_unsubscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        ????????????????????????
        :param topic_id ??????/???????????????????????????TopicId ??????????????????HQSubscribeTopicId
        :param security_list list[SecurityParam] ?????? ????????????????????????
        :return model_result model: ???????????????????????? true-??? false-???
        """
        with self._quote_socket_client:
            return self._quote_socket_client.hq_unsubscribe(topic_id=topic_id, security_list=security_list)

    ########################################## Futures API ##################################################
    def futures_entrust(self, stock_code: str,
                        entrust_type: str,
                        entrust_price: str,
                        entrust_amount: str,
                        entrust_bs: str,
                        valid_time_type: str,
                        valid_time: str,
                        order_options: str) -> ModelResult:
        """
        ??????????????????
        :param stock_code ??????
        :param entrust_type ?????????
        :param entrust_price ????????????
        :param entrust_amount ????????????
        :param entrust_bs  ???????????? ????????????'1'?????????'2'??????
        :param valid_time_type ????????????[ 0 ???????????????1 ??????????????????2 ??????????????????3 ??????????????????4 ??????????????????]
        :param valid_time ??? valid_time_type==4 ??????yyyyMMdd
        :param order_options 0:?????? 1:T+1
        
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
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
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesEntrustRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????
        :param entrust_id ??????ID
        :param stock_code ??????
        :param entrust_price ????????????
        :param entrust_amount ????????????
        :param entrust_bs  ???????????? ????????????'1'?????????'2'??????
        :param valid_time_type ????????????[ 0 ???????????????1 ??????????????????2 ??????????????????3 ??????????????????4 ??????????????????]
        :param valid_time ??? valid_time_type==4 ??????yyyyMMdd
        :param order_options ????????????
        
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
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
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesModifyEntrustRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????
        :param entrust_id ??????ID
        :param stock_code ??????
        
        :return model_result model: ?????????????????????????????????0????????????: ????????????; ??????????????????: ????????????
        """
        payload = FuturesCancelEntrustRequest()
        payload.entrustId = entrust_id
        payload.stockCode = stock_code
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesCancelEntrustRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.data)  # model type: str
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_holds_list(self) -> ModelResult:
        """
        ??????????????????
        :return model_result
        """
        payload = FuturesQueryHoldsListRequest()
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHoldsListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_fund_info(self) -> ModelResult:
        """
        ????????????????????????
        :return model_result
        """
        payload = FuturesQueryFundInfoRequest()
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryFundInfoRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", None)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.fundInfo)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_max_buy_sell_amount(self, stock_code: str) -> ModelResult:
        """
        ????????????????????????/???
        :param stock_code ????????????
        :return model_result
        """
        payload = FuturesQueryMaxBuySellAmountRequest()
        payload.stockCode = stock_code
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryMaxBuySellAmountRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", 0)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_real_entrust_list(self) -> ModelResult:
        """
        ????????????????????????
        :param model_result 
        """
        payload = FuturesQueryRealEntrustListRequest()
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryRealEntrustListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????????????????
        :param page_no ?????? ??????1
        :param page_size ?????????????????? ??????20
        :param start_date ???????????? ????????????yyyyMMdd
        :param end_date ???????????? ????????????yyyyMMdd
        :param model_result model: ????????????????????????[OrderVo]
        """
        payload = FuturesQueryHistoryEntrustListRequest()
        payload.pageNo = int(page_no)
        payload.pageSize = int(page_size)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHistoryEntrustListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_real_deliver_list(self) -> ModelResult:
        """
        ????????????????????????
        :param model_result 
        """
        payload = FuturesQueryRealDeliverListRequest()
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryRealDeliverListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
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
        ????????????????????????
        :param page_no ?????? ??????1
        :param page_size ?????????????????? ??????20
        :param start_date ???????????? ????????????yyyyMMdd
        :param end_date ???????????? ????????????yyyyMMdd
        :param model_result
        """
        payload = FuturesQueryHistoryDeliverListRequest()
        payload.pageNo = int(page_no)
        payload.pageSize = int(page_size)
        payload.startDate = str(start_date)
        payload.endDate = str(end_date)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryHistoryDeliverListRequestMsgType,
                                                                        msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                        serial_no=self._trading_socket_client._serial_no,
                                                                        token=self._token_client.get_token_from_cache(),
                                                                        pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def futures_query_product_info(self, stock_code_list: list) -> ModelResult:
        """
        ????????????????????????
        :param stock_code_list ??????????????????
        :return model_result
        """
        payload = FuturesQueryProductInfoRequest()
        for stock_code in stock_code_list:
            payload.stockCode.append(stock_code)
        with self._trading_socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._trading_socket_client.build_request_bytes_then_send(request_msg_type=FuturesQueryProductInfoRequestMsgType,
                                                                          msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                          serial_no=self._trading_socket_client._serial_no,
                                                                          token=self._token_client.get_token_from_cache(),
                                                                          pb_payload=payload)
            pb_response = self._trading_socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", [])
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.productInfoVos)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

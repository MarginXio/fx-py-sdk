# -*- coding: utf-8 -*-
from hs.api.constant import ModelResult, StatusCode, SecurityParam, MktTmType
from hs.common.network_utils import get_mac_address
from hs.common.pb.common.constant.RequestMsgType_pb2 import HQBasicQotRequestMsgType, HQBrokerRequestMsgType, \
    HQOrderBookRequestMsgType, HQTickerRequestMsgType, HQKLRequestMsgType, HQTimeShareRequestMsgType
from hs.common.pb.hq.dto.Security_pb2 import Security
from hs.common.pb.hq.request.GetBasicQotRequest_pb2 import BasicQotRequest
from hs.common.pb.hq.request.GetBrokerRequest_pb2 import BrokerRequest
from hs.common.pb.hq.request.GetKLRequest_pb2 import KLRequest
from hs.common.pb.hq.request.GetOrderBookRequest_pb2 import OrderBookRequest
from hs.common.pb.hq.request.GetTickerRequest_pb2 import TickerRequest
from hs.common.pb.hq.request.GetTimeShareRequest_pb2 import TimeShareRequest
from hs.common.protobuf_utils import parse_payload
from hs.common.quote_socket_client import QuoteSocketClient
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.token_client import TokenClient


class QuoteAPI(object):
    """
    开箱即用的行情API
    行情独立程序，建议用此API
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
        self._token_client = TokenClient(rsa_public_key=rsa_public_key,
                                         rsa_private_key=rsa_private_key,
                                         login_domain=login_domain,
                                         login_country_code=login_country_code,
                                         login_mobile=login_mobile,
                                         login_passwd=login_passwd,
                                         device_no=self._device_no,
                                         logging_filename=logging_filename,
                                         quote_stand_alone=True)

        self._socket_client = QuoteSocketClient(rsa_public_key=rsa_public_key,
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
        self._basic_qot = None  # 订阅的最新基础行情数据对象

    def is_alive(self):
        """检查StockClient是否正常连接状态"""
        return self._socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        host, port = self._socket_client.get_server(p_token)
        if host is None or port is None:
            raise Exception('Got hq server info error, host/port is None.')
        self._socket_client.restart(p_token, host, port)

    def query_hq_basic_qot(self, security_list: list) -> ModelResult:
        """
        批量查询股票基础报价
        :param security_list list[SecurityParam] 必填 股票信息，可批量
        :return model_result model: 基本行情信息：[BasicQot]
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
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQBasicQotRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.basicQot)  # model type: List[BasicQot]
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_broker(self, security_param: SecurityParam) -> ModelResult:
        """
        查询买卖经纪摆盘
        :param security_param 股票信息的实体类
        :return model_result model: 买卖经纪信息 BrokerResponse
        """
        # build pb payload
        payload = BrokerRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQBrokerRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
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
        查询买卖档
        :param security_param 股票信息的实体类
        :param mkt_tm_type 交易时段。美股：盘前：-1 盘中：1 盘后：-2；港股可以设置3个中的任意值
        :param depth_book_type 深度摆盘
        :return model_result model: 买卖档信息 OrderBookResponse
        """
        # build pb payload
        payload = OrderBookRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        payload.mktTmType = mkt_tm_type
        if depth_book_type is not None:
            payload.depthBookType = depth_book_type

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQOrderBookRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: BrokerResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_ticker(self, security_param: SecurityParam, limit: int) -> ModelResult:
        """
        查询最近多少条的逐笔列表
        :param security_param 股票信息的实体类
        :param limit 返回的逐笔个数，实际返回数量不一定会返回这么多,最多返回1000个
        :return model_result model: 逐笔信息 TickerResponse
        """
        # build pb payload
        payload = TickerRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        payload.limit = limit
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQTickerRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
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
        查询K线数据
        :param security_param 股票信息的实体类
        :param start_date 起始日期 格式为：yyyyMMdd
        :param direction 查询方向 参考常量类：Direction
        :param ex_right_flag 复权类型 参考常量类：ExRightFlag
        :param cyc_type K线类型 参考常量类：CycType
        :param limit 查询k线数量限制
        :return model_result model: K线信息 KLResponse
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
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQKLRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: KLResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_hq_time_share(self, security_param: SecurityParam) -> ModelResult:
        """
        查询分时数据
        :param security_param 股票信息的实体类
        :return model_result model: 分时信息 TimeShareResponse
        """
        # build pb payload
        payload = TimeShareRequest()
        payload.security.dataType = security_param.data_type
        payload.security.code = security_param.stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=HQTimeShareRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  serial_no=self._socket_client._serial_no,
                                                                  token=self._token_client.get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", "")
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type: TimeShareResponse
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def hq_subscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        订阅行情推送
        :param topic_id 订阅/取消订阅行情推送的TopicId 参考常量类：HQSubscribeTopicId
        :param security_list list[SecurityParam] 必填 股票信息，可批量
        :return model_result model: 是否订阅成功 true-是 false-否
        """
        with self._socket_client:
            return self._socket_client.hq_subscribe(topic_id=topic_id, security_list=security_list)

    def hq_unsubscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        取消订阅行情推送
        :param topic_id 订阅/取消订阅行情推送的TopicId 参考常量类：HQSubscribeTopicId
        :param security_list list[SecurityParam] 必填 股票信息，可批量
        :return model_result model: 是否取消订阅成功 true-是 false-否
        """
        with self._socket_client:
            return self._socket_client.hq_unsubscribe(topic_id=topic_id, security_list=security_list)

    def add_notify_callback(self, callback):
        """
        增加消息推送回调函数
        """
        self._socket_client.handle_notify_for_ever(callback)

    def stop(self):
        """退出业务API上下文环境，停止StockClient"""
        self._socket_client.stop()

# -*- coding: utf-8 -*-
import struct
from hs.common import rsa_utils
from hs.common.aes_ecb import AESCipher
from hs.common.common_utils import get_logger
from hs.common.pb.common.init.InitConnectResp_pb2 import InitConnectResp
from hs.common.pb.common.msg.Notify_pb2 import PBNotify
from hs.common.pb.common.msg.Response_pb2 import PBResponse
from hs.common.pb.common.response.CommonBoolResponse_pb2 import CommonBoolResponse
from hs.common.pb.common.response.CommonIntResponse_pb2 import CommonIntResponse
from hs.common.pb.common.response.CommonStringResponse_pb2 import CommonStringResponse
from hs.common.pb.hq.notify.BasicQotNotify_pb2 import BasicQotNotify
from hs.common.pb.hq.notify.BrokerNotify_pb2 import BrokerNotify
from hs.common.pb.hq.notify.OrderBookFullNotify_pb2 import OrderBookFullNotify
from hs.common.pb.hq.notify.TickerNotify_pb2 import TickerNotify
from hs.common.pb.hq.response.BasicQotResponse_pb2 import BasicQotResponse
from hs.common.pb.hq.response.BrokerResponse_pb2 import BrokerResponse
from hs.common.pb.hq.response.KLResponse_pb2 import KLResponse
from hs.common.pb.hq.response.OrderBookResponse_pb2 import OrderBookResponse
from hs.common.pb.hq.response.TickerResponse_pb2 import TickerResponse
from hs.common.pb.hq.response.TimeShareResponse_pb2 import TimeShareResponse
from hs.common.pb.trade.notify.TradeStockDeliverNotify_pb2 import TradeStockDeliverNotify
from hs.common.pb.trade.response.StockQueryHoldsListResponse_pb2 import StockQueryHoldsListResponse
from hs.common.pb.trade.response.TradeQueryHistoryDeliverListResponse_pb2 import TradeQueryHistoryDeliverListResponse
from hs.common.pb.trade.response.TradeQueryHistoryEntrustListResponse_pb2 import TradeQueryHistoryEntrustListResponse
from hs.common.pb.trade.response.TradeQueryHistoryFundJourListResponse_pb2 import TradeQueryHistoryFundJourListResponse
from hs.common.pb.trade.response.TradeQueryMarginFundInfoResponse_pb2 import TradeQueryMarginFundInfoResponse
from hs.common.pb.trade.response.TradeQueryRealDeliverListResponse_pb2 import TradeQueryRealDeliverListResponse
from hs.common.pb.trade.response.TradeQueryRealEntrustListResponse_pb2 import TradeQueryRealEntrustListResponse
from hs.common.pb.trade.response.TradeQueryRealFundJourListResponse_pb2 import TradeQueryRealFundJourListResponse
from hs.common.pb.trade.response.futures.FuturesQueryHoldsListResponse_pb2 import FuturesQueryHoldsListResponse
from hs.common.pb.trade.response.futures.FuturesQueryFundInfoResponse_pb2 import FuturesQueryFundInfoResponse
from hs.common.pb.trade.response.futures.FuturesQueryBuySellAmountResponse_pb2 import FuturesQueryBuySellAmountResponse
from hs.common.pb.trade.response.futures.FuturesQueryRealEntrustListResponse_pb2 import FuturesQueryRealEntrustListResponse
from hs.common.pb.trade.response.futures.FuturesQueryHistoryEntrustListResponse_pb2 import FuturesQueryHistoryEntrustListResponse
from hs.common.pb.trade.response.futures.FuturesQueryRealDeliverListResponse_pb2 import FuturesQueryRealDeliverListResponse
from hs.common.pb.trade.response.futures.FuturesQueryHistoryDeliverListResponse_pb2 import FuturesQueryHistoryDeliverListResponse
from hs.common.pb.trade.response.futures.FuturesQueryProductInfoResponse_pb2 import FuturesQueryProductInfoResponse
from hs.common.pb.trade.response.TradeQueryMaxAvailableAssetResponse_pb2 import TradeQueryMaxAvailableAssetResponse
from hs.common.pb.trade.response.TradeQueryStockShortInfoResponse_pb2 import TradeQueryStockShortInfoResponse
from hs.common.pb.trade.response.TradeQueryRealCondOrderListResponse_pb2 import TradeQueryRealCondOrderListResponse
from hs.common.pb.trade.response.TradeQueryHistoryCondOrderListResponse_pb2 import TradeQueryHistoryCondOrderListResponse

from hs.common.request_msg_header import RequestMsgHeader
from hs.common.request_msg_type_enum import RequestMsgTypeEnum

logging = get_logger(__name__)

# 包头FORMAT
MESSAGE_HEADER_FMT = "<2s1h2B2I128sBQ"
"""
    #pragma pack(push, APIProtoHeader, 1)
    struct APIProtoHeader
    {
        u8_t szHeaderFlag[2];   //2s-[2字节] 包头起始标志，固定为：“HS”
        u8_t msgType[2];        //1h-[2字节] 消息类型0：心跳 1：请求 2：响应 3：推送
        u8_t protoFmtType;      //B-[1字节] 协议格式类型，0为Protobuf格式
        u8_t protoVer;          //B-[1字节] 协议版本，用于迭代兼容, 目前填0
        u32_t serialNo;         //I-[4字节] 包序列号，用于对应请求包和回包，要求递增
        u32_t bodyLen;          //I-[4字节] 包体长度
        u8_t bodySHA1[128];     //128s-[128字节] 包体原始数据(加密后)的SHA1哈希值
        u8_t compressAlgorithm; //B-[1字节] 压缩算法，0：不压缩
        u8_t reserved[8];       //Q-[8字节] 保留8字节扩展
    };
    #pragma pack(pop, APIProtoHeader)
"""
PB_NOTIFY_CLASS_LIST = [TradeStockDeliverNotify,  # 成交推送
                        BasicQotNotify,  # 行情推送
                        BrokerNotify,
                        OrderBookFullNotify,
                        TickerNotify]
PB_RESPONSE_CLASS_LIST = [InitConnectResp,
                          CommonBoolResponse,
                          CommonStringResponse,
                          CommonIntResponse,
                          StockQueryHoldsListResponse,  # trading response
                          TradeQueryMarginFundInfoResponse,
                          TradeQueryRealEntrustListResponse,
                          TradeQueryRealFundJourListResponse,
                          TradeQueryHistoryFundJourListResponse,
                          TradeQueryHistoryEntrustListResponse,
                          TradeQueryRealDeliverListResponse,
                          TradeQueryHistoryDeliverListResponse,
                          BasicQotResponse,  # quote response
                          BrokerResponse,
                          OrderBookResponse,
                          TickerResponse,
                          KLResponse,
                          TimeShareResponse,
                          FuturesQueryHoldsListResponse,   # futures response
                          FuturesQueryFundInfoResponse,
                          FuturesQueryBuySellAmountResponse,
                          FuturesQueryRealEntrustListResponse,
                          FuturesQueryHistoryEntrustListResponse,
                          FuturesQueryRealDeliverListResponse,
                          FuturesQueryHistoryDeliverListResponse,
                          FuturesQueryProductInfoResponse,
                          TradeQueryMaxAvailableAssetResponse,
                          TradeQueryStockShortInfoResponse,
                          TradeQueryRealCondOrderListResponse,
                          TradeQueryHistoryCondOrderListResponse]


def pack_request(request_msg_header: RequestMsgHeader, encrypt_payload: str) -> bytes:
    if type(encrypt_payload) is not bytes:
       encrypt_payload = bytes(encrypt_payload, 'utf-8')
    request_msg_header.body_len = len(encrypt_payload)
    logging.debug("pack_request, request_msg_header.body_len=" + str(request_msg_header.body_len))
    return struct.pack(MESSAGE_HEADER_FMT + "%ds" % request_msg_header.body_len,
                       bytes(request_msg_header.sz_header_flag, "utf-8"),
                       request_msg_header.msg_type,
                       request_msg_header.proto_fmt_type,
                       request_msg_header.proto_ver,
                       request_msg_header.serial_no,
                       request_msg_header.body_len,
                       request_msg_header.body_sha1,
                       request_msg_header.compress_algorithm,
                       request_msg_header.reserved,
                       encrypt_payload)


def unpack_response(response: bytes, rsa_public_key: str, rsa_private_key: str, encrypt_secret_key: str):
    pack_size = struct.calcsize(MESSAGE_HEADER_FMT)
    logging.debug(f"unpack_response->len(response)：{len(response)}, header pack_size：{pack_size}，response：{response}")
    unpack_msg = struct.unpack(MESSAGE_HEADER_FMT+"%ds" % (len(response)-pack_size), response)
    logging.debug(f"unpack_response->header unpack_msg：{unpack_msg}")
    request_msg_header = RequestMsgHeader(sz_header_flag=unpack_msg[0].decode("utf-8"),
                                         msg_type=unpack_msg[1],
                                         proto_fmt_type=unpack_msg[2],
                                         proto_ver=unpack_msg[3],
                                         serial_no=unpack_msg[4],
                                         body_len=unpack_msg[5],
                                         body_sha1=unpack_msg[6],
                                         compress_algorithm=unpack_msg[7],
                                         reserved=unpack_msg[8])
    # 私钥解密body
    decrypt_body_bytes = unpack_msg[9]
    if request_msg_header.serial_no == 0:
        encrypt_secret_key = rsa_private_key
        if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value:
            # Socket登录初始化RSA
            decrypt_body_bytes = rsa_utils.decrypt_data(unpack_msg[9], encrypt_secret_key)
    else:
        # 业务请求AES
        if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
            decrypt_body_bytes = AESCipher(encrypt_secret_key).decrypt(unpack_msg[9])
    pb_response = PBNotify() if (request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value) else PBResponse()
    # 公钥验签
    if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
            or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value \
            or request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
        if rsa_utils.rsa_verify_sign(decrypt_body_bytes, request_msg_header.body_sha1, rsa_private_key):
            pb_response.ParseFromString(decrypt_body_bytes)
            if request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
                logging.debug(f"验签通过，notifyMsgType：{pb_response.notifyMsgType}，")
            else:
                logging.debug(f"验签通过，response消息：{pb_response.responseMsg}，")
        else:
            pb_response.ParseFromString(decrypt_body_bytes)
            if request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
                logging.debug(f"验签后的notifyMsgType：{pb_response.notifyMsgType}")
            else:
                logging.debug(f"验签后的response消息：{pb_response.responseMsg}")
    else:
        logging.debug("验签通过[免验]")
    logging.debug(f"unpack_response->response：{pb_response}")
    payload = parse_payload(pb_response)
    return request_msg_header, pb_response, payload


def parse_payload(pb_response):
    """解析any类型的payload"""
    if pb_response is None:
        return None
    payload = None
    payload_any = pb_response.payload
    if pb_response.DESCRIPTOR.name == PBNotify.DESCRIPTOR.name:
        for pb_class in PB_NOTIFY_CLASS_LIST:
            if payload_any.Is(pb_class.DESCRIPTOR):
                pb_class_response = pb_class()
                pb_response.payload.Unpack(pb_class_response)
                payload = pb_class_response
                logging.debug(f"parse_payload->{pb_class_response.DESCRIPTOR.name}：{payload}")
                break
    else:
        for pb_class in PB_RESPONSE_CLASS_LIST:
            if payload_any.Is(pb_class.DESCRIPTOR):
                pb_class_response = pb_class()
                pb_response.payload.Unpack(pb_class_response)
                payload = pb_class_response
                logging.debug(f"parse_payload->{pb_class_response.DESCRIPTOR.name}：{payload}")
                break
    return payload


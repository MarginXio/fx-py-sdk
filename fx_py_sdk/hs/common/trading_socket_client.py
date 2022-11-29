# -*- coding: utf-8 -*-
import queue
import threading

from hs.api.constant import ServerKey
from hs.common.common_utils import get_info_logger
from hs.common.pb.common.constant.RequestMsgType_pb2 import TradeKeepLoginRequestMsgType
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.socket_client import SocketClient
from hs.common.token_client import TokenClient

logging_name: str = __name__


class TradingSocketClient(SocketClient):
    """交易接口Socket Client"""
    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 trading_passwd: str,
                 token_client: TokenClient,
                 device_no: str,
                 logging_filename):
        super().__init__(rsa_public_key,
                         rsa_private_key,
                         login_domain,
                         login_country_code,
                         login_mobile,
                         login_passwd,
                         trading_passwd,
                         logging_filename,
                         token_client,
                         device_no,
                         ServerKey.TRADING_SERVER_KEY)
        self._logging = get_info_logger(logging_name, filename=logging_filename)
        self._trade_handle_notify_callback = None
        self._trade_notify_ring_buffer = queue.Queue(100)
        self._trade_notify_thread = None
        self._check_keep_alive_seconds_timeout = 0   # it maybe equals to _check_keep_alive_seconds_interval*3。skip timeout check if 0
        self._check_keep_alive_seconds_interval = 0  # using self._heartbeat_interval_sec if 0
        self._trading_logon_heartbeat_timer = None
    
    def start(self, p_token, p_ip, p_port):
        super().start(p_token, p_ip, p_port)
        if self.is_alive():
            self._logging.info(f"Trading socket client start success.")
        else:
            self._logging.info(f"Trading socket client start fail.")
        self.trading_logon_heartbeat(60)  # 每10分钟发送1次交易登录的心跳->600

    def stop(self):
        super().stop()
        if self._trading_logon_heartbeat_timer:
            self._trading_logon_heartbeat_timer.cancel()
            self._trading_logon_heartbeat_timer = None
    
    def handle_notify_for_ever(self, callback):
        self._trade_handle_notify_callback = callback
        
        def trade_wait_notify(_trade_socket_client_self):
            while True:
                if _trade_socket_client_self._trade_notify_thread is None:
                    break
                try:
                    pb_notify = _trade_socket_client_self._trade_notify_ring_buffer.get()
                except queue.Empty:
                    continue
                if pb_notify is None:
                    continue
                if callable(_trade_socket_client_self._trade_handle_notify_callback):
                    _trade_socket_client_self._trade_handle_notify_callback(pb_notify)
                else:
                    print(f"Trade notify callback is not callable：{_trade_socket_client_self._trade_handle_notify_callback}")
                    break

        if self._trade_notify_thread is None:
            self._trade_notify_thread = threading.Thread(target=trade_wait_notify, args=(self,))
            self._trade_notify_thread.setDaemon(True)
            self._trade_notify_thread.start()

    def handle_notify(self, pb_notify):
        self._trade_notify_ring_buffer.put(pb_notify)

    def trading_logon_heartbeat(self, interval=600):
        """
        交易登录心跳，每10分钟1次，解决服务端报错交易登录超时问题
        """
        if not self.is_alive():
            self._logging.debug(f"[KeepAlive] socket is not alive, ignore this trading logon heartbeat!")
            return "", 0
        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=TradeKeepLoginRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               serial_no=1,
                                               token=self._token_client.get_token_from_cache(),
                                               pb_payload=None)
        # 交易登录心跳接口会返回true或false，如果是false说明交易态没有了，需要重新进行交易登录。
        # 启动定时器任务，每隔interval秒执行一次
        if self._trading_logon_heartbeat_timer:
            self._trading_logon_heartbeat_timer.cancel()
            self._trading_logon_heartbeat_timer = None
        self._trading_logon_heartbeat_timer = threading.Timer(interval, self.trading_logon_heartbeat, (interval,))
        self._trading_logon_heartbeat_timer.start()
        self._logging.debug(f"[KeepAlive] sent a trading logon heartbeat message, once every {interval} seconds")
        return request_id, sent_bytes_len

# -*- coding: utf-8 -*-
import asyncio
import base64
import errno
import json
import queue
import selectors
import socket
import ssl
import struct
import threading
import time
import traceback
import urllib
import urllib.request as request
import uuid
from dataclasses import dataclass

from google.protobuf.any_pb2 import Any

from hs.api.constant import StatusCode
from hs.common import rsa_utils, protobuf_utils
from hs.common.aes_ecb import AESCipher
from hs.common.common_utils import now_to_int, get_info_logger
from hs.common.pb.common.constant.RequestMsgType_pb2 import InitConnectRequestMsgType, TradeLoginRequestMsgType, \
    TradeLogoutRequestMsgType
from hs.common.pb.common.constant.ResponseMsgType_pb2 import ResponseMsgType
from hs.common.pb.common.init.InitConnectReq_pb2 import InitConnectReq
from hs.common.pb.common.init.InitConnectResp_pb2 import InitConnectResp
from hs.common.pb.common.msg.HeartBeat_pb2 import HeartBeat
from hs.common.pb.common.msg.Notify_pb2 import PBNotify
from hs.common.pb.common.msg.Request_pb2 import PBRequest
from hs.common.pb.common.msg.Response_pb2 import PBResponse
from hs.common.pb.trade.request.TradeLoginRequest_pb2 import TradeLoginRequest
from hs.common.protobuf_utils import parse_payload, MESSAGE_HEADER_FMT
from hs.common.request_msg_header import RequestMsgHeader
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.ring_buffer import WrappedQueue
from hs.common.token_client import TokenClient

logging_name: str = __name__
DEBUG_MODE: bool = True
BRING_NON_TARGET_WAIT_RESULT_BACK: bool = False
SYNC_GET_RESULT_SECONDS_TIMEOUT: int = 5
MAX_RECV_EMPTY_BYTE_RETRY_TIMES = 0
MAX_START_RETRY_TIMES = 1


@dataclass
class SyncResult:
    result: object = None


@dataclass
class ResponseResult:
    start: int = None
    response: PBResponse = None


class SocketClient(object):
    """Socket连接客户端。注意：服务约束同一个账号只能同时保持一个长链接"""

    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 trading_passwd: str,
                 logging_filename: str,
                 token_client: TokenClient,
                 device_no: str,
                 server_key: str):
        self._logging = get_info_logger(logging_name, filename=logging_filename)
        self.g_serial_no = 0
        self.g_serial_no_lock = threading.RLock()
        self._ring_buffer = WrappedQueue(1)  # 设置最大容量为1
        self._notify_ring_buffer = queue.Queue(5000)
        self._response_dict = dict()
        self._selector = selectors.DefaultSelector()
        self._thread = None
        self._lock = threading.RLock()
        self._notify_thread = None
        self._socket = None
        self._host = None
        self._port = None
        # get device mac address from util
        self._device_no = device_no
        self._rsa_public_key = rsa_public_key
        self._rsa_private_key = rsa_private_key
        if not self._rsa_private_key.startswith('-----'):
            self._rsa_private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + self._rsa_private_key + "\n-----END RSA PRIVATE KEY-----"
        self._encrypted_key = rsa_public_key  # coming from init connection response
        self._heartbeat_interval_sec = 90  # coming from init connection response
        self._login_domain = login_domain
        self._login_country_code = login_country_code
        self._login_mobile = login_mobile
        self._login_passwd = login_passwd
        self._trading_passwd = trading_passwd
        self._serial_no = self.g_serial_no
        self._heartbeat_timer = None
        self._clear_response_result_timer = None
        self._readbuf = bytearray()
        self._is_alive = False
        self._token = ""
        self._conn_info = -1
        self._handle_notify_callback = None  # 推送回报callback
        self._last_keep_alive_seconds_int = now_to_int()
        self._check_keep_alive_seconds_timeout = 0  # it maybe equals to _check_keep_alive_seconds_interval*3。skip timeout check if 0
        self._check_keep_alive_seconds_interval = 30  # using self._heartbeat_interval_sec if 0
        self._max_start_retry_times = MAX_START_RETRY_TIMES
        self._max_recv_empty_byte_times = MAX_RECV_EMPTY_BYTE_RETRY_TIMES  # 连续收到b''的最大次数
        self._token_client = token_client
        self._get_server_key = server_key

    def get_server(self, token):
        return self._get_server(self._login_domain + "/hs/config/queryServer", token)

    def _get_server(self, url, token):
        for i in range(1):  # 错误重试3次
            try:
                if token is None or token == '':
                    raise Exception('Got server info error, token is None.')
                data = {
                    "token": token
                }
                headers = {'Content-Disposition': 'form-data', 'Accept-Charset': 'utf-8',
                           'Content-Type': 'application/x-www-form-urlencoded'}
                data = urllib.parse.urlencode(data).encode("utf-8")
                req = request.Request(url=url, data=data, headers=headers, method='POST')
                with request.urlopen(req, context=ssl._create_unverified_context()) as resp:
                    response = resp.read()
                response = json.loads(rsa_utils.bytes_to_str(response))
                # 取接口服务IP_PORT
                host_port = response.get("data").get(self._get_server_key)  # server_key: "tradeServer", "hqServer"
                host = host_port.split(":")[0]
                port = int(host_port.split(":")[1])
                self._logging.info(f"Got socket server host：{host} port：{port}")
                return host, port
            except Exception as e:
                self._logging.error(f"Got server info error：{e}")
        return None, None

    def start(self, p_token, p_ip, p_port):
        """
        Should be called from main thread
        :return:
        """
        self._token = p_token
        self._host = p_ip
        self._port = p_port

        self._ring_buffer.notify_all()  # notify all ringbuffer waiter
        self._logging.debug("Starting the socket client......")
        self._serial_no = self.init_serial_no(0)
        self.clear_response_result(interval=SYNC_GET_RESULT_SECONDS_TIMEOUT)

        if self._token is None or self._host is None or self._port is None:
            self._logging.debug("the token-host-port is all None, maybe should restart it!")
            self._max_start_retry_times -= 1
            if self._max_start_retry_times > 0:
                self.restart(p_token, p_ip, p_port)
            else:
                self._logging.error(f"Socket启动时已超过最大重试次数：{MAX_START_RETRY_TIMES}，请检查网络是否正常！")
            return
        self._conn_info = self.socket_connect()
        self.register()
        # poll thread
        self._is_alive = True
        with self._lock:
            if self._thread is None:
                self._thread = threading.Thread(target=self._thread_func)
                self._thread.setDaemon(False)  # default False
                self._thread.start()
        # 平台接口-初始化链接
        for i in range(2):
            request_id, _ = self.init_connection()
            init_conn_pb_result = self.async_get_result_direct(request_id, 
                                                               timeout_in_seconds=SYNC_GET_RESULT_SECONDS_TIMEOUT)
            if init_conn_pb_result and init_conn_pb_result.responseCode == "0000":
                break
        # 交易接口-交易登录
        is_trading_passwd_payload_valid = False
        for i in range(1):
            request_id, _ = self.trading_login()
            if request_id is not None and request_id == '':
                is_trading_passwd_payload_valid = True
            else:
                trading_passwd_result = self.async_get_result_direct(request_id, 
                                                                     timeout_in_seconds=SYNC_GET_RESULT_SECONDS_TIMEOUT)
                if trading_passwd_result is not None:
                    trading_passwd_payload = parse_payload(trading_passwd_result)
                    self._logging.debug(f"check trading password: {trading_passwd_payload}")
                    if trading_passwd_payload and trading_passwd_payload.success:
                        is_trading_passwd_payload_valid = True
                        self._last_keep_alive_seconds_int = now_to_int()
                        self._logging.debug(
                            f"heartbeat request self._last_keep_alive_seconds_int：{self._last_keep_alive_seconds_int}")
                        self.heartbeat(self._heartbeat_interval_sec)
                        break
        if not is_trading_passwd_payload_valid:
            self._logging.debug("the trading_passwd_result is None, maybe should restart it!")
            self._max_start_retry_times -= 1
            if self._max_start_retry_times > 0:
                self.restart(p_token, p_ip, p_port)
            else:
                self._logging.error(f"Socket启动时已超过最大重试次数：{MAX_START_RETRY_TIMES}，请检查网络是否正常！")
            return
        # add notify callback
        if self._handle_notify_callback is not None and callable(self._handle_notify_callback):
            self._logging.info("重设 handle_notify_callback")
            self.handle_notify_for_ever(self._handle_notify_callback)
        # check keep alive
        self._last_keep_alive_seconds_int = now_to_int()
        self.heartbeat(self._heartbeat_interval_sec)
        self._max_start_retry_times = MAX_START_RETRY_TIMES
        self._max_recv_empty_byte_times = MAX_RECV_EMPTY_BYTE_RETRY_TIMES
        self._logging.info("The socket client is started!")

    def stop(self):
        self._logging.info("Stopping the socket client...")
        if self._socket and not self._socket._closed:
            try:
                request_id, _ = self.trading_logout()
                if self._socket and not self._socket._closed:
                    self._socket.close()
            except Exception as e:
                self._logging.error(traceback.format_exc())
            finally:
                if self._socket and not self._socket._closed:
                    self._socket.close()
        self.unregister()
        self._is_alive = False
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()
            self._heartbeat_timer = None
        if self._clear_response_result_timer:
            self._clear_response_result_timer.cancel()
            self._clear_response_result_timer = None
        self._ring_buffer.clear()
        self._notify_ring_buffer.put(None)
        self._thread = None
        self._notify_thread = None
        self._serial_no = self.init_serial_no(0)
        self._readbuf[:] = b'\x00' * len(self._readbuf)
        self._socket = None
        # signal.signal(signal.SIGCHLD, grim_reaper)
        self._ring_buffer.notify_all()  # notify all ringbuffer waiter
        self._logging.info("Stopped the socket client already!")

    def restart(self, p_token, p_host, p_port):
        self._token = p_token
        self._host = p_host
        self._port = p_port

        self._logging.info(f"Socket client start reconnect {self._get_server_key}.")
        self.stop()
        self.start(p_token, p_host, p_port)
        if self.is_alive():
            self._logging.info(f"Socket client reconnected {self._get_server_key} success.")
        else:
            self._logging.info(f"Socket client reconnected {self._get_server_key} fail.")

    def register(self):
        if self._socket and not self._socket._closed:
            self._selector.register(self._socket, selectors.EVENT_READ, data=self)
            self._logging.debug("selector registered!")

    def unregister(self):
        for sel_key in list(self._selector.get_map().values()):
            self._selector.unregister(sel_key.fileobj)
            sel_key.fileobj.close()

    def init_connection(self):
        # build payload
        payload = InitConnectReq()
        payload.deviceNo = self._device_no
        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=InitConnectRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               serial_no=0,
                                               token=self._token_client.get_token_from_cache(),
                                               pb_payload=payload)
        self._logging.info(f"Sent a init connection message")
        return request_id, sent_bytes_len

    def trading_login(self):
        # build payload
        passwd = rsa_utils.encrypt_data(self._trading_passwd, self._rsa_public_key)
        passwd = base64.b64encode(passwd).decode("utf-8")
        payload = TradeLoginRequest()
        payload.password = passwd
        payload.authType = ""
        payload.authParam = ""
        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=TradeLoginRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               serial_no=self._serial_no,
                                               token=self._token_client.get_token_from_cache(),
                                               pb_payload=payload)
        self._logging.info(f"Sent a trading login message")
        return request_id, sent_bytes_len

    def trading_logout(self):
        # build payload
        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=TradeLogoutRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               serial_no=self._serial_no,
                                               token=self._token_client.get_token_from_cache(),
                                               pb_payload=None)
        self._logging.debug(f"Sent a trading logout message")
        return request_id, sent_bytes_len
    
    def trading_relogin(self):
        if not self.is_alive():
            return False
        # 执行平台登录获取新的token
        token = self._token_client.reconnect_get_token(self._get_server_key)
        self._token = token
        
        # 重新执行交易登录
        request_id, _ = self.trading_login()
        
        if request_id is not None and request_id == '':
            self._logging.info(f"trading relogined request_id is empty: {request_id}")
            return False
        else:
            trading_passwd_result = self.sync_get_result_direct(request_id, timeout_in_seconds=SYNC_GET_RESULT_SECONDS_TIMEOUT)
            if trading_passwd_result is not None:
                trading_passwd_payload = parse_payload(trading_passwd_result)
                self._logging.debug(f"check trading password: {trading_passwd_payload}")
                
                if trading_passwd_payload and trading_passwd_payload.success:
                    self._last_keep_alive_seconds_int = now_to_int()
                    self._logging.info(f"trading relogined success, heartbeat request self._last_keep_alive_seconds_int：{self._last_keep_alive_seconds_int}")
                    self.heartbeat(self._heartbeat_interval_sec)
                    return True
            else:
                self._logging.info(f"trading relogined response is None: {trading_passwd_result}")
        return False
    
    def heartbeat(self, interval=90):
        if not self.is_alive():
            self._logging.debug(f"[KeepAlive] socket is not alive, ignore this heartbeat!")
            return "", 0
        if self._check_keep_alive_seconds_interval > 0:
            interval = self._check_keep_alive_seconds_interval
        # check keep alive
        keep_alive_duration = now_to_int() - self._last_keep_alive_seconds_int
        if 0 < self._check_keep_alive_seconds_timeout < keep_alive_duration:
            self._logging.error(
                f"[KeepAlive] fail to duration：{keep_alive_duration} > keep_alive_timeout：{self._check_keep_alive_seconds_timeout}, need restart the socket client!")
            return "", 0
        # build payload
        payload = HeartBeat()
        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=0,
                                               msg_header_type_enum=RequestMsgTypeEnum.HEART_BEAT,
                                               serial_no=0,
                                               token=self._token_client.get_token_from_cache(),
                                               pb_payload=payload)
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()
            self._heartbeat_timer = None
        self._heartbeat_timer = threading.Timer(interval, self.heartbeat, (interval,))
        self._heartbeat_timer.start()
        self._logging.debug(f"[KeepAlive] sent a heartbeat message {request_id}, once every {interval} seconds")
        return request_id, sent_bytes_len

    def clear_response_result(self, interval=SYNC_GET_RESULT_SECONDS_TIMEOUT):
        self._logging.debug(f"[KeepAlive] start clear response result, dict size: {len(self._response_dict)}.")
        if len(self._response_dict) > 0:
            clear_list = list()
            for (request_id, resp) in self._response_dict.items():
                req_interval = (int(round(time.time())) - resp.start)
                if req_interval > SYNC_GET_RESULT_SECONDS_TIMEOUT:
                    clear_list.append(request_id)
            if len(clear_list) > 0: 
                for request_id in clear_list:
                    self._logging.debug(f"[KeepAlive] clear response result, ignore {request_id} response result!")
                    del self._response_dict[request_id]
        if self._clear_response_result_timer:
            self._clear_response_result_timer.cancel()
            self._clear_response_result_timer = None
        self._clear_response_result_timer = threading.Timer(interval, self.clear_response_result, (interval,))
        self._clear_response_result_timer.start()
        self._logging.debug(f"[KeepAlive] clear response result end, once every {interval} seconds")
        return

    def build_request_bytes_then_send(self, request_msg_type: int,
                                      msg_header_type_enum: RequestMsgTypeEnum,
                                      serial_no: int,
                                      token: str,
                                      pb_payload):
        if token is None:
            self._logging.error(
                f"Token is None, request_msg_type：{request_msg_type}, msg_header_type_enum：{msg_header_type_enum}, serial_no：{token}, ignore this request.")
            return None, None, 0
        try:
            request = PBRequest()
            request.requestMsgType = request_msg_type
            request.token = token
            request.requestId = str(uuid.uuid1())
            request.requestTime = int(round(time.time() * 1000))
            # build request message header
            request_msg_header = RequestMsgHeader()
            request_msg_header.serial_no = self.compare_and_set_serial_no(self._serial_no)
            request_msg_header.msg_type = RequestMsgTypeEnum.get_id(msg_header_type_enum)
            # set request payload
            if pb_payload:
                any_obj = Any()
                any_obj.Pack(pb_payload)
                request.payload.CopyFrom(any_obj)
            # set request header's body_sha1
            request_msg_header.body_sha1 = rsa_utils.rsa_sign(request.SerializeToString(), self._rsa_private_key)
            # 把数据对象打包为字节对象
            encrypt_secret_key = self._encrypted_key
            encrypt_payload = request.SerializeToString()
            if request_msg_header.serial_no == 0:
                encrypt_secret_key = self._rsa_public_key
                if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                        or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value:
                    # Socket登录初始化RSA
                    encrypt_payload = rsa_utils.encrypt_data(request.SerializeToString(), encrypt_secret_key)
            else:
                # 业务请求AES
                if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                        or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value \
                        or request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
                    encrypt_payload = AESCipher(encrypt_secret_key).encrypt(request.SerializeToString())
            msg_bytes = protobuf_utils.pack_request(request_msg_header, encrypt_payload)
            # send msg
            sent_bytes_len = self._socket.send(msg_bytes)
            return request.requestId, msg_bytes, sent_bytes_len
        except IOError as e:
            if DEBUG_MODE:
                self._logging.error(traceback.format_exc())
            else:
                self._logging.error(f"IOError Occurred：{type(e)}, maybe need restart the socket!")
            if e.errno == errno.EPIPE:
                self._logging.error(f"BrokenPipeError Occurred：{type(e)}, currently maybe need restart the socket!")
        except Exception as e:
            if DEBUG_MODE:
                self._logging.error(traceback.format_exc())
            else:
                self._logging.error(f"Send error：{type(e)}, maybe need restart the socket!")
        return None, None, 0

    def socket_connect(self):
        """
        connection and return connection info
        return: 0-OK，not 0-fail
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # FIX问题：python - Python，为什么在使用TCP套接字时出现10035(在服务器上)和10053(在客户端上)错误？ https://www.coder.work/article/386867
            self._socket.setblocking(True)
            conn_info = self._socket.connect_ex((self._host, self._port))
            self._socket.setblocking(False)  # 将setblocking(False)放到connect方法之后执行
            # self._socket.settimeout(0.02)  # non-blocking。时间久了就可能在在recv()处出现异常 ConnectionResetError: [Errno 54] Connection reset by peer
            self._logging.info(f"Socket connect info：{conn_info}, socket.fileno()：{self._socket.fileno()}")
            return conn_info
        except Exception as e:
            self.stop()
            self._logging.error(traceback.format_exc())
        return -1

    def sync_get_result_direct(self, request_id, callback=None, timeout_in_seconds=None):
        event = threading.Event()
        event.clear()
        sync_result: SyncResult = SyncResult()

        def wait_response():
            while True:
                try:
                    if event.isSet() or not self.is_alive():
                        event.set()
                        break
                    # below logic from Queue.queue.get()
                    # pb_response = self._ring_buffer.get()  # get and wait
                    with self._ring_buffer.not_empty:
                        while not self._ring_buffer._qsize() and not event.isSet() and self.is_alive():
                            self._ring_buffer.not_empty.wait(1)
                        pb_response = self._ring_buffer._get()
                        self._ring_buffer.not_full.notify()
                    if request_id:
                        if pb_response.requestId == request_id:
                            sync_result.result = pb_response
                            event.set()
                            return
                        elif BRING_NON_TARGET_WAIT_RESULT_BACK:
                            # 如果不是本次指定的request_id对应的结果，就放回ring_buffer的最左边元素位置
                            self._ring_buffer.appendleft(pb_response)
                            self._logging.error(
                                f"request_id：{request_id} got other's result, now put it back to ringbuffer")
                        else:
                            self._logging.error(
                                f"request_id：{request_id} got result of another request_id：{pb_response.requestId}, ignore it!")
                    if callable(callback):
                        callback(pb_response)
                    else:
                        self._logging.error(f"Wait_response callback is not callable：{callback}")
                    # finally, also event set
                    sync_result.result = None
                    event.set()
                    return
                except Exception as e:
                    self._logging.error(f"Error Occurred：{e}，currently release the wait_result!")
                    sync_result.result = None
                    event.set()
                    return

        sync_thread = threading.Thread(target=wait_response)
        sync_thread.setDaemon(False)
        sync_thread.start()
        event.wait(timeout=timeout_in_seconds)
        event.set()
        pb_result = sync_result.result
        if pb_result is None:
            return None
        elif pb_result.DESCRIPTOR.name == PBResponse.DESCRIPTOR.name:
            if pb_result.responseCode != "0000":
                self._logging.error(
                    f"出现异常业务状态码！requestId：{pb_result.requestId}，responseCode：{pb_result.responseCode}, responseMsg：{pb_result.responseMsg}")
                if pb_result.responseCode in ["112", "1012", "1013", "1014"]:  # 登录失败要重连：112-交易登录超时，1012-用户未登录，1013-登陆被挤下线，1014-登录超时
                    # 登录超时异常状态码处理
                    self.trading_relogin()
        return pb_result

    def async_get_result_direct(self, request_id, timeout_in_seconds=SYNC_GET_RESULT_SECONDS_TIMEOUT):
        event = threading.Event()
        event.clear()
        sync_result: SyncResult = SyncResult()
        sync_result.result = None

        def await_response():
            while True:
                try:
                    if event.isSet() or not self.is_alive():
                        event.set()
                        return
                    
                    if request_id:
                        if request_id in self._response_dict:
                            sync_result.result = self._response_dict[request_id].response
                            del self._response_dict[request_id]
                            event.set()
                            return 
                        else:
                            time.sleep(0.005)
                    else:
                        event.set()
                        return
                except Exception as e:
                    self._logging.error(f"Async Get Result Error Occurred：{e}，currently release the wait_result!")
                    sync_result.result = None
                    event.set()
                    return

        sync_thread = threading.Thread(target=await_response)
        sync_thread.setDaemon(False)
        sync_thread.start()
        event.wait(timeout=timeout_in_seconds)
        event.set()
        pb_result = sync_result.result
        if pb_result is None:
            pb_result = PBResponse()
            pb_result.responseCode = StatusCode.INVOKE_TIME_OUT
            pb_result.responseMsg = "接口调用超时"
            return 
        elif pb_result.DESCRIPTOR.name == PBResponse.DESCRIPTOR.name:
            if pb_result.responseCode != "0000":
                self._logging.error(
                    f"出现异常业务状态码！requestId：{pb_result.requestId}，responseCode：{pb_result.responseCode}, responseMsg：{pb_result.responseMsg}")
                if pb_result.responseCode in ["112", "1012", "1013", "1014"]:  # 登录失败要重连：112-交易登录超时，1012-用户未登录，1013-登陆被挤下线，1014-登录超时
                    # 登录超时异常状态码处理
                    self.trading_relogin()
        return pb_result
    
    def handle_notify_for_ever(self, callback):
        self._handle_notify_callback = callback

        def wait_notify(_socket_client_self):
            while True:
                if _socket_client_self._notify_thread is None:
                    break
                try:
                    pb_notify = _socket_client_self._notify_ring_buffer.get()  # default block=True
                except queue.Empty:
                    continue
                if pb_notify is None:
                    continue
                if callable(_socket_client_self._handle_notify_callback):
                    _socket_client_self._handle_notify_callback(pb_notify)
                else:
                    print(f"Notify callback is not callable：{_socket_client_self._handle_notify_callback}")
                    break

        if self._notify_thread is None:
            self._notify_thread = threading.Thread(target=wait_notify, args=(self,))
            self._notify_thread.setDaemon(True)
            self._notify_thread.start()

    async def wait_result(self, request_id=None,
                          future=None,
                          callback=None,
                          asyncio_semaphore: asyncio.Semaphore = asyncio.Semaphore(1)):
        async with asyncio_semaphore:
            while True:
                try:
                    if len(self._ring_buffer) < 1 and self.is_alive():
                        await asyncio.sleep(0.02)
                        continue
                    pb_response = self._ring_buffer.popleft()
                    if request_id and future:
                        if pb_response.requestId == request_id:
                            future.set_result(pb_response)
                            return
                        elif BRING_NON_TARGET_WAIT_RESULT_BACK:
                            # 如果不是本次指定的request_id对应的结果，就放回ring_buffer的最左边元素位置
                            self._ring_buffer.appendleft(pb_response)
                            self._logging.error(
                                f"request_id：{request_id} got other's result, now put it back to ringbuffer")
                        else:
                            self._logging.error(
                                f"request_id：{request_id} got result of another request_id：{pb_response.requestId}, ignore it!")
                    if callable(callback):
                        callback(pb_response)
                    else:
                        self._logging.error(f"Callback is not callable：{callback}")
                    # finally, return None future
                    future.set_result(None)
                    return
                except Exception as e:
                    self._logging.info(f"Error Occurred：{e}，currently release the wait_result!")
                    future.set_result(None)
                    return

    def _thread_func(self):
        while True:
            with self._lock:
                if not self.is_alive():
                    self._thread = None
                    break
            self.poll()

    def poll(self):
        events = self._selector.select(0.001)  # select(0.02)
        for key, evt_mask in events:
            conn = key.data
            #######
            # read_socket, write_socket = socket.socketpair()
            # print(f"[DDDDDDDDDEBUG]：{key.fileobj==read_socket}")
            #######
            if evt_mask & selectors.EVENT_READ != 0:
                try:
                    if not self.is_alive():
                        self._logging.info("poll shutdown...")
                        break
                    # 在socket非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。
                    # 参考：socket recv 10035 error 如何解决 https://bbs.csdn.net/topics/210068263
                    self.decode_response(conn)
                except socket.error as e:
                    if DEBUG_MODE:
                        self._logging.error(traceback.format_exc())
                    else:
                        self._logging.error(f"BlockingIOError Occurred：{type(e)}, maybe need restart the socket!")
                    if e.errno == errno.EAGAIN:  # str(e) == "[Errno 35] Resource temporarily unavailable"
                        self._logging.error(f"BlockingIOError Occurred：{type(e)}, just need continue to next step!")
                        # time.sleep(0.1)  # just need continue to next step
                    self.stop()  # 解决Windows下报错：ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
                except Exception as e:
                    if DEBUG_MODE:
                        self._logging.error(traceback.format_exc())
                    else:
                        self._logging.error(f"Poll decode_response Error：{e}")
                    self.stop()  # 解决Windows下报错：ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。

    def decode_response(self, conn):
        recv_bytes = self._socket.recv(1024 * 1024)  # buffer size e.g. 151 或 1024 或 128*1024
        if recv_bytes == b'':  # recv超时异常：TimeoutError: [Errno 60] Operation timed out 断网很久就会连续发送b''，如果次数较多就需要人工重启连接
            self._max_recv_empty_byte_times -= 1
            self._logging.error(
                f"Note: The decode_response recv_bytes == b''，max_recv_empty_byte_times：{self._max_recv_empty_byte_times}!")
            if self._max_recv_empty_byte_times < 0:
                # 断网太久，期间有send操作导致超时，可尝试方案：socket.setdefaulttimeout(10)、sock.settimeout(20|None) 或 sock.setblocking(True|False)
                self._is_alive = False
                self.stop()
                return
        else:
            self._max_recv_empty_byte_times = MAX_RECV_EMPTY_BYTE_RETRY_TIMES
            self._readbuf.extend(recv_bytes)
        while len(self._readbuf) > 0:
            # 检查readbuf是否可以完整解1个包
            pack_size = struct.calcsize(MESSAGE_HEADER_FMT)
            if len(self._readbuf) < pack_size:
                return
            unpack_msg = struct.unpack(MESSAGE_HEADER_FMT, self._readbuf[:pack_size])
            body_len = unpack_msg[5]
            if len(self._readbuf) < pack_size + body_len:
                self._logging.debug(
                    f"maybe the total read bytes({len(self._readbuf)}) is not enough to {pack_size}+{body_len}, just waiting the next bytes streaming!")
                return
            full_pack_bytes = self._readbuf[:pack_size + body_len]
            del self._readbuf[:pack_size + body_len]
            request_msg_header, pb_response, payload = protobuf_utils.unpack_response(full_pack_bytes,
                                                                                      self._rsa_public_key,
                                                                                      self._rsa_private_key,
                                                                                      self._encrypted_key)
            if request_msg_header.msg_type == RequestMsgTypeEnum.HEART_BEAT.value:
                self._last_keep_alive_seconds_int = now_to_int()
                self._logging.debug(
                    f"[KeepAlive] got response for heartbeat request, self._last_keep_alive_seconds_int：{self._last_keep_alive_seconds_int}，ignore it!")
                return
            elif request_msg_header.body_len < 1:
                self._logging.debug("response payload body len < 1, ignore it!")
                return
            elif pb_response and hasattr(pb_response, "responseMsgType") and (
                    pb_response.responseMsgType == ResponseMsgType.TradeKeepLoginResponseMsgType):
                self._logging.debug(f"got response for trading logon heartbeat, ignore it!")
                return
            # self._serial_no = self.compare_and_set_serial_no(request_msg_header.serial_no)
            # if self._serial_no < 1:
                # self._logging.error("Maybe you should restart the socket client and reset self._serial_no to 0!")
                # return 
            self._logging.debug(
                f"decode_response total recv_bytes_len：{len(full_pack_bytes)}，request_msg_header.serial_no：{request_msg_header.serial_no}")
            if pb_response.DESCRIPTOR.name == PBNotify.DESCRIPTOR.name:
                notify_id = pb_response.notifyId
                self._logging.debug(f"received notify and append to notify ringbuffer, notifyId：{notify_id}")
                self.handle_notify(pb_response)
            else:
                request_id = pb_response.requestId
                if pb_response.payload.Is(InitConnectResp.DESCRIPTOR):
                    conn._encrypted_key = payload.encryptedKey
                    conn._heartbeat_interval_sec = payload.heartbeatIntervalSec
                self._logging.debug(f"received message and append to ringbuffer, requestId：{request_id}")
                # 接口响应结果
                response_result = ResponseResult()
                response_result.response = pb_response
                response_result.start = int(round(time.time()))
                self._response_dict[request_id] = response_result

    def handle_notify(self, pb_notify):
        self._notify_ring_buffer.put(pb_notify)

    def is_alive(self) -> bool:
        alive = self._is_alive and not (self._socket is None or self._socket._closed)
        return alive

    def init_serial_no(self, serial_no):
        with self.g_serial_no_lock:
            self.g_serial_no = serial_no
        return self.g_serial_no

    def compare_and_set_serial_no(self, serial_no):
        with self.g_serial_no_lock:
            ret_id = self.g_serial_no
            self.g_serial_no += 1
            # 4294967295是2的32次方-1
            if self.g_serial_no >= 4294967295:
                self.g_serial_no = 0
            return ret_id

    def __enter__(self):
        if not self.is_alive():
            self.stop()

            token = self._token_client.reconnect_get_token(self._get_server_key)
            host, port = self.get_server(token)
            self.restart(token, host, port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and exc_val is not None and exc_tb is not None:
            # exit with-as once catching the throwed except in with-as body
            self.stop()
            traceback.print_exception(exc_type, exc_val, exc_tb)
            return True
        return False



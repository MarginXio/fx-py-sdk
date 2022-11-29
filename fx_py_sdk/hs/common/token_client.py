# -*- coding:utf-8 -*-
import base64
import datetime
import json
import ssl
import urllib
import urllib.request as request

from hs.api.constant import ServerKey
from hs.common import rsa_utils
from hs.common.common_utils import get_info_logger

logging_name: str = __name__

TOKEN_CACHE_TIME: int = 900  # token缓存时间15分钟


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class TokenClient(object):
    """
    Token管理类
    """

    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 device_no: str,
                 logging_filename: str,
                 quote_stand_alone: bool):
        self._logging = get_info_logger(logging_name, filename=logging_filename)
        self._rsa_public_key = rsa_public_key
        self._encrypted_key = rsa_public_key  # coming from init connection response
        self._rsa_private_key = rsa_private_key
        if not self._rsa_private_key.startswith('-----'):
            self._rsa_private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + self._rsa_private_key + "\n-----END RSA PRIVATE KEY-----"
        self._login_domain = login_domain
        self._login_country_code = login_country_code
        self._login_mobile = login_mobile
        self._login_passwd = login_passwd
        self._device_no = device_no
        self._quote_stand_alone = quote_stand_alone  # 行情作为独立程序
        self._cache_token = {"token": None, "time": datetime.datetime.now()}  # Token 缓存

    def get_token(self):
        """
        首次启动获取平台登录Token
        
        Returns
        -------
        """
        # get http login token
        token, _ = self._get_token(
            url=self._login_domain + "/hs/v2/login",
            country_code=self._login_country_code,
            mobile=self._login_mobile,
            passwd=self._login_passwd)

        if token is None:
            raise Exception('Got login token error, token is None.')

        self._cache_token["token"] = token
        self._cache_token["time"] = datetime.datetime.now()  # 缓存时间
        self._logging.info(f"Token client http login and set token cache and return.")
        return token

    def reconnect_get_token(self, server_key: str):
        """
        重连获取平台登录Token
        Parameters
        ----------
        server_key
        Returns
        -------
        """
        if server_key == ServerKey.HQ_SERVER_KEY and not self._quote_stand_alone and self._cache_token["token"] is not None:
            self._logging.info(f"Quote client get token cache and return.")
            return self._cache_token["token"]

        if self._cache_token["token"] is not None:  # 校验时间
            start = self._cache_token["time"]
            now = datetime.datetime.now()
            seconds = (now - start).seconds
            if seconds < TOKEN_CACHE_TIME:  # 未过期
                self._logging.info(f"Token client get token from cache and return, interval: {seconds}s")
                return self._cache_token["token"]

        try:
            token = self.get_token()

            if token is not None:
                self._cache_token["token"] = token
                self._cache_token["time"] = datetime.datetime.now()
                self._logging.info(f"Token client reconnect update token cache, date time: {datetime.datetime.now()}")
            return token
        except Exception as e:
            self._logging.error(f"Token client get token exception, please try again later. {e}")

    def get_token_from_cache(self):
        return self._cache_token["token"]

    def _get_token(self, url: str, country_code: str, mobile: str, passwd: str):
        for i in range(1):  # 错误重试3次
            try:
                passwd = rsa_utils.encrypt_data(passwd, self._rsa_public_key)
                passwd = base64.b64encode(passwd).decode("utf-8")
                data = {
                    "countryCode": country_code,
                        "mobile": mobile,
                    "deviceNo": self._device_no,
                    "password": passwd,
                }
                headers = {'Content-Disposition': 'form-data', 'Accept-Charset': 'utf-8',
                           'Content-Type': 'application/x-www-form-urlencoded'}
                data = urllib.parse.urlencode(data).encode("utf-8")
                req = request.Request(url=url, data=data, headers=headers, method='POST')
                with request.urlopen(req, context=ssl._create_unverified_context()) as resp:
                    response = resp.read()
                response = json.loads(rsa_utils.bytes_to_str(response))
                if response.get("respCode") != '0000':
                    self._logging.error(f"HTTP Login fail response：{response}")
                    return None, None
                token = response.get("data").get("token")
                decrypt_token = rsa_utils.decrypt_data(token, self._rsa_private_key)
                decrypt_token_str = rsa_utils.bytes_to_str(decrypt_token)
                self._logging.info(f"Got Token：{decrypt_token_str}")
                return decrypt_token_str, response
            except Exception as e:
                self._logging.error(f"Got token error：{e}")
        return None, None

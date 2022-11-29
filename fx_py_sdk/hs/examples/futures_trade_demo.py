# -*- coding: utf-8 -*-
import threading
import time

from hs.api.constant import EntrustBS, ModelResult, FuturesEntrustType, FuturesValidTimeType
from hs.api.futures_api import FuturesAPI
from hs.common.common_utils import now_to_str
from hs.common.protobuf_utils import parse_payload


class FuturesTradeDemo(object):
    """期货交易类接口独立Demo程序"""

    def __init__(self, **kwargs):
        self._futures_api = FuturesAPI(**kwargs)
        self.timer_threading = None

    def get_token(self):
        """获取平台Token"""
        return self._futures_api.get_token()

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        print(f"Stock Trading Api is alive：{self._futures_api.is_alive()}")
        return self._futures_api.is_alive()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._futures_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._futures_api.add_notify_callback(self.notify_callback)
        return self

    def futures_entrust(self) -> ModelResult:
        """期货委托下单"""
        model_result = self._futures_api.futures_entrust(stock_code="CUSH2",
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
        model_result = self._futures_api.futures_change_entrust(entrust_id=entrust_id,
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
        model_result = self._futures_api.futures_cancel_entrust(entrust_id=entrust_id,
                                                                stock_code="CUSH2")
        if model_result.is_success:
            print(f"futures cancel_entrust_id：{model_result.get_model()}")
        else:
            print(f"futures fail to cancel entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def futures_query_holds_list(self):
        """期货查询持仓"""
        model_result = self._futures_api.futures_query_holds_list()
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
        model_result = self._futures_api.futures_query_fund_info()
        if model_result.is_success:
            print(f"期货查询资金信息：{model_result.get_model()}")
        else:
            print(f"futures fail to query_fund_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_max_buy_sell_amount(self):
        """查询期货最大可买/卖"""
        model_result = self._futures_api.futures_query_max_buy_sell_amount(stock_code="CUSH2")
        if model_result.is_success:
            print(f"查询期货最大可买/卖：{model_result.get_model()}")
        else:
            print(f"futures fail to query_max_buy_sell_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_real_entrust_list(self):
        """期货查询今日委托"""
        model_result = self._futures_api.futures_query_real_entrust_list()
        if model_result.is_success:
            print(f"期货查询今日委托：{model_result.get_model()}")
        else:
            print(f"futures fail to query_real_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_history_entrust_list(self):
        """期货查询历史委托"""
        model_result = self._futures_api.futures_query_history_entrust_list(page_no=1,
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
        model_result = self._futures_api.futures_query_real_deliver_list()
        if model_result.is_success:
            print(f"期货查询今日成交：{model_result.get_model()}")
        else:
            print(f"futures fail to query_real_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_query_history_deliver_list(self):
        """期货查询历史成交"""
        model_result = self._futures_api.futures_query_history_deliver_list(page_no=1,
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
        model_result = self._futures_api.futures_query_product_info(stock_code_list)
        if model_result.is_success:
            print(f"期货查询产品信息：{model_result.get_model()}")
        else:
            print(f"futures fail to query_product_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_trade_subscribe(self):
        """期货订阅交易推送消息"""
        model_result = self._futures_api.trade_subscribe()
        if model_result.is_success:
            print(f"订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_subscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def futures_trade_unsubscribe(self):
        """取消订阅期货交易推送消息"""
        model_result = self._futures_api.trade_unsubscribe()
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
        self.futures_query_holds_list()
    
    def stop(self):
        """退出业务API上下文环境"""
        self.timer_threading.cancel()
        self._futures_api.stop()


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
    # 2、初始化交易API对象、增加消息推送回调函数
    trade_demo = FuturesTradeDemo(**params).add_notify_callback()
    # 3、执行HTTP登录、获取token及连接ip port
    token = trade_demo.get_token()
    # 4、启动交易API上下文，并会初始化连接、交易登录
    trade_demo.start(token)
    # 5、检查连接状态
    is_alive = trade_demo.check_alive()

    if is_alive:
        # 增加线程接口轮询，维持登录态
        trade_demo.timer_callback(interval=30)
        
        entrustResult = None
        # 6、命令形式展示  
        while True:
            print("###### 接口名: futures_entrust，                          接口描述: 订单接口-期货委托/改单/撤单                                ######")
            print("###### 接口名: futures_query_holds_list，                 接口描述: 查询接口-期货查询持仓                                      ######")
            print("###### 接口名: futures_query_fund_info，                  接口描述: 查询接口-期货查询资金信息                                  ######")
            print("###### 接口名: futures_query_max_buy_sell_amount，        接口描述: 查询接口-查询期货最大可买/卖                               ######")
            print("###### 接口名: futures_query_real_entrust_list，          接口描述: 查询接口-期货查询今日委托                                  ######")
            print("###### 接口名: futures_query_history_entrust_list，       接口描述: 查询接口-期货查询历史委托                                  ######")
            print("###### 接口名: futures_query_real_deliver_list，          接口描述: 查询接口-期货查询今日成交                                  ######")
            print("###### 接口名: futures_query_history_deliver_list，       接口描述: 查询接口-期货查询历史成交                                  ######")
            print("###### 接口名: futures_query_product_info，               接口描述: 查询接口-期货查询产品信息                                  ######")
            print("###### 接口名: futures_trade_subscribe，                  接口描述: 订阅接口-期货订阅交易推送消息                              ######")
            print("###### 接口名: futures_trade_unsubscribe，                接口描述: 订阅接口-取消订阅期货交易推送消息                          ######")
            print("###### 接口名: stop，                                     接口描述: ！！！程序退出，该函数将退出登录，并断开TCP链接！！！      ######")
            method_name = input("请输入需要查看的接口名: ")
    
            if method_name == "futures_entrust":
                # 委托下单
                entrustResult = trade_demo.futures_entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = trade_demo.futures_change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # trade_demo.futures_cancel_entrust(entrustResult.get_model())
            elif method_name == "futures_query_holds_list":
                # 查询接口-期货查询持仓
                trade_demo.futures_query_holds_list()
            elif method_name == "futures_query_fund_info":
                # 查询接口-期货查询资金信息
                trade_demo.futures_query_fund_info()
            elif method_name == "futures_query_max_buy_sell_amount":
                # 查询接口-查询期货最大可买/卖
                trade_demo.futures_query_max_buy_sell_amount()
            elif method_name == "futures_query_real_entrust_list":
                # 查询接口-期货查询今日委托
                trade_demo.futures_query_real_entrust_list()
            elif method_name == "futures_query_history_entrust_list":
                # 查询接口-期货查询历史委托
                trade_demo.futures_query_history_entrust_list()
            elif method_name == "futures_query_real_deliver_list":
                # 查询接口-期货查询今日成交
                trade_demo.futures_query_real_deliver_list()
            elif method_name == "futures_query_history_deliver_list":
                # 查询接口-期货查询历史成交
                trade_demo.futures_query_history_deliver_list()
            elif method_name == "futures_query_product_info":
                # 查询接口-期货查询产品信息
                trade_demo.futures_query_product_info()
            elif method_name == "futures_trade_subscribe":
                # 订阅接口-期货订阅交易推送消息
                trade_demo.futures_trade_subscribe()
            elif method_name == "futures_trade_unsubscribe":
                # 订阅接口-取消订阅期货交易推送消息
                trade_demo.futures_trade_unsubscribe()
            elif method_name == "stop":
                # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
                trade_demo.stop()
                exit(1)
            else:
                print("接口名输入有误，请参考提示重新输入！")
    else:
        # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
        trade_demo.stop()
        exit(1)
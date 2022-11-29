# -*- coding: utf-8 -*-
import threading

from hs.api.constant import ModelResult, DataType, Direction, ExRightFlag, CycType, SecurityParam, HQSubscribeTopicId, \
    MktTmType, DepthBookType
from hs.api.quote_api import QuoteAPI
from hs.common.protobuf_utils import parse_payload


class StockQuoteDemo(object):
    """股票行情类接口独立Demo程序"""
    def __init__(self, **kwargs):
        self._quote_api = QuoteAPI(**kwargs)
        self.timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._quote_api.is_alive()

    def get_token(self):
        """获取平台Token"""
        return self._quote_api.get_token()

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._quote_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._quote_api.add_notify_callback(self.notify_callback)
        return self

    def query_hq_basic_qot(self) -> ModelResult:
        """批量查询股票基础报价"""
        security_list = [SecurityParam(DataType.HK_STOCK, "00700.HK"),
                         SecurityParam(DataType.HK_STOCK, "01810.HK")]
        model_result = self._quote_api.query_hq_basic_qot(security_list=security_list)
        if model_result.is_success:
            print(f"hq basic quote：{model_result.get_model()}")
        else:
            print(f"fail to query hq basic quote, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_broker(self) -> ModelResult:
        """查询买卖经纪摆盘"""
        model_result = self._quote_api.query_hq_broker(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"))
        if model_result.is_success:
            print(f"hq broker：{model_result.get_model()}")
        else:
            print(f"fail to query hq broker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_order_book(self) -> ModelResult:
        """查询买卖档"""
        model_result = self._quote_api.query_order_book(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
                                                        mkt_tm_type=MktTmType.MID_SESSION)
        if model_result.is_success:
            print(f"order book：{model_result.get_model()}")
        else:
            print(f"fail to query order book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_ticker(self) -> ModelResult:
        """查询最近多少条的逐笔列表"""
        model_result = self._quote_api.query_hq_ticker(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
                                                       limit=10)
        if model_result.is_success:
            print(f"hq ticker：{model_result.get_model()}")
        else:
            print(f"fail to query hq ticker, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_hq_kline(self) -> ModelResult:
        """查询K线数据"""
        model_result = self._quote_api.query_hq_kline(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"),
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
        model_result = self._quote_api.query_hq_time_share(security_param=SecurityParam(DataType.HK_STOCK, "01810.HK"))
        if model_result.is_success:
            print(f"hq time share：{model_result.get_model()}")
        else:
            print(f"fail to query hq time share, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def query_depth_order_book(self):
        """查询深度摆盘数据"""
        model_result = self._quote_api.query_order_book(security_param=SecurityParam(DataType.US_STOCK, "BABA"),
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.BASIC_QOT,
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.TICKER,
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.BROKER,
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.ORDER_BOOK,
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.TOTALVIEW_BOOK,
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
        model_result = self._quote_api.hq_subscribe(topic_id=HQSubscribeTopicId.ARCA_BOOK,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.BASIC_QOT,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.TICKER,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.BROKER,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.ORDER_BOOK,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.TOTALVIEW_BOOK,
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
        model_result = self._quote_api.hq_unsubscribe(topic_id=HQSubscribeTopicId.ARCA_BOOK,
                                                    security_list=security_list)
        if model_result.is_success:
            print(f"取消订阅深度摆盘ARCABOOK推送消息：{model_result.get_model()}")
        else:
            print(f"fail to hq_unsubscribe arca book, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def notify_callback(self, pb_notify):
        """
        定义处理消息推送的callback
        :param pb_notify  参考 PBNotify.proto
        notifyMsgType:
        OrderBookNotifyMsgType = 20001
        BrokerQueueNotifyMsgType = 20002
        BasicQotNotifyMsgType = 20003
        TickerNotifyMsgType = 20004
        """
        print(f"hq_notify_callback，notifyMsgType：{pb_notify.notifyMsgType}，pb_notify：{pb_notify}，payload：{parse_payload(pb_notify)}")

    def timer_callback(self, interval=30):
        """"
        增加线程接口轮询，维持登录态
        """
        self.timer_threading = threading.Timer(interval, self.timer_callback, (interval,))
        self.timer_threading.setDaemon(False)
        self.timer_threading.start()
        self.query_hq_basic_qot()

    def stop(self):
        """退出业务API上下文环境"""
        self.timer_threading.cancel()
        self._quote_api.stop()


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
        "login_mobile": "18868118901", # 登录账号无需加区号
        "login_passwd": "lining911",
        "trading_passwd": "",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 2、初始化行情API对象、增加消息推送回调函数
    quote_demo = StockQuoteDemo(**params).add_notify_callback()
    # 3、执行HTTP登录、获取token及连接ip port
    token = quote_demo.get_token()
    # 4、启动行情API上下文，并会初始化连接、交易登录
    quote_demo.start(token)
    # 5、检查连接状态
    is_alive = quote_demo.check_alive()

    if is_alive:
        # 增加线程接口轮询
        quote_demo.timer_callback(interval=30)
        
        # 6、命令形式展示
        while True:
            print("###### 接口名: query_hq_basic_qot，            接口描述: 行情接口-基础报价                                          ######")
            print("###### 接口名: query_hq_broker，               接口描述: 行情接口-买卖经纪摆盘                                      ######")
            print("###### 接口名: query_order_book，              接口描述: 行情接口-查询买卖档                                        ######")
            print("###### 接口名: query_hq_ticker，               接口描述: 行情接口-查询最近多少条的逐笔列表                          ######")
            print("###### 接口名: query_hq_kline，                接口描述: 行情接口-K线数据                                           ######")
            print("###### 接口名: query_hq_time_share，           接口描述: 行情接口-查询分时数据                                      ######")
            print("###### 接口名: query_depth_order_book，        接口描述: 行情接口-查询深度摆盘数据                                  ######")
            print("###### 接口名: hq_subscribe_basic_qot，        接口描述: 行情接口-订阅基础行情推送消息（需要时才使用）              ######")
            print("###### 接口名: hq_subscribe_ticker，           接口描述: 行情接口-订阅逐笔推送消息（需要时才使用）                  ######")
            print("###### 接口名: hq_subscribe_broker，           接口描述: 行情接口-订阅买卖经纪推送消息（需要时才使用）              ######")
            print("###### 接口名: hq_subscribe_order_book，       接口描述: 行情接口-订阅买卖档推送消息（需要时才使用）                ######")
            print("###### 接口名: hq_subscribe_total_view_book，  接口描述: 行情接口-订阅深度摆盘TOTALVIEW推送消息（需要时才使用）     ######")
            print("###### 接口名: hq_subscribe_arca_book，        接口描述: 行情接口-订阅深度摆盘ARCABOOK推送消息（需要时才使用）      ######")
            print("###### 接口名: hq_unsubscribe_basic_qot，      接口描述: 行情接口-取消订阅基础行情推送消息（需要时才使用）          ######")
            print("###### 接口名: hq_unsubscribe_ticker，         接口描述: 行情接口-取消订阅逐笔推送消息（需要时才使用）              ######")
            print("###### 接口名: hq_unsubscribe_broker，         接口描述: 行情接口-取消订阅买卖经纪推送消息（需要时才使用）          ######")
            print("###### 接口名: hq_unsubscribe_order_book，     接口描述: 行情接口-取消订阅买卖档推送消息（需要时才使用）            ######")
            print("###### 接口名: hq_unsubscribe_total_view_book，接口描述: 行情接口-取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用） ######")
            print("###### 接口名: hq_unsubscribe_arca_Book，      接口描述: 行情接口-取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）  ######")
            print("###### 接口名: stop，                          接口描述: ！！！程序退出，该函数将退出登录，并断开TCP链接！！！      ######")
            method_name = input("请输入需要查看的接口名: ")
    
            if method_name == "query_hq_basic_qot":
                # 批量查询股票基础报价
                quote_demo.query_hq_basic_qot()
            elif method_name == "query_hq_broker":
                # 查询买卖经纪摆盘
                quote_demo.query_hq_broker()
            elif method_name == "query_order_book":
                # 查询买卖档
                quote_demo.query_order_book()
            elif method_name == "query_hq_ticker":
                # 查询最近多少条的逐笔列表
                quote_demo.query_hq_ticker()
            elif method_name == "query_hq_kline":
                # 查询K线数据
                quote_demo.query_hq_kline()
            elif method_name == "query_hq_time_share":
                # 查询分时数据
                quote_demo.query_hq_time_share()
            elif method_name == "query_depth_order_book":
                # 查询深度摆盘数据
                quote_demo.query_depth_order_book()
            elif method_name == "hq_subscribe_basic_qot":
                # 订阅基础行情推送消息（需要时才使用）
                quote_demo.hq_subscribe_basic_qot()
            elif method_name == "hq_subscribe_ticker":
                # 订阅逐笔推送消息（需要时才使用）
                quote_demo.hq_subscribe_ticker()
            elif method_name == "hq_subscribe_broker":
                # 订阅买卖经纪推送消息（需要时才使用）
                quote_demo.hq_subscribe_broker()
            elif method_name == "hq_subscribe_order_book":
                # 订阅买卖档推送消息（需要时才使用）
                quote_demo.hq_subscribe_order_book()
            elif method_name == "hq_subscribe_total_view_book":
                # 订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                quote_demo.hq_subscribe_total_view_book()
            elif method_name == "hq_subscribe_arca_book":
                # 订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                quote_demo.hq_subscribe_arca_book()
            elif method_name == "hq_unsubscribe_basic_qot":
                # 取消订阅基础行情推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_basic_qot()
            elif method_name == "hq_unsubscribe_ticker":
                # 取消订阅逐笔推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_ticker()
            elif method_name == "hq_unsubscribe_broker":
                # 取消订阅买卖经纪推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_broker()
            elif method_name == "hq_unsubscribe_order_book":
                # 取消订阅买卖档推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_order_book()
            elif method_name == "hq_unsubscribe_total_view_book":
                # 取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_total_view_book()
            elif method_name == "hq_unsubscribe_arca_Book":
                # 取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                quote_demo.hq_unsubscribe_arca_Book()
            elif method_name == "stop":
                # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
                quote_demo.stop()
                exit(1)
            else:
                print("接口名输入有误，请参考提示重新输入！")
    else:
        # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
        quote_demo.stop()
        exit(1)
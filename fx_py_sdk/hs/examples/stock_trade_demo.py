# -*- coding: utf-8 -*-
import threading
import time

from hs.api.trading_api import TradingAPI
from hs.common.common_utils import now_to_str
from hs.common.protobuf_utils import parse_payload
from hs.api.constant import ExchangeType, EntrustBS, EntrustType, ModelResult, EntrustEX, SessionType, CondTrackType


class StockTradeDemo(object):
    """股票交易类接口独立Demo程序"""

    def __init__(self, **kwargs):
        self._trading_api = TradingAPI(**kwargs)
        self.timer_threading = None

    def check_alive(self) -> bool:
        """检查Trading API是否正常连接状态"""
        return self._trading_api.is_alive()

    def get_token(self):
        """获取平台Token"""
        return self._trading_api.get_token()
    
    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        self._trading_api.start(p_token)
        return self

    def add_notify_callback(self):
        """增加消息推送回调函数"""
        self._trading_api.add_notify_callback(self.notify_callback)
        return self

    def entrust(self) -> ModelResult:
        """普通订单委托下单"""
        model_result = self._trading_api.entrust(iceberg_display_size="0",
                                                 session_type=SessionType.GENERAL_ORDER_NO,
                                                 exchange=EntrustEX.ARCA,
                                                 exchange_type=ExchangeType.K,
                                                 entrust_bs=EntrustBS.BUY,
                                                 entrust_type=EntrustType.LIMIT, # 普通订单
                                                 stock_code="00700.HK",
                                                 entrust_amount="100",
                                                 entrust_price="561.500")
        if model_result.is_success:
            print(f"entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust(self, entrust_id: str) -> ModelResult:
        """普通订单改单"""
        model_result = self._trading_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="561.500")
        if model_result.is_success:
            print(f"change_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust(self, entrust_id: str) -> ModelResult:
        """普通撤单"""
        model_result = self._trading_api.cancel_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="561.500")
        if model_result.is_success:
            print(f"cancel_entrust_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def entrust_cond(self) -> ModelResult:
        """条件单委托下单"""
        model_result = self._trading_api.entrust(iceberg_display_size="",
                                                 session_type=SessionType.COND_ORDER_DEFAULT, # 只支持盘中
                                                 exchange="",
                                                 exchange_type=ExchangeType.K,
                                                 entrust_bs=EntrustBS.SELL, # 卖出
                                                 entrust_type=EntrustType.COND_STOP_PROFIT_POINT, # 条件单-止盈限价单
                                                 stock_code="00700.HK",
                                                 entrust_amount="100", # 委托数量
                                                 entrust_price="515", # 委托下单指定价格，当条件触发时的委托下单价格
                                                 valid_days="10", # 有效天数
                                                 cond_value="511", # 止盈价格, 可能值：价格、价差、百分比数字
                                                 cond_track_type="") # 如果为跟踪订单该值必填, 1百分比、2价差, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def change_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单改单"""
        model_result = self._trading_api.change_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="100",
                                                        entrust_price="535", # 委托下单指定价格，当条件触发时的委托下单价格
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT, # 传原下单委托类型，不允许修改
                                                        session_type=SessionType.COND_ORDER_HK_DEFAULT_HIDDEN, # 修改为 '支持盘中及暗盘'
                                                        valid_days="25", # 有效期修改为15天
                                                        cond_value="533", # 价格条件修改为533
                                                        cond_track_type="") # 不是跟踪订单，该值为空, hs.api.constant.CondTrackType
        if model_result.is_success:
            print(f"change_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to change entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result

    def cancel_entrust_cond(self, entrust_id: str) -> ModelResult:
        """条件单撤单"""
        model_result = self._trading_api.cancel_entrust(exchange_type=ExchangeType.K,
                                                        entrust_id=entrust_id,
                                                        stock_code="00700.HK",
                                                        entrust_amount="",
                                                        entrust_price="",
                                                        entrust_type=EntrustType.COND_STOP_PROFIT_POINT) # 传原下单委托类型，不允许修改
        if model_result.is_success:
            print(f"cancel_entrust_cond_id：{model_result.get_model()}")
        else:
            print(f"fail to cancel entrust cond, code: {model_result.code}, msg: {model_result.msg}")
        return model_result
    
    def query_holds_list(self):
        """查询持仓股票列表"""
        model_result = self._trading_api.query_holds_list(exchange_type=ExchangeType.K)
        if model_result.is_success:
            holds_list = model_result.get_model()
            if len(holds_list) < 0:
                print(f"在当前交易市场没有持仓！")
            else:
                for holds in holds_list:
                    print(f"持仓股票名称：{holds.stockName}, 详细信息：{holds}")
        else:
            print(f"fail to query_holds_list，code：{model_result.code}, msg：{model_result.msg}")
        return model_result.get_model()

    def query_buy_amount(self):
        """获取最大可买数量"""
        model_result = self._trading_api.query_buy_amount(exchange_type=ExchangeType.K,
                                                          stock_code="00700.HK",
                                                          entrust_price="510.00")
        if model_result.is_success:
            print(f"最大可买数量：{model_result.get_model()}")
        else:
            print(f"fail to query_buy_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_sell_amount(self):
        """获取最大可卖数量"""
        model_result = self._trading_api.query_sell_amount(exchange_type=ExchangeType.K, stock_code="00700.HK")
        if model_result.is_success:
            print(f"最大可卖数量：{model_result.get_model()}")
        else:
            print(f"fail to query_sell_amount, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_margin_fund_info(self):
        """查询客户资金信息"""
        model_result = self._trading_api.query_margin_fund_info(exchange_type=ExchangeType.K)
        if model_result.is_success:
            print(f"客户资金信息：{model_result.get_model()}")
        else:
            print(f"fail to query_margin_fund_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_entrust_list(self, entrust_id: list):
        """查询客户当日委托信息"""
        model_result = self._trading_api.query_real_entrust_list(exchange_type=ExchangeType.K,
                                                                 query_count=20,
                                                                 query_param_str="0",
                                                                 entrust_ids = entrust_id)
        if model_result.is_success:
            print(f"客户当日委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_entrust_list(self):
        """查询客户历史委托信息"""
        model_result = self._trading_api.query_history_entrust_list(exchange_type=ExchangeType.K,
                                                                    query_count=20,
                                                                    query_param_str="0",
                                                                    start_date="20201010",
                                                                    end_date=now_to_str())
        if model_result.is_success:
            print(f"查询客户历史委托信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_entrust_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_deliver_list(self):
        """查询客户当日成交信息"""
        model_result = self._trading_api.query_real_deliver_list(exchange_type=ExchangeType.K,
                                                                 query_count=20,
                                                                 query_param_str="0")
        if model_result.is_success:
            print(f"客户当日成交信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_deliver_list(self):
        """查询客户历史成交信息"""
        model_result = self._trading_api.query_history_deliver_list(exchange_type=ExchangeType.K,
                                                                    query_count=20,
                                                                    query_param_str="0",
                                                                    start_date="20201210",
                                                                    end_date=now_to_str())
        if model_result.is_success:
            print(f"客户历史成交信息列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_deliver_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_real_fund_jour_list(self):
        """查询客户当日资金流水列表"""
        model_result = self._trading_api.query_real_fund_jour_list(exchange_type=ExchangeType.K,
                                                                   query_count=20,
                                                                   query_param_str="0")
        if model_result.is_success:
            print(f"客户当日资金流水列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_fund_jour_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_history_fund_jour_list(self):
        """查询客户历史资金流水列表"""
        model_result = self._trading_api.query_history_fund_jour_list(exchange_type=ExchangeType.K,
                                                                      query_count=20,
                                                                      query_param_str="0",
                                                                      start_date="20201210",
                                                                      end_date=now_to_str())
        if model_result.is_success:
            print(f"客户历史资金流水列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_fund_jour_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_before_and_after_support(self):
        """查询是否支持盘前盘后交易"""
        model_result = self._trading_api.query_before_and_after_support(stock_code="TSLA",
                                                                        exchange_type=ExchangeType.P)
        if model_result.is_success:
            print(f"是否支持盘前盘后交易：{model_result.get_model()}")
        else:
            print(f"fail to query_before_and_after_support, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_max_available_asset(self):
        """查询最大可用资产"""
        model_result = self._trading_api.query_max_available_asset(exchange_type=ExchangeType.P,
                                                                   stock_code="AAPL",
                                                                   entrust_price="142",
                                                                   entrust_type=EntrustType.MARKET)
        if model_result.is_success:
            print(f"查询最大可用资产：{model_result.get_model()}")
        else:
            print(f"fail to query_max_available_asset, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def query_stock_short_info(self):
        """查询股票沽空信息"""
        model_result = self._trading_api.query_stock_short_info(exchange_type=ExchangeType.P,
                                                                stock_code="AAPL")
        if model_result.is_success:
            print(f"查询股票沽空信息：{model_result.get_model()}")
        else:
            print(f"fail to query_stock_short_info, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()
    
    def query_real_cond_order_list(self):
        """查询当日条件单列表"""
        model_result = self._trading_api.query_real_cond_order_list(exchange_type=ExchangeType.K,
                                                                    stock_code="",
                                                                    page_no=1,
                                                                    page_size=20)
        if model_result.is_success:
            print(f"查询当日条件单列表：{model_result.get_model()}")
        else:
            print(f"fail to query_real_cond_order_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()
    
    def query_history_cond_order_list(self):
        """查询历史条件单列表"""
        model_result = self._trading_api.query_history_cond_order_list(start_time="2021-01-01 19:21:21",
                                                                       end_time="2021-01-02 19:21:21",
                                                                       exchange_type=ExchangeType.K,
                                                                       stock_code="",
                                                                       page_no=1,
                                                                       page_size=20)
        if model_result.is_success:
            print(f"查询历史条件单列表：{model_result.get_model()}")
        else:
            print(f"fail to query_history_cond_order_list, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()
    
    def trade_subscribe(self):
        """订阅交易推送消息"""
        model_result = self._trading_api.trade_subscribe()
        if model_result.is_success:
            print(f"订阅交易推送消息：{model_result.get_model()}")
        else:
            print(f"fail to trade_subscribe, code: {model_result.code}, msg: {model_result.msg}")
        return model_result.get_model()

    def trade_unsubscribe(self):
        """取消订阅交易推送消息"""
        model_result = self._trading_api.trade_unsubscribe()
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
        self.query_holds_list()
    
    def stop(self):
        """退出业务API上下文环境"""
        self.timer_threading.cancel()
        self._trading_api.stop()


if __name__ == '__main__':
    # 1、配置启动参数
    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                            "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                            "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ENCRYPT_RSA_PRIVATEKEY = "MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBANd2tAKwgShHikGR5iYkuuwIdtSL+ZQxYi+5j9YxNewZ43iEVCBqZdPeQAYUEvWjFf0vkzCULVUxBESd1zErHD7yEQP8H4tKKIGf9q5iRwDIetKkij95wgfsDQ90CyCFZnjcho6c9sZ7RUkJFspp3kLZw19FkTYNPPeGxv/2Qqa/AgMBAAECgYEAz06WxD+vBWJP0+bc2bZdYtyB+N70s3EQV3riueN/TjtacYpgpw+4CbG9SBvoYg8YCRLNO+BV/bG7uYlkkxo3gVQJ5W6XZruwGtovL9FCHaco0tbgrHzDqLCCh/z4fqiUFvUowYQzph8Kgl/a2L58e3bDiqSY+Si67Sm1W6qycoECQQD5NFYa7nVZ+da9Q6idDja+Is4st+o08ZrwpN0VGmCMqRqDKgykGC4VNmM5g1Idx/unU1jAwnOJfgl2cNrzS65lAkEA3VbTtz3cX22FO6a0cOX41mp9a9rk1jCbR8CR/cLXnK7R3z3BYjXsDccMWpkFenInShYeIWgzNceLoihDJuTsUwJBAJmIlhgnnCNgGt4mZibFEBMarH2+ncwaooPqfs82ng9rTAtNh9Y9k368MGvJrXjtsezIG+E+rCIkhb30D+FfWkUCQQCNZemMt1UwFVw29lFxikjEWXVUUJs+BgE8/lWFglKRgtEKR35iCkaJqq5Gtljcl05oMub+un10jsyyQ/xaPYaHAkEA7iFG9jQxDJe222uI5TChpoPlowWsmv+7bJ/OrzGJ3W+1XPd9bEjmFb9+AzxKH03NMbSiL+37+4yo1xsihnqnoQ=="

    params = {
        "rsa_public_key": ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://openapi-daily.hstong.com",  # 生产环境domain为：https://openapi.hstong.com
        "login_country_code": "CHN", # 如果为香港或美国地区手机号，需要修改为对应区域编码，区域编码查询：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8
        "login_mobile": "13945615532", # 登录账号无需加区号
        "login_passwd": "D-97N4",
        "trading_passwd": "811490",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 2、初始化交易API对象、增加消息推送回调函数
    trade_demo = StockTradeDemo(**params).add_notify_callback()
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
            print("###### 接口名: query_margin_fund_info，            接口描述: 交易接口-查询客户资金信息									######")
            print("###### 接口名: query_holds_list，                  接口描述: 交易接口-查询持仓股票列表									######")
            print("###### 接口名: query_buy_amount，                  接口描述: 交易接口-获取最大可买数量									######")
            print("###### 接口名: query_sell_amount，                 接口描述: 交易接口-获取最大可卖数量									######")
            print("###### 接口名: query_real_fund_jour_list，         接口描述: 交易接口-查询客户当日资金流水列表							######")
            print("###### 接口名: query_history_fund_jour_list，      接口描述: 交易接口-查询客户历史资金流水列表							######")
            print("###### 接口名: entrust，                           接口描述: 订单接口-委托/改单/撤单										######")
            print("###### 接口名: entrust_cond，                      接口描述: 订单接口-条件单委托/改单/撤单								######")
            print("###### 接口名: query_real_entrust_list，           接口描述: 订单接口-查询客户当日委托信息								######")
            print("###### 接口名: query_history_entrust_list，        接口描述: 订单接口-查询客户历史委托信息								######")
            print("###### 接口名: query_real_deliver_list，           接口描述: 订单接口-查询客户当日成交信息								######")
            print("###### 接口名: query_history_deliver_list，        接口描述: 订单接口-查询客户历史成交信息								######")
            print("###### 接口名: query_before_and_after_support，    接口描述: 订单接口-查询是否支持盘前盘后交易						    ######")
            print("###### 接口名: query_max_available_asset，         接口描述: 订单接口-查询最大可用资产						            ######")
            print("###### 接口名: query_stock_short_info，            接口描述: 订单接口-查询股票沽空信息       						    ######")
            print("###### 接口名: query_real_cond_order_list，        接口描述: 订单接口-查询当日条件单列表      						    ######")
            print("###### 接口名: query_history_cond_order_list，     接口描述: 订单接口-查询历史条件单列表       						    ######")
            print("###### 接口名: trade_subscribe，                   接口描述: 订单接口-订阅交易推送消息									######")
            print("###### 接口名: trade_unsubscribe，                 接口描述: 订单接口-取消订阅交易推送消息								######")
            print("###### 接口名: stop，                              接口描述: ！！！程序退出，该函数将退出交易登录，并断开TCP链接！！！	######")
            method_name = input("请输入需要查看的接口名: ")
    
            if method_name == "query_margin_fund_info":
                # 交易接口-查询客户资金信息
                trade_demo.query_margin_fund_info()
            elif method_name == "query_holds_list":
                # 查询持仓股票列表
                trade_demo.query_holds_list()
            elif method_name == "query_buy_amount":
                # 获取最大可买数量
                trade_demo.query_buy_amount()
            elif method_name == "query_sell_amount":
                # 获取最大可卖数量
                trade_demo.query_sell_amount()
            elif method_name == "query_real_fund_jour_list":
                # 查询客户当日资金流水列表
                trade_demo.query_real_fund_jour_list()
            elif method_name == "query_history_fund_jour_list":
                # 查询客户历史资金流水列表
                trade_demo.query_history_fund_jour_list()
            elif method_name == "entrust":
                # 委托下单
                entrustResult = trade_demo.entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = trade_demo.change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # trade_demo.cancel_entrust(entrustResult.get_model())
            elif method_name == "entrust_cond":
                # 条件单委托下单
                entrustResult = trade_demo.entrust_cond()
                time.sleep(1)
                # 条件单改单（需要时才改单）
                # result = trade_demo.change_entrust_cond(entrustResult.get_model())
                time.sleep(1)
                # 条件单撤单（需要时才撤单）
                # trade_demo.cancel_entrust_cond(entrustResult.get_model())
            elif method_name == "query_real_entrust_list":
                # 查询客户当日委托信息
                if entrustResult is not None:
                    entrustIds = list()
                    entrustIds.append(entrustResult.get_model())
                    trade_demo.query_real_entrust_list(entrustIds)
                else:
                    trade_demo.query_real_entrust_list(list())
            elif method_name == "query_history_entrust_list":
                # 查询客户历史委托信息
                trade_demo.query_history_entrust_list()
            elif method_name == "query_real_deliver_list":
                # 查询客户当日成交信息
                trade_demo.query_real_deliver_list()
            elif method_name == "query_history_deliver_list":
                # 查询客户历史成交信息
                trade_demo.query_history_deliver_list()
            elif method_name == "query_before_and_after_support":
                # 查询是否支持盘前盘后交易
                trade_demo.query_before_and_after_support()
            elif method_name == "query_max_available_asset":
                # 查询最大可用资产
                trade_demo.query_max_available_asset()
            elif method_name == "query_stock_short_info":
                # 查询股票沽空信息
                trade_demo.query_stock_short_info()
            elif method_name == "query_real_cond_order_list":
                # 查询当日条件单列表
                trade_demo.query_real_cond_order_list()
            elif method_name == "query_history_cond_order_list":
                # 查询历史条件单列表
                trade_demo.query_history_cond_order_list()
            elif method_name == "trade_subscribe":
                # 订阅交易推送消息（需要时才使用）
                trade_demo.trade_subscribe()
            elif method_name == "trade_unsubscribe":
                # 取消订阅交易推送消息（需要时才使用）
                trade_demo.trade_unsubscribe()
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
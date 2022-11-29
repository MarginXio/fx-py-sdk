# -*- coding: utf-8 -*-
import threading
from hs.examples.stock_quote_demo import StockQuoteDemo
from hs.examples.stock_trade_demo import StockTradeDemo


# 定义异步执行的逻辑
def async_call_trading(trade_demo: StockTradeDemo=None):
    # 2、初始化交易API对象、增加消息推送回调函数、启动交易API上下文
    if not trade_demo:
        print(f"async_call_trading trade_demo is empty, exit.")
        exit(1)
    # 3、Call当前OpenAPI所有支持的业务方法
    # 检查连接状态（非必需）
    trade_demo.check_alive()
    # 委托下单
    result = trade_demo.entrust()
    # 改单（需要时才改单）
    # result = trade_demo.change_entrust(result.get_model())
    # 撤单（需要时才撤单）
    # trade_demo.cancel_entrust(result.get_model())
    # 查询持仓股票列表
    trade_demo.query_holds_list()
    # 获取最大可买数量
    trade_demo.query_buy_amount()
    # 获取最大可卖数量
    trade_demo.query_sell_amount()
    # 查询客户资金信息
    trade_demo.query_margin_fund_info()
    # 查询客户当日委托信息
    trade_demo.query_real_entrust_list(entrust_id=[])
    # 查询客户历史委托信息
    trade_demo.query_history_entrust_list()
    # 查询客户当日成交信息
    trade_demo.query_real_deliver_list()
    # 查询客户历史成交信息
    trade_demo.query_history_deliver_list()
    # 查询客户当日资金流水列表
    trade_demo.query_real_fund_jour_list()
    # 查询客户历史资金流水列表
    trade_demo.query_history_fund_jour_list()
    # 订阅交易推送消息
    trade_demo.trade_subscribe()
    # 取消订阅交易推送消息
    # trade_demo.trade_unsubscribe()


def async_call_quote(quote_demo: StockQuoteDemo=None,
                     call_hq: bool = True,
                     subscribe_hq: bool = True):
    # 初始化行情API对象、增加消息推送回调函数、启动行情API上下文
    if not quote_demo:
        print(f"async_call_quote quote_demo is empty, exit.")
        exit(1)
    # 3、Call当前OpenAPI所有支持的业务方法
    # 检查连接状态（非必需）
    quote_demo.check_alive()
    if call_hq:
        # 批量查询股票基础报价
        quote_demo.query_hq_basic_qot()
        # 查询买卖经纪摆盘
        quote_demo.query_hq_broker()
        # 查询买卖档
        quote_demo.query_order_book()
        # 查询最近多少条的逐笔列表
        quote_demo.query_hq_ticker()
        # 查询K线数据
        quote_demo.query_hq_kline()
        # 查询分时数据
        quote_demo.query_hq_time_share()
    if subscribe_hq:
        # 订阅基础行情推送消息（需要时才使用）
        quote_demo.hq_subscribe_basic_qot()
        # 订阅逐笔推送消息（需要时才使用）
        quote_demo.hq_subscribe_ticker()
        # 订阅买卖经纪推送消息（需要时才使用）
        quote_demo.hq_subscribe_broker()
        # 订阅买卖档推送消息（需要时才使用）
        quote_demo.hq_subscribe_order_book()
        # 取消订阅基础行情推送消息（需要时才使用）
        # quote_demo.hq_unsubscribe_basic_qot()
        # 取消订阅逐笔推送消息（需要时才使用）
        # quote_demo.hq_unsubscribe_ticker()
        # 取消订阅买卖经纪推送消息（需要时才使用）
        # quote_demo.hq_unsubscribe_broker()
        # 取消订阅买卖档推送消息（需要时才使用）
        # quote_demo.hq_unsubscribe_order_book()
    # 最后，如有需要可以退出业务API上下文，以释放业务对象
    # quote_demo.stop()


def multiple_async_call_quote(num_times: int = 1):
    quote_demo = StockQuoteDemo(**params).add_notify_callback()
    token = quote_demo.get_token()
    quote_demo.start(token)
    
    async_call_quote(quote_demo, call_hq=False, subscribe_hq=True)
    # 重复调用接口次数：num_times
    for i in range(num_times):
        print(f"call quote num_times: {i}")
        async_call_quote(quote_demo, call_hq=True, subscribe_hq=False)


def multiple_async_call_trading(num_times: int = 1):
    trade_demo = StockTradeDemo(**params).add_notify_callback()
    token = trade_demo.get_token()
    trade_demo.start(token)
    # 重复调用接口次数：num_times
    for i in range(num_times):
        print(f"call trading num_times: {i}")
        async_call_trading(trade_demo)


def async_call_trading_and_quote():
    async_call_trading()
    async_call_quote()


if __name__ == '__main__':
    # 1、配置启动参数
    # 平台公钥，请求的时候使用
    ENCRYPT_RSA_PUBLICKEY = "<<your encrypt rsa public key>>"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ENCRYPT_RSA_PRIVATEKEY = "<<your encrypt rsa private key>>"
    params = {
        "rsa_public_key": ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://openapi-daily.hstong.com",  # 生产环境domain为：https://openapi.hstong.com
        "login_country_code": "CHN",
        "login_mobile": "<<your login mobile>>",
        "login_passwd": "<<your login password>>",
        "trading_passwd": "<<your trading password>>",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    
    # # 异步执行多次交易接口
    threading.Thread(target=multiple_async_call_trading, args=(1000,)).start()
    print("async send trading command already!")

    # 异步执行多次行情接口
    threading.Thread(target=multiple_async_call_quote, args=(1000,)).start()  # 1000次
    print("async send quote command already!")

    # # 异步执行1次：交易和行情接口
    threading.Thread(target=async_call_trading_and_quote).start()
    print("async send trading and quote command already!")

    print("finished call thread...")


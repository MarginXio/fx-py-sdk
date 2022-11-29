# -*- coding: utf-8 -*-
from dataclasses import dataclass


class StatusCode(object):
    """系统/业务状态码"""
    RET_OK = "0000"  # 处理成功
    INVOKE_TIME_OUT = "1015"  # 接口调用超时


class ServerKey(object):
    """获取长连接IP端口的Key"""
    HQ_SERVER_KEY = "hqServer"
    TRADING_SERVER_KEY = "tradeServer"
    

@dataclass
class ModelResult:
    """API统一返回的模型对象"""
    is_success: bool = False
    code: str = ""
    msg: str = ""
    data: object = None

    def with_model(self, model):
        self.is_success = True
        self.data = model
        return self

    def get_model(self):
        return self.data

    def with_error(self, error_code, error_msg):
        self.is_success = False
        self.code = error_code
        self.msg = error_msg
        return self

    def to_str(self) -> str:
        return "{" + f"is_success: {self.is_success}, code: \"{self.code}\", msg: \"{self.msg}\", data: {self.data}" + "}"


@dataclass
class SecurityParam(object):
    """股票信息的实体类，用于构建行情查询接口的参数"""
    data_type: int  # 股票类型 参考常量类：DataType
    stock_code: str  # 股票代码


class ClientType(object):
    """客户端类型"""
    INTERNET = 0  # internet


class QueryType(object):
    """查询类型"""
    DEFAULT = 0  # 默认
    MARGIN = 1  # Margin


class EntrustBS(object):
    """买卖方向"""
    BUY = "1"  # 多头开仓
    SELL = "2"  # 多头平仓
    SHORT_SELL = "3"  # 空头平仓
    SHORT_BUY = "4"  # 空头开仓


class ExchangeType(object):
    """交易类型"""
    K = "K"  # 港股
    P = "P"  # 美股
    V = "v"  # 深股通
    T = "t"  # 泸股通


class EntrustType(object):
    """
    委托类型
    港股：'0'-竞价限价、'1'-竞价、'2'-增强限价盘、'3'-限价盘、'4'-特别限价盘、'6'-暗盘
    美股：'3'-限价盘、'5'-市价盘、'8'-冰山市价、'9'-冰山限价、'10'-隐藏市价、'11'-隐藏限价
    A股：'3'-限价盘
    条件单：'31'-止盈限价单、'32'-止盈市价单(美股)、'33'-止损限价单、'34'-止损市价单(美股)、'35'-追踪止损限价单、'36'-追踪止损市价单(美股)
    """
    AUCTION_LIMIT = "0"  # 竞价限价
    AUCTION = "1"  # 竞价
    ENHANCED_LIMIT = "2"  # 增强限价盘
    LIMIT = "3"  # 限价盘
    SPECIAL_LIMIT = "4"  # 特别限价盘
    MARKET = "5"  # 市价盘
    DARK = "6"  # 暗盘
    ICEBERG_MARKET = "8"  # 冰山市价
    ICEBERG_LIMIT = "9"  # 冰山限价
    HIDE_MARKET = "10"  # 隐藏市价
    HIDE_LIMIT = "11"  # 隐藏限价
    
    COND_STOP_PROFIT_POINT = "31" # 止盈限价单
    COND_STOP_PROFIT_MARKET = "32" # 止盈市价单
    COND_STOP_LOSS_POINT = "33" # 止损限价单
    COND_STOP_LOSS_MARKET = "34" # 止损市价单
    COND_TRACK_STOP_LOSS_POINT = "35" # 追踪止损限价单
    COND_TRACK_STOP_LOSS_MARKET = "36" # 追踪止损市价单


class SessionType(object):
    """"
    盘前盘后交易
    0:否 1:是 3:只支持盘中 5:港股支持盘中及暗盘 7:美股支持盘中及盘前盘后
    """
    GENERAL_ORDER_NO = "0" # 否
    GENERAL_ORDER_YES = "1" # 是
    
    COND_ORDER_DEFAULT = "3" # 只支持盘中
    COND_ORDER_HK_DEFAULT_HIDDEN = "5" # 港股支持盘中及暗盘
    COND_ORDER_US_DEFAULT_BEFOREAFTER = "7" # 美股支持盘中及盘前盘后


class CondTrackType(object):
    """
    条件跟踪类型 1百分比、2价差、3价格
    """
    PERCENTAGE = "1" # 百分比
    PRICE = "2" # 价差
    FIX_PRICE = "3" # 价格


class CondStatus(object):
    """
    条件单状态  1:待触发 2:已触发 3:暂停 4:已过期 5:已删除 6:错误 8:止盈止损单失效 9:除权除息失效
    """
    PENDING = 1 # 待触发
    FINISH = 2 # 已触发
    PAUSE = 3 # 暂停
    EXPIRE = 4 # 已过期
    DELETE = 5 # 已删除
    ERROR = 6 # 错误
    INVALID_PROFITLOSS = 8 # 止盈止损失效
    INVALID_DIVIDEND = 9 # 除权除息失效
    RECALL = 10 # 撤回


class EntrustEX(object):
    """交易所"""
    SMART = "SMART"
    AMEX = "AMEX"
    ARCA = "ARCA"
    BATS = "BATS"
    BEX = "BEX"
    BYX = "BYX"
    CBOE = "CBOE"
    CHX = "CHX"
    DRCTEDGE = "DRCTEDGE"
    EDGEA = "EDGEA"
    EDGX = "EDGX"
    IBKRTS = "IBKRTS"
    IEX = "IEX"
    ISE = "ISE"
    ISLAND = "ISLAND"
    LTSE = "LTSE"
    MEMX = "MEMX"
    NYSE = "NYSE"
    NYSENAT = "NYSENAT"
    PEARL = "PEARL"
    PHLX = "PHLX"
    PSX = "PSX"


class DataType(object):
    """股票类型"""
    HK_STOCK = 10000  # 港股股票
    HK_INDEX = 10001  # 港股指数
    HK_ETF = 10002  # 港股ETF
    HK_WARRANT = 10003  # 港股窝轮
    HK_CBBC = 10004  # 港股牛熊证
    HK_BOND = 10005  # 港股债券
    HK_INDUSTRY = 10006  # 港股行业板块
    HK_CONCEPT = 10007  # 港股概念板块
    HK_FUTURES = 10009  # 衍生品期货
    HK_INDEX_FUTURES = 10010  # 香港指数期货
    HK_STOCK_FUTURES = 10011  # 港股股票期货
    HK_DIVIDEND_POINT_INDEX_FUTURES = 10012  # 港股恒指股息期货
    HK_RMB_CURRENCY_FUTURES = 10013  # 港股人民币货币期货
    HK_CESC_INDEX_FUTURES = 10014  # 港股中华交易服务期货
    HK_VOLATILITY_INDEX_FUTURES = 10015  # 恒指波幅指数期货
    HK_INLINE = 10016  # 界内证
    US_STOCK = 20000  # 美股股票
    US_INDEX = 20001  # 美股指数
    US_ETF = 20002  # 美股ETF
    US_OPTION = 20003  # 美股期权
    US_INDUSTRY = 20006  # 美股行业板块
    US_CONCEPT = 20007  # 美股概念板块
    ASHARE_STOCK = 30000  # A股股票
    ASHARE_INDEX = 30001  # A股指数
    ASHARE_ETF = 30002  # A股ETF
    ASHARE_INDUSTRY = 30006  # A股行业
    ASHARE_CONCEPT = 30007  # A股概念
    ASHARE_KSH = 30008  # A股科创板


class CycType(object):
    """K线类型"""
    DAY = 2  # 日线
    WEEK = 3  # 周线
    MONTH = 4  # 月线
    MINUTE1 = 5  # 1分钟
    MINUTE5 = 6  # 5分钟
    MINUTE15 = 7  # 15分钟
    MINUTE30 = 8  # 30分钟
    MINUTE60 = 9  # 60分钟
    MINUTE120 = 10  # 120分钟
    QUARTER = 11  # 季度线
    YEAR = 12  # 年度线
    DAY5 = 13  # 五日
    MINUTE3 = 14  # 3分钟


class ExRightFlag(object):
    """复权类型"""
    BFQ = 0  # 不复权
    QFQ = 1  # 前复权
    HFQ = 2  # 后复权


class Direction(object):
    """查询方向"""
    QUERY_LEFT = 0  # 往左查询
    QUERY_RIGHT = 1  # 往右查询


class HQSubscribeTopicId(object):
    """订阅/取消订阅行情推送的TopicId"""
    BASIC_QOT = 11  # 基础行情推送
    TICKER = 14  # 逐笔推送
    BROKER = 16  # 买卖经纪推送
    ORDER_BOOK = 17  # 买卖档推送
    TOTALVIEW_BOOK = 26  # TOTALVIEW
    ARCA_BOOK = 25  # ARCA


class MktTmType(object):
    """
    交易时段
    美股：盘前：-1 盘中：1 盘后：-2
    """
    PRE_MARKET = -1  # 盘前：-1
    MID_SESSION = 1  # 盘中：1
    AFTER_HOURS = -2  # 盘后：-2


class DepthBookType(object):
    """
    2 3 totalview arcabook
    """
    TOTAL_VIEW = 2  # totalview
    ARCA_BOOK = 3  # arcabook


class FuturesEntrustType(object):
    """
    期货委托类型
    0 限价单、1 竞价单、2 市价单、3 条件单
    """
    LIMIT = "0"  # 限价单
    AUCTION = "1"  # 竞价单
    MARKET = "2"  # 市价单
    OPTION = "3"  # 条件单


class FuturesValidTimeType(object):
    """
    期货委托生效类型
    0 即日有效、1 成交并取消、2 全额或取消、3 到期日有效、4 指定日期有效
    """
    VALID_TODAY = "0"  # 即日有效
    DEAL_AND_CANCEL = "1"  # 成交并取消
    FULL_OR_CANCEL = "2"  # 全额或取消
    VALID_ON_EXPIRY_DATE = "3"  # 到期日有效
    VALID_ON_SPECIFIED_DATE = "4"  # 指定日期有效

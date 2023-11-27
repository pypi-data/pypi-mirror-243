import sys
from datetime import datetime
from time import sleep
from typing import Dict, List, Tuple, Set, Optional, Callable
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from numpy import ndarray
from pandas import DataFrame

from vnpy.trader.setting import SETTINGS
from vnpy.trader.object import BarData, TickData, HistoryRequest
from vnpy.trader.utility import round_to, ZoneInfo,get_folder_path, ZoneInfo
from vnpy.event import EventEngine,EVENT_TIMER
from vnpy.trader.constant import (
    Direction,
    Offset,
    Exchange,
    OrderType,
    Product,
    Status,
    OptionType,
    Interval
)
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
    BarData, 
    HistoryRequest
)

from vnpy.trader.datafeed import BaseDatafeed
from icetcore import (TCoreAPI,
                    QuoteEvent,
                    TradeEvent,
                    BarType,
                    SymbolType,
                    GreeksType,
                    OrderStruct,
                    OrderSide,
                    TimeInForce,
                    #OrderType,
                    PositionEffect)





# 委托状态映射



Status.FROZEN="锁券成功"
STATUS_ICE2VT: Dict[int, Status] = {
    0: Status.NOTTRADED,
    1: Status.NOTTRADED,
    2: Status.NOTTRADED,
    3: Status.ALLTRADED,
    4: Status.PARTTRADED,
    5: Status.PARTTRADED,
    6: Status.NOTTRADED,
    7: Status.PARTTRADED,
    8: Status.CANCELLED,
    9: Status.NOTTRADED,
    10: Status.REJECTED,
    11: Status.SUBMITTING,
    12: Status.SUBMITTING,
    13: Status.NOTTRADED,
    14: Status.SUBMITTING,
    15: Status.SUBMITTING,
    16: Status.SUBMITTING,
    17: Status.FROZEN,
    18: Status.REJECTED,
    19: Status.SUBMITTING,
    20: Status.SUBMITTING,
    21: Status.REJECTED,
    22: Status.SUBMITTING,
    23: Status.SUBMITTING,
    24: Status.SUBMITTING,
    31: Status.SUBMITTING
}

# 多空方向映射
DIRECTION_VT2ICE: Dict[Direction, int] = {
    Direction.LONG: 1,
    Direction.SHORT:2
}
DIRECTION_ICE2VT: Dict[int, Direction] = {v: k for k, v in DIRECTION_VT2ICE.items()}
# DIRECTION_ICE2VT[1] = Direction.LONG
# DIRECTION_ICE2VT[2] = Direction.SHORT

# 委托类型映射
OrderType.STOPLIMIT="停损限价"
ORDERTYPE_VT2ICE: Dict[OrderType, tuple] = {
    OrderType.LIMIT: (2, 1),
    OrderType.MARKET: (1, 2),
    OrderType.FAK: (2, 2),
    OrderType.FOK: (2, 3),
    OrderType.STOP: (3, 2),
    OrderType.STOPLIMIT: (4, 1)
}
ORDERTYPE_ICE2VT: Dict[Tuple, OrderType] = {#{v: k for k, v in ORDERTYPE_VT2ICE.items()}
    (1, 2): OrderType.MARKET ,
    (1, 1): OrderType.MARKET ,
    (2, 1): OrderType.LIMIT,
    (2, 2): OrderType.FAK,
    (2, 3): OrderType.FOK,
    (22, 2): OrderType.FAK,
    (3, 1): OrderType.STOP,
    (3, 2): OrderType.STOP,
    (5, 2): OrderType.STOP,
    (5, 1): OrderType.STOP,
    (6, 1): OrderType.STOPLIMIT,
    (6, 2): OrderType.STOPLIMIT,
    (4, 2): OrderType.STOPLIMIT,
    (4, 1): OrderType.STOPLIMIT
}
# 开平方向映射
Offset.COVEREDCALLWRITING="备兑开仓"
Offset.COVEREDCALLCLOSE="备兑平仓"
OFFSET_VT2ICE: Dict[Offset, int] = {
    Offset.OPEN: 0,
    Offset.CLOSE: 1,
    Offset.CLOSETODAY: 2,
    Offset.CLOSEYESTERDAY: 3,
    Offset.NONE: 4,
    Offset.COVEREDCALLWRITING:10,
    Offset.COVEREDCALLCLOSE:11
}
OFFSET_ICE2VT: Dict[int, Offset] = {v: k for k, v in OFFSET_VT2ICE.items()}

# 交易所映射
EXCHANGE_ICE2VT: Dict[str, Exchange] = {
    "CFFEX": Exchange.CFFEX,
    "SHFE": Exchange.SHFE,
    "CZCE": Exchange.CZCE,
    "DCE": Exchange.DCE,
    "INE": Exchange.INE,
    "GFEX": Exchange.GFEX,
    "SSE":Exchange.SSE,
    "SZSE":Exchange.SZSE,
    "CME":Exchange.CME,
    "CBOT":Exchange.CBOT,
    "EUREX":Exchange.EUNX,
    "ENXT_PAR":Exchange.EUNX,
    "LIFFE":Exchange.NYSE,
    "LME":Exchange.LME,
    "ICE":Exchange.ICE,
    "NYBOT":Exchange.NYMEX,
    "SGXQ":Exchange.SGX,
    "TOCOM":Exchange.TOCOM,
    "OSE":Exchange.TOCOM,
    "TSE":Exchange.TSE,
    "BMD":Exchange.BMD,
    "HKEX":Exchange.HKFE,
    "CFE":Exchange.CFE
}
EXCHANGE_VT2ICE: Dict[Exchange, str] = {v: k for k, v in EXCHANGE_ICE2VT.items()}
# 产品类型映射
PRODUCT_ICE2VT: Dict[str, Product] = {
    "FUT": Product.FUTURES,
    "OPT": Product.OPTION,
    "STK": Product.EQUITY
}

# 期权类型映射
OPTIONTYPE_ICE2VT: Dict[str, OptionType] = {
    "C": OptionType.CALL,
    "P": OptionType.PUT
}


# 其他常量
MAX_FLOAT = sys.float_info.max                  # 浮点数极限值
CHINA_TZ = ZoneInfo("Asia/Shanghai")       # 中国时区

# 合约数据全局缓存字典
symbol_contract_map: Dict[str, ContractData] = {}


class IceTCoreGateway(BaseGateway,BaseDatafeed):
    default_name: str = "ICETCore"
    default_setting: Dict[str, str] = {
        "客户端路径": "C:/AlgoMaster2/APPs64"
    }

    exchanges: List[str] = list(EXCHANGE_ICE2VT.values())

    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        """构造函数"""
        super().__init__(event_engine, gateway_name)
        self.eventobj=IceTCoreAPI(self)
        
        self.api: "TCoreAPI" =None
        self.reqid: int = 0

        self.subscribed: set = set()

        self.order_ref: int = 0

        self.connect_status: bool = False
        self.login_status: bool = False

        self.login_failed: bool = False
        self.auth_failed: bool = False
        self.contract_inited: bool = False

        self.userid: str = ""
        self.brokerid: str = ""
        self.auth_code: str = ""

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        self.api=TCoreAPI(apppath=setting["客户端路径"],eventclass=self.eventobj)
        # 禁止重复发起连接，会导致异常崩溃
        if not self.connect_status:
            self.api.connect()#(self.appid,self.auth_code)
            self.connect_status = True
            self.qryInstrument()
        #self.init_query()

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        self.write_log("订阅行情"+req.symbol)

        contract: ContractData = symbol_contract_map.get(EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol, None)
        symbolhead="TC.S."
        if contract.product==Product.FUTURES:
            symbolhead="TC.F."
        elif contract.product==Product.OPTION:
            symbolhead="TC.O." 
        self.api.subquote(symbolhead+contract.name)
        self.subscribed.add(symbolhead+contract.name)
        #print(symbolhead+EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol)
        #self.api.subquote(symbolhead+EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol)
        #self.subscribed.add(symbolhead+EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        if req.offset not in OFFSET_VT2ICE:
            self.write_log("请选择开平方向")
            return ""

        if req.type not in ORDERTYPE_VT2ICE:
            self.write_log(f"当前接口不支持该类型的委托{req.type.value}")
            return ""

        self.order_ref += 1
        contract: ContractData = symbol_contract_map.get(EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol, None)
        symbolhead="TC.S."
        if contract.product==Product.FUTURES:
            symbolhead="TC.F."
        elif contract.product==Product.OPTION:
            symbolhead="TC.O." 

        tp: tuple = ORDERTYPE_VT2ICE[req.type]
        price_type, time_condition = tp
        OrderStruct.Symbol=symbolhead+contract.name#EXCHANGE_VT2ICE[req.exchange]+"."+req.symbol
        OrderStruct.BrokerID=self.brokerid
        OrderStruct.Account=self.userid
        OrderStruct.Price=req.price
        OrderStruct.TimeInForce=time_condition
        OrderStruct.Side= DIRECTION_VT2ICE.get(req.direction, "")
        OrderStruct.OrderType=price_type
        OrderStruct.OrderQty=int(req.volume)
        OrderStruct.PositionEffect=OFFSET_VT2ICE.get(req.offset, "")#PositionEffect.Auto
        OrderStruct.Synthetic=0
        OrderStruct.SelfTradePrevention=3

        ordid,msg = self.api.neworder(OrderStruct)
        if not ordid:
            self.write_log(f"委托请求发送失败，错误代码：{msg}")
            return ""
        while True:
            if self.api.getorderinfo(ordid):
                orderidlist: str = self.api.getorderinfo(ordid)
                break
        for orderid in orderidlist:
            order: OrderData = req.create_order_data(orderid['ReportID'], self.default_name)
            self.on_order(order)
        return order.vt_orderid

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
       #print(req.orderid)
        #self.api.getorderinfo(req.orderid)['ReportID']
        self.api.cancelorder(req.orderid)

    def query_account(self) -> None:
        """查询资金"""
        self.api.getaccmargin(self.brokerid+"-"+self.userid)

    def query_position(self) -> None:
        """查询持仓"""
        if not symbol_contract_map:
            return
        self.api.getposition(self.brokerid+"-"+self.userid)

    def close(self) -> None:
        """关闭连接"""
        if self.connect_status:
            self.api.disconnect()

    def write_error(self, msg: str, error: dict) -> None:
        """输出错误信息日志"""
        error_id: int = error["ErrorID"]
        error_msg: str = error["ErrorMsg"]
        msg: str = f"{msg}，代码：{error_id}，信息：{error_msg}"
        self.write_log(msg)


    def qryInstrument(self):
        """合约查询回报"""
        data=self.api.getallsymbol()
        if data:
            for symb in data:
                symbcheck=symb.split(".")
                if len(symbcheck)>4:
                    if "TC.F." in symb:
                        product: Product = Product.FUTURES
                    elif "TC.O." in symb:
                        product: Product = Product.OPTION
                    elif "TC.S.SSE.60" or "TC.S.SSE.90" or "TC.S.SZSE.00" or "TC.S.SZSE.30" or "TC.S.SZSE.20":
                        product: Product = Product.EQUITY
                    elif "TC.S.SSE.000" or "TC.S.SZSE.399":
                        product: Product = Product.INDEX
                    elif "TC.S.SSE.51" or "TC.S.SZSE.15":
                        product: Product = Product.ETF
                    elif "TC.S.SSE.01" or "TC.S.SSE.11" or "TC.S.SSE.20" or "TC.S.SZSE.10" or "TC.S.SZSE.12" or "TC.S.SZSE.13":
                        product: Product = Product.BOND
                    elif "TC.S.SSE.50" or "TC.S.SZSE.16":
                        product: Product = Product.FUND
                    strsymbol=symb.replace(symbcheck[0]+"."+symbcheck[1]+"."+symbcheck[2]+".","").replace(".","")
                    contract: ContractData = ContractData(
                        symbol=strsymbol,
                        exchange=EXCHANGE_ICE2VT[symbcheck[2]],
                        name=symb.replace(symbcheck[0]+"."+symbcheck[1]+".",""),
                        product=product,
                        size=float(self.api.getsymbolvolume_multiple(symb)),
                        pricetick=float(self.api.getsymbol_ticksize(symb)),
                        gateway_name=self.default_name
                    )

                    # 期权相关
                    if contract.product == Product.OPTION:
                        "TC.O.SSE.510050.202308.C.2.3"
                        strick=symb.replace(symbcheck[0]+"."+symbcheck[1]+"."+symbcheck[2]+"."+symbcheck[3]+"."+symbcheck[4]+"."+symbcheck[5]+".","")
                        contract.symbol=self.api.getsymbol_id(symb)
                        contract.option_portfolio =symbcheck[4]
                        contract.option_underlying =symbcheck[3]
                        contract.option_type = OPTIONTYPE_ICE2VT.get(symbcheck[5], None)
                        contract.option_strike = float(strick)
                        contract.option_index = strick
                        #contract.option_listed = datetime.strptime(data["OpenDate"], "%Y%m%d")
                        contract.option_expiry = datetime.strptime(self.api.getexpirationdate(symb), "%Y%m%d")
                        # contract.__post_init__()
                    self.on_contract(contract)
                    #symbol_contract_map[symb.replace(symbcheck[0]+"."+symbcheck[1]+".","")] = contract
                    symbol_contract_map[symbcheck[2]+"."+strsymbol] = contract

            self.contract_inited = True
            self.write_log("合约信息查询成功")
            for acc in self.api.getaccountlist():
                data2=self.api.getposition(acc["AccMask"])
                for data1 in data2:
                    if data1["Side"]!=0:
                        symbsplit=data1["Symbol"].split(".")
                        symbol: str = data1["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
                        contract1 = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)
                        if contract1:
                            position: PositionData = PositionData(
                                symbol=symbol,
                                exchange=contract1.exchange,
                                direction=DIRECTION_ICE2VT[data1["Side"]],
                                volume=float(data1["Quantity"]),
                                price=float(data1["AvgPrice"]),
                                frozen=data1["LongFrozen"] if data1["Side"]==1 else data1["ShortFrozen"],
                                pnl=data1["FloatProfitByDate"],
                                yd_volume=data1["YdLongQty"] if data1["Side"]==1 else data1["YdShortQty"],
                                gateway_name=self.default_name
                            )
                        else:
                            self.write_log(f"持仓合约不存在:{data1['Symbol']}")
                            position: PositionData = PositionData(
                                symbol=data1["Symbol"],
                                exchange=Exchange.LOCAL,
                                direction=DIRECTION_ICE2VT[data1["Side"]],
                                volume=float(data1["Quantity"]),
                                price=float(data1["AvgPrice"]),
                                frozen=data1["LongFrozen"] if data1["Side"]==1 else data1["ShortFrozen"],
                                pnl=data1["FloatProfitByDate"],
                                yd_volume=data1["YdLongQty"] if data1["Side"]==1 else data1["YdShortQty"],
                                gateway_name=self.default_name
                            )
                        self.on_position(position)
            
            orderreport=self.api.getorderreport()
            for orderdata in orderreport:
                if orderdata["ExecType"]==10 or orderdata['ExecType']==12:
                    return
                symbsplit=orderdata["Symbol"].split(".")
                symbol: str = orderdata["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
                contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

                timestamp: str = f"{orderdata['TransactDate']} {orderdata['TransactTime']}"
                dt: datetime = datetime.strptime(timestamp, "%Y%m%d %H%M%S")
                dt: datetime = dt.replace(tzinfo=CHINA_TZ)+timedelta(hours=8)

                tp: tuple = (orderdata["OrderType"], orderdata["TimeInForce"])

                order: OrderData = OrderData(
                    symbol=symbol,
                    exchange=contract.exchange,
                    orderid=orderdata["ReportID"],
                    type=ORDERTYPE_ICE2VT[tp],
                    direction=DIRECTION_ICE2VT[orderdata["Side"]],
                    offset=OFFSET_ICE2VT[orderdata["PositionEffect"]],
                    price=float(orderdata["Price"] if orderdata["Price"] else 0),
                    volume=float(orderdata["OrderQty"]),
                    traded=float(orderdata["CumQty"]),
                    status=STATUS_ICE2VT[orderdata["ExecType"]],
                    datetime=dt,
                    reference=orderdata["UserKey1"],
                    gateway_name=self.default_name
                )
                self.on_order(order)
                self.eventobj.sysid_orderid_map[orderdata["UserKey1"]] = orderdata["ReportID"]

            fillreport=self.api.getfilledreport()
            for filldata in fillreport:
                symbsplit=filldata["Symbol"].split(".")
                symbol: str = filldata["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
                contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

                timestamp: str = f"{filldata['TransactDate']} {filldata['TransactTime']}"
                dt: datetime = datetime.strptime(timestamp, "%Y%m%d %H%M%S")
                dt: datetime = dt.replace(tzinfo=CHINA_TZ)+timedelta(hours=8)
                
                trade: TradeData = TradeData(
                    symbol=symbol,
                    exchange=contract.exchange,
                    orderid=filldata["ReportID"],
                    tradeid=filldata["OrderID"],
                    direction=DIRECTION_ICE2VT[filldata["Side"]],
                    offset=OFFSET_ICE2VT[filldata["PositionEffect"]],
                    price=float(filldata["AvgPrice"] if filldata["AvgPrice"] else 0),
                    volume=float(filldata["CumQty"]),
                    datetime=dt,
                    gateway_name=self.default_name
                )
                self.on_trade(trade)
class IceTCoreAPI(TradeEvent,QuoteEvent):
    """"""
    def __init__(self, gateway: IceTCoreGateway) -> None:
        """构造函数"""
        self.subscribed: set = set()
        self.gateway: IceTCoreGateway = gateway
        self.gateway_name: str = gateway.gateway_name

        self.sysid_orderid_map: Dict[str, str] = {}
        self.current_date: str = datetime.now().strftime("%Y%m%d")

    def onconnected(self,apitype:str) -> None:
        """服务器连接成功回报"""
        if "quote"==apitype:
            self.login_status = True
            self.gateway.write_log("行情接口连线成功")
            for symbol in self.subscribed:
                self.gateway.subscribe(symbol)
        if "trade"== apitype:
            self.gateway.write_log("交易接口连线成功")
            self.gateway.api.submargin()
            self.gateway.api.subposition()

    def ondisconnected(self,apitype:str) -> None:
        """服务器连接断开回报"""
        if "quote" in apitype:
            self.login_status = False
            self.gateway.write_log("行情接口连接断开")
        if "trade" in apitype:
            self.login_status = False
            self.gateway.write_log(f"交易接口连线断开")

    # def onbar(self,datatype,interval,symbol,data:list,isreal:bool)-> None:
    #     pass
    # def ongreeksreal(self,datatype,symbol,data:dict):
    #     pass
    # def ongreeksline(self,datatype,interval,symbol,data,isreal):
    #     pass
    def onquote(self,data)-> None:
        """行情数据推送"""
        # 过滤没有时间戳的异常行情数据
        # if not data["DateTime"]:
        #     return
        # # 过滤还没有收到合约数据前的行情推送
        symbsplit=data["Symbol"].split(".")
        symbol: str = data["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
        contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

        if not contract:
            return
        tick: TickData = TickData(
            symbol=symbol,
            exchange=contract.exchange,
            datetime=data["DateTime"].replace(tzinfo=CHINA_TZ),
            #name=contract.name,
            volume=data["Volume"],
            turnover=data["Turnover"],
            open_interest=data["OpenInterest"],
            last_price=adjust_price(data["Last"]),
            limit_up=data["UpperLimit"],
            limit_down=data["LowerLimit"],
            open_price=adjust_price(data["Open"]),
            high_price=adjust_price(data["High"]),
            low_price=adjust_price(data["Low"]),
            pre_close=adjust_price(data["YClosedPrice"]),
            bid_price_1=adjust_price(data["Bid"]),
            ask_price_1=adjust_price(data["Ask"]),
            bid_volume_1=data["BidVolume"],
            ask_volume_1=data["AskVolume"],
            gateway_name=self.gateway_name
        )

        if data["BidVolume1"] or data["AskVolume1"]:
            tick.bid_price_2 = adjust_price(data["Bid1"])
            tick.bid_price_3 = adjust_price(data["Bid2"])
            tick.bid_price_4 = adjust_price(data["Bid3"])
            tick.bid_price_5 = adjust_price(data["Bid4"])

            tick.ask_price_2 = adjust_price(data["Ask1"])
            tick.ask_price_3 = adjust_price(data["Ask2"])
            tick.ask_price_4 = adjust_price(data["Ask3"])
            tick.ask_price_5 = adjust_price(data["Ask4"])

            tick.bid_volume_2 = data["BidVolume1"]
            tick.bid_volume_3 = data["BidVolume2"]
            tick.bid_volume_4 = data["BidVolume3"]
            tick.bid_volume_5 = data["BidVolume4"]

            tick.ask_volume_2 = data["AskVolume1"]
            tick.ask_volume_3 = data["AskVolume2"]
            tick.ask_volume_4 = data["AskVolume3"]
            tick.ask_volume_5 = data["AskVolume4"]

        self.gateway.on_tick(tick)

    # def onATM(self,datatype,symbol,data:dict):
    #     pass
    def onservertime(self, serverdt):
        self.current_date = serverdt.strftime("%Y%m%d")#.replace(tzinfo=CHINA_TZ)
    def onaccountlist(self,data,count):
        self.gateway.userid=data[0]["Account"]
        self.gateway.brokerid=data[0]["BrokerID"]
    def onordereportreal(self,data):
        """委托更新推送"""
        if not self.gateway.contract_inited:
            return
        # if data["ExecType"]==10:
        #     self.gateway.write_error("交易委托失败",data["ReportID"])
        #     return
        # elif data['ExecType']==12:
        #     self.gateway.write_log("删改单失败："+data["ReportID"])
        #     return
        symbsplit=data["Symbol"].split(".")
        symbol: str = data["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
        contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

        timestamp: str = f"{data['TransactDate']} {data['TransactTime']}"
        dt: datetime = datetime.strptime(timestamp, "%Y%m%d %H%M%S")
        dt: datetime = dt.replace(tzinfo=CHINA_TZ)+timedelta(hours=8)

        tp: tuple = (data["OrderType"], data["TimeInForce"])

        order: OrderData = OrderData(
            symbol=symbol,
            exchange=contract.exchange,
            orderid=data["ReportID"],
            type=ORDERTYPE_ICE2VT[tp],
            direction=DIRECTION_ICE2VT[data["Side"]],
            offset=OFFSET_ICE2VT[data["PositionEffect"]],
            price=float(data["Price"] if data["Price"] else 0),
            volume=float(data["OrderQty"]),
            traded=float(data["CumQty"]),
            status=STATUS_ICE2VT[data["ExecType"]],
            datetime=dt,
            reference=data["UserKey1"],
            gateway_name=self.gateway_name
        )
        self.gateway.on_order(order)

        self.sysid_orderid_map[data["UserKey1"]] = data["ReportID"]


    def onfilledreportreal(self,data):
        """成交数据推送"""
        if not self.gateway.contract_inited:
            return
        symbsplit=data["Symbol"].split(".")
        symbol: str = data["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
        contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

        orderid: str = self.sysid_orderid_map[data["UserKey1"]]

        timestamp: str = f"{data['TransactDate']} {data['TransactTime']}"
        dt: datetime = datetime.strptime(timestamp, "%Y%m%d %H%M%S")
        dt: datetime = dt.replace(tzinfo=CHINA_TZ)+timedelta(hours=8)
        
        trade: TradeData = TradeData(
            symbol=symbol,
            exchange=contract.exchange,
            orderid=data["DetailReportID"],
            tradeid=data["OrderID"],
            direction=DIRECTION_ICE2VT[data["Side"]],
            offset=OFFSET_ICE2VT[data["PositionEffect"]],
            price=float(data["MatchedPrice"] if data["MatchedPrice"] else 0),
            volume=float(data["MatchedQty"]),
            datetime=dt,
            gateway_name=self.gateway_name
        )
        self.gateway.on_trade(trade)
    # def onorderreportreset(self):
    #     self.positions.clear()
    # def onpositionmoniter(self,data):
    #     pass
    def onmargin(self,accmask,data):
        """资金查询回报"""
        # if "Account" not in data[0].keys():
        #     return
        for data1 in data:
            if "Account" not in data1.keys():
                return
            account: AccountData = AccountData(
                accountid=data1["Account"],
                balance=float(data1["TotalEquity"]),
                frozen=float(data1["FrozenCash"]),
                gateway_name=self.gateway_name
            )
            account.available = data1["ExcessEquity"]
            self.gateway.on_account(account)

    def onposition(self,accmask,data):
        if not data:
            return
        if not self.gateway.contract_inited:
            return
        for data1 in data:
            if data1["Side"]!=0:
                symbsplit=data1["Symbol"].split(".")
                symbol: str = data1["Symbol"].replace(symbsplit[0]+"."+symbsplit[1]+"."+symbsplit[2]+".","").replace(".","")
                contract: ContractData = symbol_contract_map.get(symbsplit[2]+"."+symbol, None)

                if contract:
                    position: PositionData = PositionData(
                        symbol=symbol,
                        exchange=contract.exchange,
                        direction=DIRECTION_ICE2VT[data1["Side"]],
                        volume=float(data1["Quantity"]),
                        price=float(data1["AvgPrice"]),
                        frozen=data1["LongFrozen"] if data1["Side"]==1 else data1["ShortFrozen"],
                        pnl=data1["FloatProfitByDate"],
                        yd_volume=data1["YdLongQty"] if data1["Side"]==1 else data1["YdShortQty"],
                        gateway_name=self.gateway_name
                    )
                else:
                    self.write_log(f"持仓合约不存在:{data1['Symbol']}")
                    position: PositionData = PositionData(
                        symbol=data1["Symbol"],
                        exchange=Exchange.LOCAL,
                        direction=DIRECTION_ICE2VT[data1["Side"]],
                        volume=float(data1["Quantity"]),
                        price=float(data1["AvgPrice"]),
                        frozen=data1["LongFrozen"] if data1["Side"]==1 else data1["ShortFrozen"],
                        pnl=data1["FloatProfitByDate"],
                        yd_volume=data1["YdLongQty"] if data1["Side"]==1 else data1["YdShortQty"],
                        gateway_name=self.gateway_name
                    )
                self.gateway.on_position(position)


def adjust_price(price: float) -> float:
    """将异常的浮点数最大值（MAX_FLOAT）数据调整为0"""
    if price == MAX_FLOAT:
        price = 0
    return price

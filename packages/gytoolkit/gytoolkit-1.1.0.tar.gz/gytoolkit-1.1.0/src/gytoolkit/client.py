from typing import List
import pandas as pd
from .position import Position
from .constants import TradeData

class Client:
    _client_instances = {}  # Dictionary to store client instances by id

    def __new__(cls, id, *args, **kwargs):
        # Check if a fund instance with the same id exists; if yes, return the existing instance
        if id in cls._client_instances:
            return cls._client_instances[id]
        # If not, create a new instance and store it in the dictionary
        instance = super(Client, cls).__new__(cls)
        cls._client_instances[id] = instance
        return instance

    def __init__(self, id, name=None):
        if not hasattr(self, "id"):
            self.id = id
            self.name = name
            self.positions: List[Position] = []
            self.trades: List[TradeData] = []
    
    def add_position(self, position:Position):
        self.positions.append(position)

    def add_trade(self, trade:TradeData):
        self.trades.append(trade)

    def get_trade_history(self, prodcode:str):
        # 对指定产品输出这个客户的交易记录
        trades:List[TradeData] = []
        for trade in self.trades:
            if trade.prodcode == prodcode:
                trades.append(trade)
        # 按日期排序交易记录
        trades.sort(key=lambda x: x.date)
        return trades
    
    def get_assets_and_profit_loss(self, date):
        assets = 0
        profit_loss = 0
        for position in self.positions:
            # Only consider positions that are not closed and were created before the date
            if not position.closed and position.creation_date <= date:
                value = position.shares * position.fund.get_net_value(date)
                assets += value
                profit_loss += value - position.cost
        return assets, profit_loss

    def summary_by_fund(self, date):
        date = pd.to_datetime(date)
        # 按产品汇总客户目前的持仓份额和持仓成本
        summary = {}
        for position in self.positions:
            nv_data = position.fund.get_net_value(date)
            
            if nv_data is None:
                continue

            fund_code = position.fund.code
            if fund_code not in summary:
                summary[fund_code] = {
                    "持有份额": 0,
                    "成本": 0,
                    "市值": 0,
                    "分红金额": 0,
                    "已赎回金额": 0,
                    "提取业绩报酬": 0,
                    "盈亏": 0,
                }
                summary[fund_code]["净值日期"] = nv_data.date
                summary[fund_code]["单位净值"] = nv_data.netvalue
                summary[fund_code]["累计净值"] = nv_data.cum_netvalue
            summary[fund_code]["持有份额"] += position.shares
            summary[fund_code]["成本"] += position.cost
            summary[fund_code]["市值"] += position.market_value(date=date)
            summary[fund_code]["分红金额"] += position.dividend_amount
            summary[fund_code]["已赎回金额"] += position.redeemed_amount
            summary[fund_code]["提取业绩报酬"] += position.perf_fee
            summary[fund_code]["盈亏"] += position.pnl(date=date)

        return pd.DataFrame.from_dict(summary, orient="index")





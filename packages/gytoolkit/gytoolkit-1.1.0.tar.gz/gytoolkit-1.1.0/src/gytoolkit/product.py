from typing import List,Union
from datetime import datetime
import pandas as pd
from .constants import NetValueData, ProdInfoData, DividendData, TradeData
from .position import Position


class Product:
    _product_instances = {}  # Dictionary to store fund instances by code

    def __new__(cls, code, *args, **kwargs):
        # Check if a fund instance with the same code exists; if yes, return the existing instance
        if code in cls._product_instances:
            return cls._product_instances[code]
        # If not, create a new instance and store it in the dictionary
        instance = super(Product, cls).__new__(cls)
        cls._product_instances[code] = instance
        return instance

    def __init__(
        self,
        code,
        prodinfo: ProdInfoData = None,
    ):
        if not hasattr(
            self, "code"
        ):  # Initialize attributes only for newly created instances
            self.code = code
            self.info = prodinfo
            self.netvalues: List[NetValueData] = []
            self.positions: List[Position] = []
            self.dividends: List[DividendData] = []
            self.trades: List[TradeData] = []
            self.fixedtime_perfees = []  # 基金的固定时点业绩报酬计提记录

    def add_netvalue(self, netvalue_data: Union[NetValueData,List[NetValueData]]):
        """
        Adds a NetvalueData object to the list of net values for the current fund.

        Parameters:
            netvalue_data (NetvalueData): The NetvalueData object to be added.

        Raises:
            ValueError: If the NetvalueData object is not associated with the current fund.

        Returns:
            None
        """
        # Check if the NetvalueData is associated with the current fund
        if not isinstance(netvalue_data,list):
            netvalue_data = [netvalue_data]
        
        for nv_data in netvalue_data:
            if nv_data.prodcode != self.code:
                raise ValueError("NetvalueData is not associated with this fund.")

            # Find the appropriate position to insert the NetvalueData in chronological order
            insert_index = len(self.netvalues)
            for i, data in enumerate(self.netvalues):
                if nv_data.date < data.date:
                    insert_index = i
                    break

            # Insert the NetvalueData at the appropriate position
            self.netvalues.insert(insert_index, nv_data)

    def get_net_value(self, date: datetime, precise=False) -> NetValueData:
        """
        返回最接近给定日期的NetvalueData对象。

        参数:
            date (datetime.date): 目标日期。
            precise (bool, 可选): 如果设置为True,则仅在数据的日期与目标日期完全匹配时返回NetvalueData对象。
                                    如果设置为False(默认值),则返回在目标日期之前或与之相等的最接近的NetvalueData对象。

        返回值:
            NetvalueData: 最接近给定日期的NetvalueData对象。如果找不到数据，则返回None。
        """
        closest_data = None

        for data in self.netvalues:
            if data.date <= date:
                if closest_data is None or data.date > closest_data.date:
                    closest_data = data

        if precise and closest_data is not None:
            if closest_data.date != date:
                closest_data = None

        return closest_data

    def add_position(self, position:Position):
        self.positions.append(position)

    def add_dividend(self, dividend:DividendData):
        self.dividends.append(dividend)

    def add_trade(self, trade:TradeData):
        self.trades.append(trade)

    def get_asset_size(self, date):
        asset_size = 0
        for position in self.positions:
            # Only consider positions that are not closed and were created before the date
            if not position.closed and position.creation_date <= date:
                # You need to implement the get_net_value(date) method
                asset_size += position.shares * self.get_net_value(date)
        return asset_size

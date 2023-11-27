import pandas as pd
from glob import glob
from .dataloader import BaseDataLoader
from .constants import TradeData

cols = [
    "client_id",
    "prodcode",
    "date",
    "type",
    "amount",
    "shares",
]

index_col = ["client_id", "prodcode", "date", "type"]


class TradeLoader(BaseDataLoader):
    def __init__(self) -> None:
        super().__init__(TradeData)

    def load_otc(self, *args, **kwargs):
        folder_path = self.source["otc"]
        file_paths = glob(folder_path + "/*.xlsx")
        otc_trade_list = []
        for file in file_paths:
            otc_trade_list.append(
                pd.read_excel(file, header=7)[:-1][
                    ["客户代码", "交易日期", "交易类别", "产品代码", "确认数量", "确认金额"]
                ].drop_duplicates(keep="last")
            )

        otc_trade = pd.concat(otc_trade_list).drop_duplicates(keep="last")

        if not otc_trade.empty:
            col_map = {
                "客户代码": "client_id",
                "产品代码": "prodcode",
                "交易日期": "date",
                "交易类别": "type",
                "确认数量": "shares",
                "确认金额": "amount",
            }
            otc_trade.rename(columns=col_map, inplace=True)

            otc_trade["date"] = pd.to_datetime(otc_trade["date"], format="%Y%m%d")

        return self.format_data(otc_trade, cols=cols, index_col=index_col)

    def load_local(self, *args, **kwargs):
        file_paths = self.source["local"]
        local_trade_data = pd.read_excel(file_paths).drop_duplicates(keep="last")

        if not local_trade_data.empty:
            col_map = {
                "客户代码": "client_id",
                "产品代码": "prodcode",
                "交易日期": "date",
                "交易类别": "type",
                "确认数量": "shares",
                "确认金额": "amount",
            }
            local_trade_data.rename(columns=col_map, inplace=True)

            local_trade_data["date"] = pd.to_datetime(local_trade_data["date"], format="%Y%m%d")

        return self.format_data(local_trade_data, cols=cols, index_col=index_col)


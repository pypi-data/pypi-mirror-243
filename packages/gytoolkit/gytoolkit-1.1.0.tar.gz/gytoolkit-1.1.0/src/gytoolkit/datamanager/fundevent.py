from abc import abstractmethod
import pandas as pd
from .dataloader import BaseDataLoader
from .constants import FundEventData, DividendData, PerfFeeData

index_col = ["prodcode", "date"]


class FundEventLoader(BaseDataLoader):
    def __init__(self, datatype, buss_type, col_map) -> None:
        self.buss_type = buss_type
        self.col_map = col_map
        super().__init__(datatype)

    def load_local(self):
        buss_type = self.buss_type
        col_map = self.col_map

        file_paths = self.source["local"]
        fund_event_data = pd.read_excel(file_paths).drop_duplicates(keep="last")

        if not fund_event_data.empty:
            fund_event_data.rename(columns=col_map, inplace=True)

            fund_event_data["date"] = pd.to_datetime(
                fund_event_data["date"], format="%Y-%m-%d"
            )

            fund_event_data = fund_event_data[fund_event_data.type == buss_type]

        return self.format_data(
            fund_event_data, cols=col_map.values(), index_col=index_col
        )


class DividendLoader(FundEventLoader):
    def __init__(self) -> None:
        col_map = {
            "产品代码": "prodcode",
            "时间": "date",
            "业务类型": "type",
            "金额": "dividend_per_share",
        }
        buss_type = "分红"
        super().__init__(DividendData, buss_type, col_map)


class PerfFeeLoader(FundEventLoader):
    def __init__(self) -> None:
        col_map = {
            "产品代码": "prodcode",
            "时间": "date",
            "业务类型": "type",
        }
        buss_type = "固定时点计提"
        super().__init__(PerfFeeData, buss_type, col_map)

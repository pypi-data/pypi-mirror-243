from typing import List, Union
import glob
import pandas as pd
from gytoolkit import ppwdbapi
from .constants import ProdInfoData
from .dataloader import BaseDataLoader
from .utils import benchmark_to_dict

STRATEGY_BENCHMARK_MAP = {
    "主观多头": "沪深300:1",
    "中证500指增": "中证500:1",
    "中证1000指增": "中证1000:1",
    "沪深300指增": "沪深300:1",
    "量化选股": "中证1000:1",
}

cols = [
    "prodcode",
    "shortname",
    "strategy",
    "benchmark",
]

index_col = "prodcode"


class ProdInfoLoader(BaseDataLoader):
    def __init__(self) -> None:
        super().__init__(ProdInfoData)

    def load_local(self, *args, **kwargs) -> Union[List[ProdInfoData], pd.DataFrame]:
        folder_path = self.source["local"]
        file_paths = glob.glob(folder_path + "/*.xlsx")
        local_prodinfo_list = []
        for file in file_paths:
            local_prodinfo_list.append(
                pd.read_excel(file)[["产品代码", "产品简称", "投资策略", "业绩基准"]].drop_duplicates(
                    keep="last"
                )
            )

        local_prodinfo_list.业绩基准 = local_prodinfo_list.业绩基准.apply(benchmark_to_dict)

        local_prodinfo = pd.concat(local_prodinfo_list).drop_duplicates(keep="last")

        if not local_prodinfo.empty:
            col_map = {
                "产品代码": "prodcode",
                "产品简称": "shortname",
                "投资策略": "strategy",
                "业绩基准": "benchmark",
            }
            local_prodinfo.rename(columns=col_map, inplace=True)

        return self.format_data(local_prodinfo,cols=cols,index_col=index_col)

    def load_ppw(self, *args, **kwargs) -> Union[List[ProdInfoData], pd.DataFrame]:
        api: ppwdbapi = self.source["ppw"]
        products_info = api.get_fund(*args, **kwargs)

        if not products_info.empty:
            products_info["业绩基准"] = products_info.三级策略.applymap(STRATEGY_BENCHMARK_MAP)
            products_info.业绩基准 = products_info.业绩基准.apply(benchmark_to_dict)

            col_map = {
                "备案编码": "prodcode",
                "产品简称": "shortname",
                "三级策略": "strategy",
                "业绩基准": "benchmark",
            }
            products_info.rename(columns=col_map, inplace=True)
        return self.format_data(products_info,cols=cols,index_col=index_col)

    # def load(self,df=True,**kwargs) -> Union[List[ProdInfoData], pd.DataFrame]:
    #     data = self._load(**kwargs)
    #     if df:
    #         return data
    #     else:
    #         if data.empty:
    #             return []
    #         return [ProdInfoData(**row) for index, row in data.reset_index().iterrows()]

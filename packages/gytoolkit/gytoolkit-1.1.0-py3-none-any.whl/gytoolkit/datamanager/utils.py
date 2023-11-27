import numpy as np
import pandas as pd
import glob
from typing import List, Union, Optional
from .constants import NetValueData, TradeData


def ppwnvformatter(ppwnvdf, df=True) -> Union[List[NetValueData], pd.DataFrame]:
    """
    将ppwdbapi的净值数据转换为gytoolkit定义的净值数据
    """
    cols = [
        "date",
        "prodcode",
        "netvalue",
        "cum_netvalue",
        "prodname",
        "netasset",
        "shares",
    ]
    col_map = {
        "净值日期": "date",
        "备案编码": "prodcode",
        "单位净值": "netvalue",
        "累计净值": "cum_netvalue",
        "产品简称": "prodname",
    }
    ppwnvdf.rename(columns=col_map, inplace=True)
    ppwnvdf[["netasset", "shares"]] = np.nan
    ppwnvdf = ppwnvdf[cols]
    if df:
        return ppwnvdf.set_index(["date", "prodcode"])
    else:
        return [NetValueData(**row) for index, row in ppwnvdf.reset_index().iterrows()]


def get_otc_nv(
    folder_path: str, df=True
) -> Union[List[NetValueData], pd.DataFrame]:
    file_paths = glob.glob(folder_path + "/*.xlsx")
    otc_nv_list = []
    for file in file_paths:
        otc_nv_list.append(
            pd.read_excel(file, header=8)[:-1][
                ["产品编码", "净值日期", "产品简称", "最新净值", "累计净值"]
            ].drop_duplicates(subset=["产品编码", "净值日期"], keep="last")
        )
    otc_nv = pd.concat(otc_nv_list).drop_duplicates(
        subset=["产品编码", "净值日期"], keep="last"
    )

    if otc_nv.empty:
        if df:
            return pd.DataFrame()
        else:
            return []

    otc_nv["净值日期"] = pd.to_datetime(otc_nv["净值日期"], format="%Y%m%d")
    cols = [
        "date",
        "prodcode",
        "netvalue",
        "cum_netvalue",
        "prodname",
        "netasset",
        "shares",
    ]
    col_map = {
        "净值日期": "date",
        "产品编码": "prodcode",
        "最新净值": "netvalue",
        "累计净值": "cum_netvalue",
        "产品简称": "prodname",
    }

    otc_nv.rename(columns=col_map, inplace=True)
    otc_nv[["netasset", "shares"]] = np.nan
    otc_nv = otc_nv[cols]

    if df:
        return otc_nv.set_index(["date", "prodcode"])
    else:
        return [NetValueData(**row) for index, row in otc_nv.reset_index().iterrows()]


def get_otc_trade(
    folder_path: str, df=True
) -> Union[List[TradeData], pd.DataFrame]:
    file_paths = glob.glob(folder_path + "/*.xlsx")
    otc_trade_list = []
    for file in file_paths:
        otc_trade_list.append(
            pd.read_excel(file, header=7)[:-1][
                ["客户代码", "交易日期", "交易类别", "产品代码", "确认数量", "确认金额"]
            ].drop_duplicates(keep="last")
        )

    otc_trade = pd.concat(otc_trade_list).drop_duplicates(keep="last")

    if otc_trade.empty:
        if df:
            return pd.DataFrame()
        else:
            return []

    otc_trade["交易日期"] = pd.to_datetime(otc_trade["交易日期"], format="%Y%m%d")

    col_map = {
        "客户代码": "client_id",
        "产品代码": "prodcode",
        "交易日期": "date",
        "交易类别": "type",
        "确认数量": "shares",
        "确认金额": "amount",
    }
    otc_trade.rename(columns=col_map, inplace=True)
    cols = [
        "client_id",
        "prodcode",
        "date",
        "type",
        "amount",
        "shares",
    ]
    if df:
        return otc_trade[cols]
    else:
        return [TradeData(**row) for index, row in otc_trade.reset_index().iterrows()]


def benchmark_to_dict(benchmark):
    pairs = benchmark.split(',')
    # Initialize an empty dictionary
    result_dict = {}
    # Iterate through the key-value pairs
    for pair in pairs:
        # Split each pair into key and value
        key, value = pair.split(':')
        # Add the key-value pair to the dictionary (convert value to float)
        result_dict[key] = float(value)
        
    return result_dict
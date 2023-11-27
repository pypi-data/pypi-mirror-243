import pandas as pd


def calc_adjusted_netvalues(netvalues: pd.Series, cum_netvalues: pd.Series):
    netvalues = netvalues.sort_index()
    cum_netvalues = cum_netvalues.sort_index()
    dividend = (cum_netvalues-netvalues).diff().fillna(0)
    adjust_factor = (netvalues+dividend)/netvalues
    cum_adjust_factor = adjust_factor.cumprod()
    adj_cum_nv = cum_adjust_factor*netvalues
    adj_cum_nv.name = "分红复权累计净值"
    return pd.to_numeric(adj_cum_nv)


def truncate_timeseries(ts: pd.Series, start_time: pd.Timestamp, end_time: pd.Timestamp):
    return ts[(ts.index >= start_time) & (ts.index <= end_time)]

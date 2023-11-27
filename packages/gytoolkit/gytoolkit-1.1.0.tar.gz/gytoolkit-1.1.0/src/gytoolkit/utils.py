from typing import List, Union, Optional
import pandas as pd
from gytoolkit.constants import NetValueData


def save_netvalue(new_net_values: List[NetValueData], local_file: str = None):
    """
    更新本地的净值解析文件
    args:
        new_net_values:新解析的净值数据
        save_file:本地储存文件路径,如有数据则更新,如没有则创建
    output:
        None
    """
    if len(new_net_values) > 0:
        new_net_values = pd.DataFrame(new_net_values).set_index(["date", "prodcode"])
        try:
            local_net_values = pd.read_excel(local_file, index_col=[0, 1])
            net_values = local_net_values.combine_first(new_net_values)
            net_values = net_values.sort_index(ascending=[False, True])
            net_values.to_excel(local_file)
        except:
            new_net_values.sort_index(ascending=[False, True]).to_excel(local_file)


def load_netvalue(
    local_file: str, df: bool = True
) -> Union[List[NetValueData], pd.DataFrame]:
    """
    Load net value data from a local file.

    Args:
        local_file (str): The path to the local file containing the net value data.
        df (bool, optional): Whether to return the data as a pandas DataFrame. 
            Defaults to True.

    Returns:
        Union[List[NetValueData], pd.DataFrame]: The loaded net value data. If `df` is True,
            it is returned as a DataFrame. Otherwise, it is returned as a list of NetValueData objects.
    """
    try:
        net_values = pd.read_excel(local_file, index_col=[0, 1])
        if not df:
            net_values = [NetValueData(**row) for index,row in net_values.reset_index().iterrows()]
    except:
        if df:
            net_values = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
        else:
            net_values = []
    return net_values

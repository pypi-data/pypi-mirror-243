from abc import abstractmethod
from typing import Literal, List
import pandas as pd


class BaseDataLoader:
    def __init__(self, datatype) -> None:
        self.datatype = datatype
        self.source = {}
        self.source_order = {}

    def add_source(
        self,
        source_name: Literal["mail", "otc", "ppw", "local"],
        priority: int,
        dirpath_or_api,
    ):
        self.source[source_name] = dirpath_or_api
        self.source_order[source_name] = priority

    def remove_source(
        self,
        source_name: Literal["mail", "otc", "ppw", "local"],
    ):
        self.source.pop(source_name)
        self.source_order.pop(source_name)

    @property
    def get_source_order(self) -> List[Literal["mail", "otc", "ppw", "local"]]:
        return sorted(self.source_order, key=self.source_order.get)

    def load_mail(self, *args, **kwargs):
        if "mail" in self.source.keys():
            return NotImplementedError

    def load_otc(self, *args, **kwargs):
        if "otc" in self.source.keys():
            return NotImplementedError

    def load_ppw(self, *args, **kwargs):
        if "ppw" in self.source.keys():
            return NotImplementedError

    def load_local(self, *args, **kwargs):
        if "local" in self.source.keys():
            return NotImplementedError

    def load(self, *args, df=True, **kwargs):
        for source_name in self.get_source_order:
            data = getattr(self, "load_" + source_name)(*args, **kwargs)
            if hasattr(self, "data"):
                self.data = self.data.combine_first(data)
            else:
                self.data = data
        if df:
            return data
        else:
            if data.empty:
                return []
            return [
                self.datatype(**row) for index, row in data.reset_index().iterrows()
            ]

    def format_data(self,data:pd.DataFrame,cols,index_col) -> pd.DataFrame:
        if data.empty:
            df = pd.DataFrame(columns=cols)
        else:
            df = data.reset_index()[cols]
        
        if index_col:
            df = df.set_index(index_col)
        
        return df
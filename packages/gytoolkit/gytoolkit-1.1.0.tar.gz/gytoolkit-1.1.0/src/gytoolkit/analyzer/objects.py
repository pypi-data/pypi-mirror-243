import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype, is_numeric_dtype


class TimeSerise:
    """
    金融时间序列描述器
    pd.Series
        index:时间 dtype:pd.Datetimeindex
        values:价格 dtype:np.float
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype):
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if value is None:
            return

        # value不是符合要求的pd.series
        try:
            value = value.dropna().sort_index()
            assert isinstance(value, pd.Series)
            assert is_datetime64_any_dtype(value.index)
            assert is_numeric_dtype(value)
            assert len(value) > 0
        except:
            return

        setattr(obj, self.private_name, value)
        # obj._validate()

    def __delete__(self, obj):
        delattr(obj, self.private_name)
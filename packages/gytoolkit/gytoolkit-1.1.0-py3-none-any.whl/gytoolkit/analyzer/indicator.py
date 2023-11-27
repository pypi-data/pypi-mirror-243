from typing import Tuple,List
import numpy as np
import pandas as pd
from math import pow, sqrt
import statsmodels.api as sm
from functools import wraps
from gytoolkit.product import Product
from datetime import datetime
from .utils import calc_adjusted_netvalues,truncate_timeseries
from .objects import TimeSerise

class Indicator:
    """
    计算时间序列的各项指标
    net_value 和 benchmark的index必须一致
    假设净值序列等间隔分布
    """
    _net_values = TimeSerise()
    _benchmark = TimeSerise()

    def __init__(self, net_values: pd.Series = None, benchmark: pd.Series = None) -> None:
        self._net_values = net_values
        self._benchmark = benchmark
        self.init()
        

            
    def init(self):
        """
        检查业绩基准是否满足要求
        检查净值的日期是否与业绩基准对齐
        """
        if (self._net_values is not None) and (self._benchmark is not None):
            # 用benchmark截取净值
            if (self._benchmark.index.min() > self._net_values.index.min()) | (self._benchmark.index.max() < self._net_values.index.max()):
                self._net_values = truncate_timeseries(self._net_values,start_time=self._benchmark.index.min(),end_time=self._benchmark.index.max())


            # detect abnormal index
            abnormal_index = self._net_values.index[~self._net_values.index.isin(
                self._benchmark.index)]
            if len(abnormal_index) > 0:
                correction = {}
                for error_index in abnormal_index:
                    correct_index = self._benchmark.index.asof(error_index)
                    correction[error_index] = correct_index

                self._net_values.rename(correction, inplace=True)
                self._net_values = self._net_values[~self._net_values.index.duplicated(
                    keep='first')]
        
        self._start = None
        self._end = None
        self.isvalid = self.check_valid()
        
    def check_valid(self):
        if self.nv_num<2:
            return False

        intervals = pd.Series(self.net_values.index).diff().dropna()
        if max(intervals)>pd.Timedelta("50d"):
            return False
        
        return True    
    @property
    def start(self):
        if self._start:
            return self._start
        else:
            return self._net_values.index.min()
    
    @start.setter
    def start(self,value):
        if not issubclass(value.__class__, datetime):
            raise TypeError("start must be datetime")
        # if value > self.end:
        #     raise ValueError("start must be less than end")
        self._start = value
        self.isvalid = self.check_valid()
    
    @property
    def end(self):
        if self._end:
            return self._end
        else:
            return self._net_values.index.max()
    
    @end.setter
    def end(self,value):
        if not issubclass(value.__class__, datetime):
            raise TypeError("end must be datetime")
        # if value < self.start:
        #     raise ValueError("end must be greater than start")
        self._end = value
        self.isvalid = self.check_valid()

    @property
    def net_values(self):
        return truncate_timeseries(self._net_values,start_time=self.start,end_time=self.end)
    
    @property
    def nv_start(self):
        return self.net_values.index.min()
    
    @property
    def nv_end(self):
        return self.net_values.index.max()
    
    @property
    def benchmark(self):
        return truncate_timeseries(self._benchmark,start_time=self.start,end_time=self.end).reindex(self.net_values.index)
    


    def from_product(product: Product,benmark_api = None):
        net_values = product.netvalues
        index = [net_value.date for net_value in net_values]

        unit_net_value = [net_value.netvalue for net_value in net_values]
        unit_net_value = pd.Series(data=unit_net_value,index=index)

        cum_net_value = [net_value.cum_netvalue for net_value in net_values]
        cum_net_value = pd.Series(data=unit_net_value,index=index)

        net_value_series = calc_adjusted_netvalues(netvalues=unit_net_value, cum_netvalues=cum_net_value)

        if benmark_api:
            benchmark_serise = benmark_api(product.info.benchmark)
        else:
            benchmark_serise = net_value_series
        
        return Indicator(net_value_series,benchmark_serise)

    def check(func):
        '''
        return None or the result.
        '''
        @wraps(func)
        def wrapper(self,*args, **kwargs):
            if self.isvalid==False:
                return np.nan
            result = func(self,*args, **kwargs)
            return result
        return wrapper

    @property
    def _returns(self):
        return self.net_values.pct_change().dropna()

    @property
    def _logreturns(self):
        return (np.log(self.net_values) - np.log(self.net_values.shift(1))).dropna()
    
    @property
    def _returns_benchmark(self):
        return self.benchmark.pct_change().dropna()

    @property
    def _excess_return_arithmetic(self):
        return self._returns - self._returns_benchmark

    @property
    def _excess_return_geometric(self):
        return (1+self._returns)/(1+self._returns_benchmark) - 1
    

    @property
    @check
    def interval(self) -> float:
        """
        净值序列的横跨天数
        """
        return (self.end-self.start).days

    @property
    @check
    def interval_year(self) -> float:
        """
        净值序列的横跨年数
        """
        return self.interval/365

    @property
    def nv_num(self):
        """
        净值样本数量
        """
        return len(self.net_values)

    @property
    @check
    def nv_freq(self) -> float:
        """
        净值数据频率：平均每两个净值之间的间隔天数
        周频数据应约为 7
        """
        if self.nv_num == 0:
            return 0 
        return self.interval/self.nv_num

    @property
    @check
    def nv_per_year(self) -> float:
        """
        平均每年有多少个净值数据（用于年化）
        """
        return self.nv_num/self.interval_year

    @property
    @check
    def total_return(self) -> float:
        """
        区间总收益
        """
        return self._calc_return()

    @property
    @check
    def total_benchmark_return(self) -> float:
        """
        业绩基准区间总收益
        """
        return self._calc_return(bm=True)

    @property
    @check
    def annulized_return(self) -> float:
        """区间年化收益"""
        return self._calc_return(annulized=True)

    @property
    @check
    def annulized_benchmark_return(self):
        """区间业绩基准年化收益"""
        return self._calc_return(annulized=True, bm=True)

    @property
    @check
    def annulized_excess_return(self):
        """区间简单超额年化收益"""
        return self.annulized_return-self.annulized_benchmark_return

    # @cache
    def _calc_return(self, annulized=False, bm=False):
        if not bm:
            p_series = self.net_values
        elif bm:
            p_series = self.benchmark

        if len(p_series) == 0:
            return 0

        s = p_series.iloc[0]
        e = p_series.iloc[-1]
        ret = e/s-1

        if not annulized:
            return ret

        elif annulized:
            years = self.interval_year
            if years == 0:
                return 0
            else:
                return pow(ret+1, 1/years) - 1

    @property
    @check
    def volatility(self) -> float:
        """区间波动率"""
        return self._returns.std(ddof=1)

    @property
    @check
    def annulized_volatility(self) -> float:
        """
        区间年化波动率，频率是nv_freq
        转化为年化波动率 公式:sqrt(days in year(365)/nv_freq)*vol = sqrt(days*num_nv/interval)*vol = sqrt(num_nv/year_interval)*vol
        """
        if self.nv_freq == 0:
            return 0
        return sqrt(365/self.nv_freq)*self.volatility

    @property
    @check
    def alpha(self) -> float:
        """区间年化alpha"""
        return self._calc_alphabeta[0]

    @property
    @check
    def beta(self) -> float:
        """区间beta"""
        return self._calc_alphabeta[1]

    @property
    def _calc_alphabeta(self) -> Tuple[float, float]:
        
        y = self._returns
        X = self._returns_benchmark
        
        if len(X) == 1:
            return 0,1
        
        X = sm.add_constant(X)
        mod = sm.OLS(y, X)
        res = mod.fit()
        # 区间alpha
        alpha = res.params.const
        # 年化alpha
        if alpha<-1:
            annulized_alpha = np.nan
        else:
            annulized_alpha = np.power(alpha+1, 365/self.nv_freq) - 1
        # beta
        beta = res.params.iloc[1]

        return annulized_alpha, beta

    @property
    @check
    def corr(self) -> float:
        """相关系数"""
        return self._returns.corr(self._returns_benchmark)

    # @cache
    def calc_drawdown(self, bm=False):
        if not bm:
            p_series = self.net_values
        elif bm:
            p_series = self.benchmark
        
        if len(p_series) == 0:
            return 0
        
        water_mark = p_series.cummax()
        drawdown = 1-p_series/water_mark
        return max(drawdown)

    @property
    @check
    def drawdown(self) -> float:
        """区间最大回撤"""
        return self.calc_drawdown()

    @property
    @check
    def drawdown_benchmark(self) -> float:
        """业绩基准区间最大回撤"""
        return self.calc_drawdown(bm=True)

    @property
    @check
    def relative_drawdown(self) -> float:
        """区间相对回撤"""
        return self.drawdown-self.drawdown_benchmark

    # @cache
    @check
    def sharpe(self, rf=0.015) -> float:
        """
        夏普比率
        parameters:
        rf:无风险收益率
        """
        if self.annulized_volatility == 0:
            return 0
        return (self.annulized_return-rf)/self.annulized_volatility

    @property
    @check
    def ir(self) -> float:
        """信息比率"""
        alpha, beta = self._calc_alphabeta
        exceed_return = self._returns - beta * self._returns_benchmark
        # 超额序列波动率
        std_er = exceed_return.std(ddof=1)
        # 年化超额波动率
        annulized_std_er = sqrt(365/self.nv_freq)*std_er
        # 信息比率
        if annulized_std_er == 0:
            return 0
        ir = alpha/annulized_std_er
        return ir

    @property
    @check
    def downside_deviation(self):
        ret = self._returns.copy()
        ret[ret > 0] = 0
        downside_variance = ret.pow(2).sum()/len(ret)
        downside_deviation = sqrt(downside_variance)
        return downside_deviation

    # @cache
    @check
    def sortino(self, mar=0.015) -> float:
        """
        索提诺比率
        -----------
        parameters:
        mar:minimal accepted return 要求最低回报率(目标回报率)

        note:
        下行方差 = 低于mar的return与mar之间的差值的平方/总样本数(自由度为0)
        下行标准差 = sqrt(下行方差)

        年化索提诺:(年化收益率-mar)/年化下行标准差
        """
        # TODO : mar应该对于周频数据生效，目前取0

        downside_deviation = self.downside_deviation
        if (downside_deviation == 0) or (self.nv_freq == 0):
            return 0 
        # 转化为年化下行波动率 公式：sqrt(days/avgdays_per_nv)*vol = sqrt(days*num_nv/interval)*vol = sqrt(num_nv/year_interval)*vol
        annulized_downside_deviation = sqrt(
            365/self.nv_freq)*downside_deviation

        if annulized_downside_deviation == 0:
            return 0
        return (self.annulized_return-mar)/annulized_downside_deviation

    def statistics(self, start_dt=None, end_dt=None, fields:List[str]=None) -> pd.Series:
        """
        产品区间指标
        fields:
            total_return
            annulized_return
        """
        if fields is None:
            fields = ["total_return","total_benchmark_return","annulized_return","annulized_excess_return","drawdown","relative_drawdown","volatility","annulized_volatility","alpha","beta","sharpe","ir","sortino"]
        if isinstance(fields,str):
            fields = [fields]
        
        if start_dt is not None:
            self.start = pd.Timestamp(start_dt)

        if end_dt is not None:
            self.end = pd.Timestamp(end_dt)

        temp_values = []
        for field in fields:
            value = getattr(self,field)
            if callable(value):
                value = value()
            temp_values.append(value)
        temp_values.append(getattr(self,"nv_start"))
        temp_values.append(getattr(self,"nv_end"))
        temp_values.append(getattr(self,"nv_num"))

        temp_values.extend([self.start,self.end])
        index = fields.copy()
        index.extend(["nv_start","nv_end","nv_num","start_date","end_date"])

        return pd.Series(data=temp_values,index=index)
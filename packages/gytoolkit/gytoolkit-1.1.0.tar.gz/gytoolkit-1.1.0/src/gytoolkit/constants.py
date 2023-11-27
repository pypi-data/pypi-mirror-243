"""
common constant definition used in gytoolkit
"""
from __future__ import annotations
from typing import Any, Optional, List, Dict, Literal
from dataclasses import dataclass, field
from datetime import datetime


class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        key = tuple(kwargs.get(attr) for attr in cls.__singleton_attributes__)
        if key not in cls.instances:
            cls.instances[key] = super().__call__(*args, **kwargs)
        else:
            # 更新属性
            instance = cls.instances[key]
            for attr, value in kwargs.items():
                if attr not in cls.__singleton_attributes__ and attr is not None:
                    setattr(instance, attr, value)
        return cls.instances[key]


@dataclass
class NetValueData(metaclass=SingletonMeta):
    __singleton_attributes__ = ("date", "prodcode")
    date: datetime
    prodcode: str
    netvalue: float
    cum_netvalue: float
    prodname: str = None
    netasset: float = None
    shares: float = None


@dataclass
class TradeData:
    client_id: str  # 交易客户
    prodcode: str  # 交易基金
    date: datetime  # 交易日期
    type: Literal["110-认购", "111-申购", "112-赎回"]  # 交易类型
    amount: Optional[float] = None  # 交易金额，认购、申购时必填
    shares: Optional[float] = None  # 交易份额，认购、赎回时必填

    def __post_init__(self):
        if self.type in ["110-认购", "111-申购"] and self.amount is None:
            raise ValueError("Amount must be provided for type 110-认购 or 111-申购")
        if self.type == "110-认购" and self.shares is None:
            raise ValueError("Shares must be provided for type 110-认购 or 112-赎回")


@dataclass
class FundEventData:
    """
    基金产品事件信息
    """

    prodcode: str
    date: datetime
    type: Literal["分红", "固定时点计提"]


@dataclass
class DividendData(FundEventData):
    """
    产品的分红信息
    """

    dividend_per_share: float
    def __post_init__(self):
        if self.type != "分红":
            raise ValueError("DividendData type must be '分红'")

@dataclass
class PerfFeeData(FundEventData):
    """
    产品的固定时点计提业绩报酬信息
    """
    type = "固定时点计提"


@dataclass
class ProdInfoData:
    """
    基金产品基础信息、费率、开放赎回等要素
    """

    prodcode: str
    name: str = None
    shortname: str = None
    manager_id: str = None
    personnel_id: List[str] = field(default_factory=list)
    est_date: datetime = None
    strategy: str = None
    size: float = 0
    benchmark: Dict[str, float] = field(default_factory=dict)
    # 费用设置
    # TODO:业绩报酬需要换成function(anuulized_return)
    custodian: str = None
    custodial_fee: float = 0
    outsourcer: str = None
    outsourcing_fee: float = 0
    subscription_fee: float = 0
    management_fee: float = 0
    performance_fee: float = 0
    commision_rate: float = 0
    close_period: str = None
    lockup_period: str = None
    buy_period: str = None
    buy_offset: str = None
    redemption_period: str = None
    redemption_offset: str = None
    risk_level: str = None
    perf_fee_lock_period = 0  # 基金的固定时点业绩报酬锁定期(部分基金180天以内的份额不提取)


@dataclass
class ManagerInfoData:
    manager_id: str
    name: str = None
    creditcode: str = None
    represent: str = None
    establish_date: datetime = None
    registered_date: float = None
    registered_address: str = None
    registered_capital: float = None
    paidin_capital: float = None
    office_address: str = None
    is_advisor: bool = False
    is_member: bool = False
    total_members: int = None
    research_members: int = None

    finance: List[ManagerFinanceData] = None
    holders: List[ManagerShareHolderData] = None
    departments: List[ManagerDeptData] = None
    awards: List[ManagerAwardData] = None
    coop: List[ManagerMarketData] = None
    personnels: List[PersonnelInfoData] = None


@dataclass
class ManagerFinanceData:
    manager_id: str
    year: int
    revenue: float = None
    net_profit: float = None
    assets: float = None
    liability: float = None


@dataclass
class ManagerShareHolderData:
    manager_id: str
    name: str
    type: str = None
    proportion: float = None
    direct: bool = True


@dataclass
class ManagerDeptData:
    manager_id: str
    name: str
    director_id: str = None
    members: float = None
    dept_description: str = None


@dataclass
class PersonnelInfoData:
    """
    高管,基金经理和核心投研,核心市场人员信息
    """

    id: str
    name: str
    position: str = None  # 职务
    birthday: datetime = None
    resume: str = None


@dataclass
class ManagerAwardData:
    """
    管理人获奖信息
    """

    manager_id: str
    name: str  # 奖项名称
    type: Literal["manager", "product", "personnel"] = None  # 获奖类型：管理人，产品，基金经理
    organization: str = None  # 颁奖机构
    datetime: str = None  # 获奖时间
    description: str = None  # 具体奖项描述


@dataclass
class ManagerMarketData:
    """
    管理人市场合作信息
    """

    manager_id: str
    organization: str  # 合作机构名称
    type: Literal["sale", "FOF", "invest", "seed"] = None  # 合作类型：代销，FOF，自营，种子
    datetime: datetime = None  # 合作时间
    scale: float = None  # 合作规模
    remark: str = None  # 具体合作描述

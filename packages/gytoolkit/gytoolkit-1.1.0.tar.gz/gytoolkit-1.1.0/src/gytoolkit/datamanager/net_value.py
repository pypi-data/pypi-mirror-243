import pandas as pd
from typing import List, Union
from functools import lru_cache
from .constants import NetValueData
from .dataloader import BaseDataLoader
from gytoolkit import ppwdbapi
from gytoolkit.mailparser import MailClient
from gytoolkit.utils import load_netvalue,save_netvalue
from .utils import get_otc_nv, ppwnvformatter


class NetValueLoader(BaseDataLoader):
    """
    净值数据来源(按优先级):
        1-邮箱解析
        2-ppwdbapi
        3-otc
        4-本地手工净值
    """
    def __init__(self) -> None:
        self.mailapi = {}
        super().__init__(NetValueData)

    def set_mailapi(self, username, password):
        mailclient = MailClient(username=username, password=password)
        self.mailapi[username] = mailclient

    def update_local_mail(self, depth=50):
        if "mail" not in self.source.keys():
            raise ValueError("Please set local mail file first.")
        
        local_mail_file = self.source["mail"]
        mail_api = self.mailapi
        if len(mail_api) > 0:
            for mailaccount, api in mail_api.items():
                headers = api.get_mail_header(lookin_depth=depth)
                nv_list = api.parse_mails(headers)
                save_netvalue(nv_list, local_mail_file)
        self.set_local_mail(local_mail_file)
        
    def load_mail(self, *args, **kwargs):
        return load_netvalue(self.source["mail"],df=True)
    
    def load_local(self, *args, **kwargs):
        return load_netvalue(self.source["local"],df=True)

    def load_otc(self, *args, **kwargs):
        otc_folder = self.source["otc"]
        return get_otc_nv(otc_folder,df=True)
    
    def load_ppw(self, *args, **kwargs):
        api:ppwdbapi = self.source["ppw"]

        if "reg_ids" in kwargs.keys():
            reg_ids = kwargs["reg_ids"]
            fund_info = api.get_fund(reg_ids=reg_ids)
            ppwnv = ppwnvformatter(api.get_netvalue(fund_info.index),df=True)
        else:
            ppwnv = ppwnvformatter(api.get_netvalue(*args, **kwargs),df=True)
        return ppwnv

    # def load(self, *args, df=True,**kwargs) -> Union[List[NetValueData], pd.DataFrame]:
    #     return super().load(*args,df=df,**kwargs)

    # def set_local_mail(self, local_mail_file):
    #     self.local_mail_file = local_mail_file
    #     self.get_local.cache_clear()
    
    # def set_local_otc(self, otc_folder_path):
    #     self.otc_folder_path = otc_folder_path
    #     self.get_local.cache_clear()
    
    # def set_addtional_file(self, additional_file):
    #     self.additional_file = additional_file
    #     self.get_local.cache_clear()

    # @lru_cache
    # def get_local(
    #     self, df=True
    # ) -> List[NetValueData]:
    #     # 按优先级顺序读取数据
    #     # 1、OTC数据
    #     if hasattr(self, "otc_folder_path"):
    #         otc_netvalues = get_otc_nv(self.otc_folder_path, df=True)
    #     else:
    #         otc_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
    #     # 2、手工净值
    #     if hasattr(self, "additional_file"):
    #         addtional_netvalues = load_netvalue(self.additional_file, df=True)
    #     else:
    #         addtional_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
    #     # 3、邮箱数据
    #     if hasattr(self, "local_mail_file"):
    #         mail_netvalues = load_netvalue(self.local_mail_file, df=True)
    #     else:
    #         mail_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     local_netvalues = otc_netvalues.combine_first(addtional_netvalues)
    #     local_netvalues = local_netvalues.combine_first(mail_netvalues)

    #     if df:
    #         return local_netvalues
    #     else:
    #         return [NetValueData(**row) for index, row in local_netvalues.reset_index().iterrows()]

    # def load(
    #     self,
    #     prodcode,
    #     df=True,
    # ) -> Union[List[NetValueData], pd.DataFrame]:
    #     local_netvalues = self.get_local()
    #     idx = pd.IndexSlice
    #     try:
    #         local_netvalue = local_netvalues.loc[idx[:, prodcode],]
    #     except:
    #         local_netvalue = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     ppwdbapi = self.api.get("ppwdbapi")
    #     if ppwdbapi:
    #         fund_info = ppwdbapi.get_fund(reg_ids=prodcode)
    #         ppwnv = ppwnvformatter(ppwdbapi.get_netvalue(fund_info.index))
    #     else:
    #         ppwnv = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

    #     net_value = ppwnv.combine_first(local_netvalue)
    #     if df:
    #         return net_value
    #     else:
    #         return [NetValueData(**row) for index, row in net_value.reset_index().iterrows()]

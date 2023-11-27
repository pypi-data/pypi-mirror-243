from dataclasses import dataclass
from datetime import datetime
from gytoolkit.constants import NetValueData

@dataclass
class MailHeaderData():
    Date:datetime
    sender_name:str
    sender_addr:str
    receriver_name:str
    receriver_addr:str
    cc_name:str
    cc_addr:str
    Subject:str


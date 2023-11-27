from typing import Dict
from .product import Product
from .constants import ManagerInfoData

class Manager:
    def __init__(self,id):
        self.id: str = id,
        self.info = ManagerInfoData
        self.products: Dict[str, Product] = {}
    
    def add_product(self, prod: Product) -> None:
        self.products[prod.info.name] = prod

    def remove_product(self, prod_name: str) -> None:
        if prod_name in self.products:
            self.products.pop(prod_name)
    
    @property
    def AUM(self) -> float:
        aum = 0
        for p in self.products.values():
            aum += p.info.size
        return aum

    
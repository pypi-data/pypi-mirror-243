from typing import List, Dict
import pandas as pd
from .client import Client
from .product import Product
from .constants import TradeData, DividendData
from .position import Position


class Broker:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.clients: Dict[str, Product] = {}

    def add_product(self, product: Product):
        self.products[product.code] = product

    def get_product(self, prodcode):
        # Get the fund from the transaction
        product = self.products.get(prodcode)
        if not product:
            product = Product(prodcode)
            self.add_product(product)
        return product

    def add_client(self, client: Client):
        self.clients[client.id] = client

    def get_client(self, client_id):
        # Get the fund from the transaction
        client = self.clients.get(client_id)
        if not client:
            client = Client(client_id)
            self.add_client(client)
        return client

    def process_trade(self, trade: TradeData):
        # Get the fund from the transaction
        product = self.get_product(trade.prodcode)
        client = self.get_client(trade.client_id)

        # If it's a purchase transaction, create a new position
        if trade.type in ("110-认购", "111-申购"):
            if trade.type == "110-认购":
                new_position = Position(
                    client_id=client.id,
                    prodcode=product.code,
                    creation_date=trade.date,
                    cost=trade.amount,
                    init_shares=trade.shares,
                    init_price=1,
                    init_cum_price=1,
                )

            if trade.type == "111-申购":
                current_nv = product.get_net_value(trade.date)
                new_position = Position(
                    client_id=client.id,
                    prodcode=product.code,
                    creation_date=trade.date,
                    cost=trade.amount,
                    init_shares=trade.shares,
                    init_price=current_nv.netvalue,
                    init_cum_price=current_nv.cum_netvalue,
                )

            client.add_position(new_position)
            product.add_position(new_position)  # Added this line

        # If it's a redemption transaction, remove the shares from the position
        if trade.type == "112-赎回":
            if trade.shares is None:
                # 全仓赎回
                remaining_shares = sum(
                    [
                        position.shares
                        for position in client.positions
                        if position.prodcode == trade.prodcode
                    ]
                )
            else:
                remaining_shares = trade.shares
            # Assuming positions have a creation_date attribute
            for position in sorted(client.positions, key=lambda p: p.creation_date):
                if (
                    position.prodcode == trade.prodcode and not position.closed
                ):  # Added a check for the closed attribute
                    if position.shares <= remaining_shares:
                        # Close the entire position
                        remaining_shares -= position.shares
                        # update the redeemed amount
                        position.redempt(trade.date, position.shares)
                    else:
                        # Remove part of the position
                        # update the redeemed amount
                        if position.shares < remaining_shares + 0.01:
                            position.redempt(trade.date, position.shares)
                        else:
                            position.redempt(trade.date, remaining_shares)
                        remaining_shares = 0
                if remaining_shares == 0:
                    break

        client.add_trade(trade)
        product.trades.append(trade)

    def process_dividend(self, dividend_data: DividendData):
        # Get the fund from the transaction
        product = self.get_product(dividend_data.prodcode)
        nvdata = product.get_net_value(dividend_data.date)

        # Calculate the dividend amount for each position and handle accordingly
        for position in product.positions:
            if not position.closed and position.creation_date <= dividend_data.date:
                position.handle_dividend(nvdata, dividend_data)

        # Add the dividend to the fund's dividends list
        product.add_dividend(dividend_data)

    def extract_perffee(self, prodcode: str, date):
        # Get the fund from the transaction
        product = self.get_product(prodcode)
        nvdata = product.get_net_value(date)

        # extract fixed time performance fee
        for position in product.positions:
            if not position.closed and position.creation_date <= date - pd.Timedelta(
                product.info.perf_fee_lock_period, "D"
            ):
                position.extract_fixedtime_perffee(nvdata)
        
        product.fixedtime_perfees.append(date)

    def set_divident_method(self, clent_id: str, prodcode:str, dividend_reinvestment):
        client = self.get_client(clent_id)
        for position in client.positions:
            if position.prodcode == prodcode:
                position.dividend_reinvestment = dividend_reinvestment
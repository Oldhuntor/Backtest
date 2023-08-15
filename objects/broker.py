"""
Broker objects, act as a trader
"""

class Broker():
    def __init__(self,startcash):
        self.cash = startcash # initial cash
        self.position = 0
        self.action_log = []

    def buy(self, price, amount, date):
        self.cash -= price*amount
        self.position += amount
        print(f"buy for {amount}, at price {price}, on date {date}")
        self.action_log.append('buy')

    def sell(self, price, amount, date):
        self.cash += price*amount
        self.position -= amount
        print(f"sell for {amount}, at price {price}, on date {date}")
        self.action_log.append('sell')

    def hold(self):
        self.action_log.append('hold')



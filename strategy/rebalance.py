import numpy as np

from strategy.template.strategy_template_crypto import templateCrypto


class rebalance(templateCrypto):
    """
    rebalance strategy for two symbols
    frequency: 1d
    """
    def __init__(self, broker, params):

        super().__init__(broker, params)


    def strategy(self, ticks):
        tick1 = ticks[self.symbols[0]]
        tick2 = ticks[self.symbols[1]]
        date = tick1['time']
        open1 = np.float(tick1['open'])
        open2 = np.float(tick2['open'])
        if not self.start:
            # buy initial amount of two symbol
            init_cash = self.agent.cash

            amount1 = init_cash/2/open1
            amount2 = init_cash/2/open2

            self.agent.buy(self.symbols[0], open1,amount1,date)
            self.agent.buy(self.symbols[1], open2,amount2,date)

            self.start = True
            self.recorder(ticks, date)
            return

        if self.end:
            total_value = self.agent.position[self.symbols[0]] * open1 + self.agent.position[self.symbols[1]] * open2
            print(f"end assets value: {total_value}")
            self.recorder(ticks, date)
            return

        # compare in usdt
        assetValue1 = open1*self.agent.position[self.symbols[0]]
        assetValue2 = open2*self.agent.position[self.symbols[1]]
        diff = assetValue1 - assetValue2
        amount1 = abs(diff / open1)
        amount2 = abs(diff / open2)

        print(f"current value: {self.symbols[0]}: {assetValue1}, {self.symbols[1]}: {assetValue2}")
        # rebalance
        if diff > 0:
            # asset1 sell, asset2 buy

            self.agent.sell(self.symbols[0], price=open1, amount=amount1, date=date)
            self.agent.buy(self.symbols[1], price=open2, amount=amount2, date=date)

        else:

            self.agent.buy(self.symbols[0], price=open1, amount=amount1, date=date)
            self.agent.sell(self.symbols[1], price=open2, amount=amount2, date=date)

        self.recorder(ticks, date)














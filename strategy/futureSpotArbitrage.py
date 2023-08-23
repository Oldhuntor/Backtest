from strategy.template.strategy_template_crypto import templateCrypto

class arbitrage(templateCrypto):
    """

    期现套策略
    大于3%开仓，开仓后每缩小1%平1/3的仓位
    币本位合约开1倍杠杆
    ex：
    持有10个btc spot
    开币本位合约10个BTCUSD_231229


    目前还没有支持合约计算的broker
    解决方案：
    写一个支持开平仓的broker并整合到原本的broker中


    """

    def __init__(self, broker, params):

        super().__init__( broker, params)

    def readParams(self):
        self.openThreshold = self.params['openThreshold'] # 3%
        self.closeGap = self.params['closeGap'] # 1%
        self.openRate = self.params['openRate']
        self.closeRate = self.params['closeRate']
        self.pullBack = self.params['pullBack']
        self.leverage = self.params['leverage']
        self.futureSymbol = self.symbols[0]
        self.spotSymbol = self.symbols[1]


    def updatePositionStatus(self):
        pass


    def strategy(self, ticks:dict):

        # futures
        tickFuture = ticks[self.futureSymbol]

        # Spots
        tickSpot = ticks[self.spotSymbol]

        priceDiff = (tickFuture['open'] - tickSpot['open'])/tickSpot['open']

        # Direction short futures and long spot
        if priceDiff > self.params['openThreshold']:
            pass

















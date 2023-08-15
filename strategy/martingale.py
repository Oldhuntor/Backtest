from strategy.template.strategy_template import template


class martingale(template):

    def __init__(self,startdate, endate,
                 code, broker, params):

        super().__init__(startdate, endate,
                         code, broker, params)


    def strategy(self, tick):
        open = tick['open']
        high = tick['high']
        low = tick['low']
        close = tick['close']
        date = tick['trade_date']
        self.price_log.append(open)

        if not self.start:
            # buy the initial amount
            amount = (self.agent.cash) * 0.1 / open
            print(f"buy the initial amount")
            self.agent.buy(open, amount, date=date)
            self.recorder(open, date)
            self.start = True
            return

        if self.end:
            print("sell all the position at the end of the strategy")
            self.agent.sell(open, self.agent.position, date)
            self.recorder(open, date)
            return

        # reach take profit margin, execute sell
        if (open - self.price_log[0]) / open >= self.params['takeprofit'] and self.agent.position > 0:
            self.agent.sell(price=open, amount=self.agent.position, date=date)
            self.recorder(open, date)
            self.price_log = []

            return

        # price drop below the threshold, execute buy
        if (open - self.price_log[0]) / open <= self.params['increasePos']:

            amount = ((self.agent.position) * 2)

            if self.agent.position > 0 and (self.agent.cash - amount * open) > 0:
                self.agent.buy(price=open, amount=(self.agent.position) * 2, date=date)
                self.price_log = []
                self.recorder(open, date)

            elif self.agent.position == 0:
                # 购买初始仓位
                amount = (self.agent.cash) * 0.1 / open
                print(f"buy the initial amount again!")
                self.agent.buy(open, amount, date=date)
                self.price_log = []
                self.recorder(open, date)

            else:
                print("out of cash")
                self.agent.hold()
                self.recorder(open, date)
            return
        self.agent.hold()
        self.recorder(open, date)













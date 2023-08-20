from strategy.template.strategy_template_Ashare import template

class arbitrage(template):

    def __init__(self,startdate, endate,
                 code, broker, params):

        super().__init__(startdate, endate,
                         code, broker, params)



    def init(self):
        pass


    def strategy(self, tickA, tickB):
        pass





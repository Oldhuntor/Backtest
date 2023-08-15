from objects.broker import Broker
from strategy.martingale import martingale


params = {
    'takeprofit': 0.05,
    'increasePos': -0.05,
}

cash = 100000
startdate = '20201227'
endate = '20230731'
stock = '601908'
strategy = 'matingale'


if __name__ == '__main__':

    broker = Broker(cash)
    strategy = martingale(startdate, endate, stock, broker, params)
    strategy.run()
    strategy.plot()

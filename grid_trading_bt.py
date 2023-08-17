from objects.broker import Broker
from strategy.grid_trading import grid


params = {
    'grid_step': 0.01,
    'upper_price': 15,
    'lower_price': 6,
    'leverage':1,
}

cash = 100000
startdate = '20201227'
endate = '20230731'
stock = '601908'


if __name__ == '__main__':

    broker = Broker(cash)
    strategy = grid(startdate, endate, stock, broker, params)
    strategy.run()
    strategy.plot()
    strategy.cal_performance()

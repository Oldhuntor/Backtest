from objects.broker import BrokerMulti
from strategy.rebalance import rebalance


params = {
    'symbols': ["BTCUSDT","ETHUSDT"],
    'startDate': '2017-08-22',
    'endDate': '2023-08-20',
    'frequency': "1d",
    'exchange':'binance',
}

cash = 100000
startdate = '20201227'
endate = '20230731'


if __name__ == '__main__':

    broker = BrokerMulti(cash)
    strategy = rebalance(broker, params)
    strategy.run()
    # strategy.plot()
    # strategy.cal_performance()

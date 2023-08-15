import pandas as pd
import matplotlib.pyplot as plt
from functions.get_A_stock import get_stock_pro
from objects.broker import Broker

params = {}

class template():
    def __init__(self, startdate, endate, code, broker: Broker, params):
        self.data = get_stock_pro(code,startdate,endate)
        self.stockName = code
        self.start = False
        self.end = False
        self.price_log = []
        self.agent = broker
        self.record = []
        self.params = params
        self.init()

    def run(self):
        for index in range(len(self.data)):
            tick = self.data.iloc[index]
            if index == len(self.data)-1:
                self.end = True
            self.strategy(tick)

    # customized init function for strategy
    def init(self):
        pass

    def strategy(self, tick):
        """"""
        pass

    def plot(self):
        def convert_to_datetime(date_str):
            return pd.to_datetime(date_str, format='%Y%m%d')


        self.data['trade_date'] = self.data['trade_date'].apply(convert_to_datetime)

        df = pd.DataFrame(self.record)
        df['action'] = self.agent.action_log
        df['date'] = df['date'].apply(convert_to_datetime)

        # Create a subplot with 3 rows and 1 column
        fig, axs = plt.subplots(4, 1, figsize=(8, 10))

        # Plot Position
        axs[0].plot(df['date'], df['position'])
        axs[0].set_ylabel('Position')
        axs[0].grid()

        # Plot Market Price
        axs[1].plot(self.data['trade_date'], self.data['open'], color='black')
        axs[1].set_ylabel('Market Price')
        # Mark buy and sell actions on Market Price plot
        buy_data = df[df['action'] == 'buy']
        sell_data = df[df['action'] == 'sell']
        axs[1].scatter(buy_data['date'], buy_data['market'], color='green', label='Buy', marker='^')
        axs[1].scatter(sell_data['date'], sell_data['market'], color='red', label='Sell', marker='v')

        # Customize the legend
        legend = axs[1].legend(loc='upper right')
        legend.get_frame().set_facecolor('white')  # Set background color of the legend box
        axs[1].grid()

        axs[2].plot(df['date'], df['unrealizedProfit'], color='b')
        axs[2].set_ylabel('unrealizedProfit')
        axs[2].grid()

        # Plot Cash
        axs[3].plot(df['date'], df['cash'], color='g')
        axs[3].set_ylabel('Cash')
        axs[3].set_xlabel('date')
        axs[3].grid()

        plt.suptitle(f'Backtesting stock:{self.stockName}', fontsize=16)

        # Adjust layout to prevent overlapping of labels
        plt.tight_layout()

        # Show the plot
        plt.show()

    def cal_performance(self):

        pass

    def recorder(self, price, date):
        unrealizedProfit = self.agent.position*price + self.agent.cash
        record = {'cash': self.agent.cash, 'position': self.agent.position, 'market': price, 'date': date, "unrealizedProfit":unrealizedProfit}
        self.record.append(record)










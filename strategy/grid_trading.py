from strategy.template.strategy_template_Ashare import template
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class grid(template):

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

        if not self.start:
            if open > self.upper_price or open < self.lower_price:
                print(f"price {open} reach the upper: {self.upper_price} or lower : {self.lower_price} limit of the grid")
                return
            # initial order
            self.last_trade_price = open
            self.upper_grid_price = open*(1+self.grid_step)
            self.lower_grid_price = open*(1-self.grid_step)

            # initial position
            tar_value = ((math.log(self.upper_price/open))/(math.log(1+self.grid_step)))*self.grid_value
            tar_pos = tar_value/open
            self.agent.buy(open, tar_pos, date)
            self.recorder(open, date)
            self.upper_grid_price = self.last_trade_price * (1 + self.grid_step)
            self.lower_grid_price = self.last_trade_price * (1 - self.grid_step)
            self.start = True

            return

        if open > self.upper_grid_price and self.upper_grid_price < self.upper_price:
            amount = self.grid_value/open
            self.agent.sell(open, amount, date)
            self.recorder(self.upper_grid_price, date)
            self.last_trade_price = open
            # set new limit order
            self.upper_grid_price = self.last_trade_price * (1 + self.grid_step)
            self.lower_grid_price = self.last_trade_price * (1 - self.grid_step)
            return

        elif open < self.lower_grid_price and self.lower_grid_price > self.lower_price:
            amount = self.grid_value/open
            self.agent.buy(open, amount, date)
            self.recorder(self.lower_grid_price, date)
            self.last_trade_price = open
            # set new limit order
            self.upper_grid_price = self.last_trade_price * (1 + self.grid_step)
            self.lower_grid_price = self.last_trade_price * (1 - self.grid_step)
            return

        else:
            self.agent.hold()
            self.recorder(open, date)



    def init(self):

        self.grid_step = self.params['grid_step']
        self.upper_price = self.params['upper_price']
        self.lower_price = self.params['lower_price']
        self.leverage = self.params['leverage']
        self.total_grid = math.log(self.upper_price / self.lower_price) / math.log(1 + self.grid_step)
        self.grid_value = int(self.agent.cash / self.total_grid) # 每网格金额


    def plot(self):
        def convert_to_datetime(date_str):
            return pd.to_datetime(date_str, format='%Y%m%d')
        self.data['trade_date'] = self.data['trade_date'].apply(convert_to_datetime)

        df = pd.DataFrame(self.record)
        df['action'] = self.agent.action_log
        df['date'] = df['date'].apply(convert_to_datetime)

        # Create a subplot with 4 rows and 1 column
        fig, axs = plt.subplots(4, 1, figsize=(8, 10))

        # Plot Position
        axs[0].plot(df['date'], df['position'])
        axs[0].set_ylabel('Position')
        axs[0].grid()

        # Plot Market Price
        axs[1].plot(self.data['trade_date'], self.data['open'], color='black')

        # axs[1].axhline(y=self.upper_price, color='green', linestyle='--', label='Horizontal Line')
        # axs[1].axhline(y=self.lower_price, color='green', linestyle='--', label='Horizontal Line')

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

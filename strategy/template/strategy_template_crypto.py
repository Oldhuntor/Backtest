import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions.get_A_stock import get_stock_pro
from objects.broker import BrokerMulti
from data.database.sqlite_server import DBpath,connectSqlite

params = {}

class templateCrypto():
    """
    支持2个及以上的标的同时持有
    """
    def __init__(self,broker: BrokerMulti, params):
        self.sqlconn = connectSqlite(DBpath)
        self.start = False
        self.end = False
        self.agent = broker
        self.record = {}
        self.params = params
        self.strategy_name = ""
        self.init()
        self.readParams()

    def run(self):
        length = len(self.data[self.symbols[0]])
        for index in range(length):
            ticks = {}
            for symbol in self.symbols:
                ticks[symbol] = self.data[symbol].iloc[index]
            if index == length-1:
                self.end = True
            self.strategy(ticks)

    # customized init function for strategy
    def init(self):
        startDate = pd.Timestamp(self.params['startDate'])
        endDate = pd.Timestamp(self.params['endDate'])
        frequency = self.params['frequency']
        exchange = self.params['exchange']
        self.symbols = self.params['symbols'] # list
        self.data = {}

        # fetch all the data
        for symbol in self.symbols:
            table_name = f"{exchange}_{symbol}_{frequency}"

            # 执行 SQL 查询
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.sqlconn)

            # filter the data by date
            df['time'] = pd.to_datetime(df['time'])
            filtered_df = df[(df['time'] >= startDate) & (df['time'] <= endDate)]
            filtered_df.drop_duplicates(inplace=True)
            self.data[symbol] = filtered_df

        self.sqlconn.close()

    def readParams(self):
        pass

    def strategy(self, ticks:dict):
        """"""
        pass

    def plot(self):
        """
        draw the position graph together in one graph
        draw hte
        """

        # 处理数据
        data = []
        for symbol, records in self.record.items():
            for record in records:
                record['symbol'] = symbol
                data.append(record)

        df = pd.DataFrame(data)
        df['total_unrealizedProfit'] = df.groupby('date')['unrealizedProfit'].transform('sum')

        # 创建画布和子图
        fig, axs = plt.subplots(2, 1, figsize=(10, 12))

        # 绘制position柱状图
        df_position = df.pivot(index='date', columns='symbol', values='position')
        df_position.plot(kind='bar', ax=axs[0])
        axs[0].set_ylabel('Position')
        axs[0].set_xlabel('Date')
        axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45)
        axs[0].legend()

        # 绘制总的unrealized profit折线图
        df_total_unrealizedProfit = df.groupby('date')['unrealizedProfit'].sum().reset_index()
        axs[1].plot(df_total_unrealizedProfit['date'], df_total_unrealizedProfit['unrealizedProfit'], marker='o')
        axs[1].set_ylabel('Total Unrealized Profit')
        axs[1].set_xlabel('Date')
        axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45)
        symbolStr = ""
        for symbol in self.symbols:
            symbolStr += symbol
            symbolStr += ';'
        plt.suptitle(f'Backtesting, strategy: {self.strategy_name}, symbols :{symbolStr}', fontsize=16)

        # Adjust layout to prevent overlapping of labels
        plt.tight_layout()

        # Show the plot
        plt.show()

    def cal_performance(self):

        self.data['trade_date'] = self.data['trade_date'].apply(self.convert_to_datetime)

        df = pd.DataFrame(self.record)
        df['date'] = df['date'].apply(self.convert_to_datetime)

        # Calculate daily returns
        df['Portfolio_Return'] = df['unrealizedProfit'].pct_change()

        # Calculate cumulative returns
        df['Cumulative_Portfolio_Return'] = (1 + df['Portfolio_Return']).cumprod()

        # Calculate annualized return
        portfolio_annual_return = (df['Cumulative_Portfolio_Return'].iloc[-1]) ** (365 / len(df)) - 1

        # Calculate volatility (standard deviation of returns)
        portfolio_volatility = df['Portfolio_Return'].std()

        # Calculate Sharpe ratio
        risk_free_rate = 0.02  # Assume a risk-free rate
        portfolio_sharpe_ratio = (portfolio_annual_return - risk_free_rate) / portfolio_volatility

        # Calculate maximum drawdown
        df['Portfolio_Drawdown'] = (1 - df['Cumulative_Portfolio_Return'] / df['Cumulative_Portfolio_Return'].cummax())
        max_portfolio_drawdown = df['Portfolio_Drawdown'].max()

        # Print results
        print(f"Portfolio Annual Return: {portfolio_annual_return:.2%}")
        print(f"Portfolio Volatility: {portfolio_volatility:.2%}")
        print(f"Portfolio Sharpe Ratio: {portfolio_sharpe_ratio:.2f}")
        print(f"Maximum Portfolio Drawdown: {max_portfolio_drawdown:.2%}")

    def recorder(self, ticks, date):
        """
        record the process separately
        """
        for symbol in self.symbols:
            if symbol not in self.record.keys():
                self.record[symbol] = []
            symbol_position = np.around(self.agent.position[symbol], 3)
            symbol_price = np.float(ticks[symbol]['open'])
            symbol_unrealizedProfit = np.around(symbol_position*symbol_price, 3)
            record = {'cash': np.around(self.agent.cash, 3), 'position': symbol_position, 'date': date, "unrealizedProfit": symbol_unrealizedProfit}
            self.record[symbol].append(record)

    def convert_to_datetime(self, date_str):
        return pd.to_datetime(date_str, format='%Y%m%d')





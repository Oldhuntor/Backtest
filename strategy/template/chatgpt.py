class TradingSimulator:
    def __init__(self, initial_balance=100000, margin_rate=0.1, leverage=10):
        self.balance = initial_balance
        self.positions = {}  # 用字典来维护不同标的的仓位信息
        self.margin_rate = margin_rate
        self.leverage = leverage

    def open_position(self, symbol, price, quantity, is_long):
        if symbol in self.positions:
            return "Position for this symbol already exists. Close existing position first."

        cost = price * quantity / self.leverage
        required_margin = cost * self.margin_rate

        if required_margin > self.balance:
            return "Insufficient margin."

        self.balance -= required_margin
        self.positions[symbol] = {
            'position': quantity if is_long else -quantity,
            'entry_price': price,
            'liquidation_price': self.calculate_liquidation_price(price, quantity, is_long)
        }
        return f"Position for {symbol} opened."

    def close_position(self, symbol, price, quantity=None):
        if symbol not in self.positions:
            return "No position for this symbol."

        position_info = self.positions[symbol]
        current_position = position_info['position']
        entry_price = position_info['entry_price']

        if quantity is None:
            quantity = abs(current_position)

        if quantity > abs(current_position):
            return "Cannot close more than current position."

        profit_loss = (price - entry_price) * current_position * self.leverage

        if quantity == abs(current_position):
            self.balance += profit_loss
            del self.positions[symbol]
        else:
            partial_position = quantity if current_position > 0 else -quantity
            self.balance += (price - entry_price) * partial_position * self.leverage
            position_info['position'] -= partial_position
            position_info['liquidation_price'] = self.calculate_liquidation_price(
                entry_price, abs(position_info['position']), current_position > 0
            )

        return f"Position for {symbol} closed. P/L: {profit_loss:.2f}"

    def calculate_liquidation_price(self, entry_price, quantity, is_long):
        if quantity != 0:
            if is_long:
                return entry_price - (self.balance / (quantity * self.margin_rate * self.leverage))
            else:
                return entry_price + (self.balance / (quantity * self.margin_rate * self.leverage))
        else:
            return None


# 使用示例
simulator = TradingSimulator()

# 开仓不同标的
print(simulator.open_position("AAPL", 150, 50, is_long=True))
print(simulator.open_position("GOOG", 2500, 10, is_long=False))

# 平仓不同标的的部分仓位
print(simulator.close_position("AAPL", 155, quantity=30))
print(simulator.close_position("GOOG", 2600))

print("余额:", simulator.balance)

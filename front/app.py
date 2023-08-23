from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/huangxuanhao/Desktop/database/BinanceData.db'  # 连接到 SQLite 数据库
db = SQLAlchemy(app)

class binance_BTCUSDT_1h(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    # 添加其他字段，根据表格结构进行适当的修改

@app.route('/')
def index():
    btcusdt_data = binance_BTCUSDT_1h.query.all()
    return render_template('index.html', btcusdt_data=btcusdt_data)

if __name__ == '__main__':
    app.run(debug=True)

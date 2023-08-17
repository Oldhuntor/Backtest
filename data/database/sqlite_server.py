import sqlite3

DBpath = '/Users/huangxuanhao/Desktop/database/BinanceData.db'

def connectSqlite(path):
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('/Users/huangxuanhao/Desktop/database/BinanceData.db')
    return conn

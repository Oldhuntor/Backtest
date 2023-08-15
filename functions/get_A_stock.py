"""
Use tushare package to get data of chinese stocks
"""
import tushare as ts

# tushare token
token = '8de79483bd18bf182df0b78a38f89c48f68cc0a6cdcd7694a35e4d7e'
ts.set_token(token)
pro = ts.pro_api()


def get_stock_pro(code, startdate, endate):
    code = code + '.SH'
    df = pro.daily(ts_code=code, start_date=startdate, end_date=endate)
    df = df.iloc[::-1]
    return df


import akshare as ak
import pandas as pd

# stock_us_daily_df = ak.stock_us_daily(symbol="QQQ", adjust="qfq")
stock_us_daily_df = ak.stock_us_daily(symbol="QQQ", adjust="")

print(stock_us_daily_df)
stock_us_daily_df.set_index("date", inplace=True)

# 计算涨跌幅
# 涨跌幅 = (当天收盘价 - 前一天收盘价) / 前一天收盘价 * 100%
stock_us_daily_df['涨跌幅(%)'] = stock_us_daily_df['close'].pct_change() * 100

print("\n添加涨跌幅后的数据:")
print(stock_us_daily_df)

stock_us_daily_df.to_csv("QQQ_daily.csv", encoding="utf-8-sig")

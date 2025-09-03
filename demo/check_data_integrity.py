import pandas as pd
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

# 读取QQQ数据
df = pd.read_csv('QQQ_daily.csv')

# 确保日期列是datetime格式（注意这里使用'date'而不是'Date'）
df['date'] = pd.to_datetime(df['date'])

# 获取数据的起始和结束日期
start_date = df['date'].min()
end_date = df['date'].max()

print(f"数据时间范围: {start_date.date()} 到 {end_date.date()}")
print(f"总记录数: {len(df)}")

# 获取NYSE交易日历
nyse = mcal.get_calendar('NYSE')
trading_days = nyse.valid_days(start_date=start_date, end_date=end_date)

# 将交易日转换为set以便快速查找
trading_days_set = set(trading_days.date)
data_days_set = set(df['date'].dt.date)

# 检查是否有缺失的交易日
missing_days = trading_days_set - data_days_set
if missing_days:
    print("\n缺失的交易日:")
    for day in sorted(missing_days):
        print(day)
    print(f"\n总共缺失 {len(missing_days)} 个交易日")
else:
    print("\n没有发现缺失的交易日！数据完整性良好。")

# 检查数据是否有重复的日期
duplicates = df[df['date'].duplicated()]
if not duplicates.empty:
    print("\n发现重复的日期:")
    print(duplicates['date'].sort_values())
else:
    print("\n没有发现重复的日期。")
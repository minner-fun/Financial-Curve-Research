import pandas as pd
from datetime import datetime, timedelta

# 读取QQQ数据
df = pd.read_csv('QQQ_daily.csv')

# 确保日期列是datetime格式
df['date'] = pd.to_datetime(df['date'])

# 获取数据的起始和结束日期
start_date = df['date'].min()
end_date = df['date'].max()

print(f"数据时间范围: {start_date.date()} 到 {end_date.date()}")
print(f"总记录数: {len(df)}")

# 生成所有工作日（周一到周五）
all_days = pd.date_range(start=start_date, end=end_date, freq='B')
all_days_set = set(all_days.date)
data_days_set = set(df['date'].dt.date)

# 检查工作日中缺失的日期
missing_workdays = all_days_set - data_days_set
if missing_workdays:
    print("\n工作日中缺失的日期（可能包含节假日）:")
    for day in sorted(missing_workdays):
        print(day)
    print(f"\n总共缺失 {len(missing_workdays)} 个工作日（包含节假日）")
else:
    print("\n在工作日中没有发现缺失的日期！")

# 检查数据是否有重复的日期
duplicates = df[df['date'].duplicated()]
if not duplicates.empty:
    print("\n发现重复的日期:")
    print(duplicates['date'].sort_values())
else:
    print("\n没有发现重复的日期。")

# 检查日期间隔
df_sorted = df.sort_values('date')
date_diffs = df_sorted['date'].diff()
unusual_gaps = date_diffs[date_diffs > timedelta(days=3)]
if not unusual_gaps.empty:
    print("\n发现异常的日期间隔（超过3天）:")
    for idx in unusual_gaps.index:
        prev_date = df_sorted.loc[idx-1, 'date'].date()
        curr_date = df_sorted.loc[idx, 'date'].date()
        gap_days = (curr_date - prev_date).days
        print(f"从 {prev_date} 到 {curr_date} 间隔了 {gap_days} 天")

import pandas as pd
import numpy as np
from datetime import datetime

# 读取带有投资数据的CSV文件
df = pd.read_csv('QQQ_daily_with_investment.csv')

# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 计算3倍涨跌幅
df['3x_return_pct'] = df['涨跌幅(%)'] * 3

# 计算3倍杠杆的收盘价
# 第一天的3倍收盘价等于原始收盘价
df['3x_close'] = 0.0
df.loc[0, '3x_close'] = df.loc[0, 'close']

# 从第二天开始，根据3倍涨跌幅计算3倍收盘价
for i in range(1, len(df)):
    if pd.notna(df.loc[i, '3x_return_pct']):
        # 3倍收盘价 = 前一天3倍收盘价 * (1 + 3倍涨跌幅/100)
        df.loc[i, '3x_close'] = df.loc[i-1, '3x_close'] * (1 + df.loc[i, '3x_return_pct'] / 100)
    else:
        df.loc[i, '3x_close'] = df.loc[i-1, '3x_close']

# 计算3倍杠杆的定投收益
# 重新计算定投逻辑，但使用3倍收盘价
df['year_month'] = df['date'].dt.to_period('M')

# 初始化3倍投资相关列
df['3x_monthly_investment'] = 0.0
df['3x_shares_bought'] = 0.0
df['3x_cumulative_investment'] = 0.0
df['3x_cumulative_shares'] = 0.0
df['3x_portfolio_value'] = 0.0

# 定投参数
monthly_investment = 1000.0

# 处理每个月的3倍杠杆定投
cumulative_investment_3x = 0.0
cumulative_shares_3x = 0.0

# 按年月分组处理
for year_month, group in df.groupby('year_month'):
    # 找到该月26号或之后的第一个交易日
    target_day = 26
    month_data = group.sort_values('date')
    
    # 寻找26号或之后的第一个交易日
    investment_day = None
    for _, row in month_data.iterrows():
        if row['date'].day >= target_day:
            investment_day = row.name
            break
    
    # 如果该月没有26号之后的交易日，取该月最后一个交易日
    if investment_day is None:
        investment_day = month_data.index[-1]
    
    # 在投资日进行定投（使用3倍收盘价）
    investment_price_3x = df.loc[investment_day, '3x_close']
    shares_to_buy_3x = monthly_investment / investment_price_3x
    
    # 更新累计数据
    cumulative_investment_3x += monthly_investment
    cumulative_shares_3x += shares_to_buy_3x
    
    # 更新该月投资日的数据
    df.loc[investment_day, '3x_monthly_investment'] = monthly_investment
    df.loc[investment_day, '3x_shares_bought'] = shares_to_buy_3x
    
    # 更新该月所有交易日的累计数据和投资组合价值
    for idx in month_data.index:
        if idx <= investment_day:
            # 投资日及之前的日期
            if idx == investment_day:
                df.loc[idx, '3x_cumulative_investment'] = cumulative_investment_3x
                df.loc[idx, '3x_cumulative_shares'] = cumulative_shares_3x
            else:
                # 投资日之前，使用上月的累计数据
                df.loc[idx, '3x_cumulative_investment'] = cumulative_investment_3x - monthly_investment
                df.loc[idx, '3x_cumulative_shares'] = cumulative_shares_3x - shares_to_buy_3x
        else:
            # 投资日之后的日期，使用当月投资后的累计数据
            df.loc[idx, '3x_cumulative_investment'] = cumulative_investment_3x
            df.loc[idx, '3x_cumulative_shares'] = cumulative_shares_3x
        
        # 计算3倍杠杆投资组合价值
        df.loc[idx, '3x_portfolio_value'] = df.loc[idx, '3x_cumulative_shares'] * df.loc[idx, '3x_close']

# 选择输出列
output_columns = ['date', 'open', 'high', 'low', 'close', 'volume', '涨跌幅(%)', 
                 'investment_total', 'portfolio_value',
                 '3x_return_pct', '3x_close', '3x_portfolio_value']

df_output = df[output_columns].copy()
df_output = df_output.rename(columns={
    'investment_total': 'investment_total',
    'portfolio_value': 'portfolio_value',
    '3x_return_pct': '3x_return_pct',
    '3x_close': '3x_close',
    '3x_portfolio_value': '3x_portfolio_value'
})

# 保存到新文件
df_output.to_csv('QQQ_daily_with_3x_leverage.csv', index=False)

print("处理完成！已生成 QQQ_daily_with_3x_leverage.csv 文件")
print(f"\n投资统计信息:")
print(f"数据时间范围: {df['date'].min().strftime('%Y-%m-%d')} 至 {df['date'].max().strftime('%Y-%m-%d')}")

# 原始QQQ投资统计
original_investment = df['investment_total'].max()
original_portfolio_value = df['portfolio_value'].iloc[-1]
original_return = original_portfolio_value - original_investment
original_return_pct = (original_return / original_investment) * 100

print(f"\n原始QQQ定投:")
print(f"累计投资总额: ${original_investment:,.2f}")
print(f"最终投资组合价值: ${original_portfolio_value:,.2f}")
print(f"总收益: ${original_return:,.2f}")
print(f"收益率: {original_return_pct:.2f}%")

# 3倍杠杆投资统计
leverage_3x_investment = df['3x_cumulative_investment'].max()
leverage_3x_portfolio_value = df['3x_portfolio_value'].iloc[-1]
leverage_3x_return = leverage_3x_portfolio_value - leverage_3x_investment
leverage_3x_return_pct = (leverage_3x_return / leverage_3x_investment) * 100

print(f"\n3倍杠杆QQQ定投:")
print(f"累计投资总额: ${leverage_3x_investment:,.2f}")
print(f"最终投资组合价值: ${leverage_3x_portfolio_value:,.2f}")
print(f"总收益: ${leverage_3x_return:,.2f}")
print(f"收益率: {leverage_3x_return_pct:.2f}%")

print(f"\n对比:")
print(f"3倍杠杆相比原始QQQ的收益倍数: {leverage_3x_return / original_return:.2f}x")

# 显示数据样本
print(f"\n数据样本（前10行）:")
sample_columns = ['date', 'close', '涨跌幅(%)', '3x_return_pct', '3x_close', 'portfolio_value', '3x_portfolio_value']
print(df[sample_columns].head(10).to_string(index=False))

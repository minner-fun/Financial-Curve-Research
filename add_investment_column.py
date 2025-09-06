import pandas as pd
from datetime import datetime

# 读取数据
df = pd.read_csv('QQQ_daily.csv')

# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 添加年月列用于分组
df['year_month'] = df['date'].dt.to_period('M')

# 初始化投资相关列
df['monthly_investment'] = 0.0  # 当月投资金额
df['shares_bought'] = 0.0       # 当月购买股数
df['cumulative_investment'] = 0.0  # 累计投资总额
df['cumulative_shares'] = 0.0      # 累计持有股数
df['portfolio_value'] = 0.0        # 投资组合价值

# 定投参数
monthly_investment = 1000.0  # 每月投资1000美元

# 处理每个月的定投
cumulative_investment = 0.0
cumulative_shares = 0.0

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
    
    # 在投资日进行定投
    investment_price = df.loc[investment_day, 'close']
    shares_to_buy = monthly_investment / investment_price
    
    # 更新累计数据
    cumulative_investment += monthly_investment
    cumulative_shares += shares_to_buy
    
    # 更新该月投资日的数据
    df.loc[investment_day, 'monthly_investment'] = monthly_investment
    df.loc[investment_day, 'shares_bought'] = shares_to_buy
    
    # 更新该月所有交易日的累计数据和投资组合价值
    for idx in month_data.index:
        if idx <= investment_day:
            # 投资日及之前的日期
            if idx == investment_day:
                df.loc[idx, 'cumulative_investment'] = cumulative_investment
                df.loc[idx, 'cumulative_shares'] = cumulative_shares
            else:
                # 投资日之前，使用上月的累计数据
                df.loc[idx, 'cumulative_investment'] = cumulative_investment - monthly_investment
                df.loc[idx, 'cumulative_shares'] = cumulative_shares - shares_to_buy
        else:
            # 投资日之后的日期，使用当月投资后的累计数据
            df.loc[idx, 'cumulative_investment'] = cumulative_investment
            df.loc[idx, 'cumulative_shares'] = cumulative_shares
        
        # 计算投资组合价值
        df.loc[idx, 'portfolio_value'] = df.loc[idx, 'cumulative_shares'] * df.loc[idx, 'close']

# 保存带有投资数据的新CSV文件
output_columns = ['date', 'open', 'high', 'low', 'close', 'volume', '涨跌幅(%)', 
                 'cumulative_investment', 'portfolio_value']
df_output = df[output_columns].copy()
df_output = df_output.rename(columns={'cumulative_investment': 'investment_total'})

# 保存到新文件
df_output.to_csv('QQQ_daily_with_investment.csv', index=False)

print("处理完成！已生成 QQQ_daily_with_investment.csv 文件")
print(f"\n投资统计信息:")
print(f"数据时间范围: {df['date'].min().strftime('%Y-%m-%d')} 至 {df['date'].max().strftime('%Y-%m-%d')}")
print(f"投资月数: {len(df[df['monthly_investment'] > 0])} 个月")
print(f"累计投资总额: ${df['cumulative_investment'].max():,.2f}")
print(f"最终投资组合价值: ${df['portfolio_value'].iloc[-1]:,.2f}")
print(f"总收益: ${df['portfolio_value'].iloc[-1] - df['cumulative_investment'].max():,.2f}")
print(f"收益率: {((df['portfolio_value'].iloc[-1] / df['cumulative_investment'].max()) - 1) * 100:.2f}%")

# 显示前几次投资的详细信息
investment_days = df[df['monthly_investment'] > 0].head(10)
print(f"\n前10次定投详情:")
print(investment_days[['date', 'close', 'monthly_investment', 'shares_bought', 'cumulative_investment', 'portfolio_value']].to_string(index=False))

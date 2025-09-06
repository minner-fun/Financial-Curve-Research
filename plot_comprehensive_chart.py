import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('QQQ_daily_with_3x_leverage.csv')

# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 创建图表，使用子图布局
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('QQQ vs 3倍杠杆QQQ 投资对比分析', fontsize=20, fontweight='bold')

# 子图1: 收盘价对比
ax1.plot(df['date'], df['close'], linewidth=2, color='blue', alpha=0.8, label='QQQ收盘价')
ax1.plot(df['date'], df['3x_close'], linewidth=2, color='red', alpha=0.8, label='3倍杠杆QQQ收盘价')
ax1.set_title('收盘价对比', fontsize=14, fontweight='bold')
ax1.set_ylabel('价格 (USD)', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')  # 使用对数坐标，因为3倍杠杆增长很快

# 子图2: 投资组合价值对比
ax2.plot(df['date'], df['portfolio_value'], linewidth=2, color='green', alpha=0.8, label='QQQ投资组合价值')
ax2.plot(df['date'], df['3x_portfolio_value'], linewidth=2, color='orange', alpha=0.8, label='3倍杠杆投资组合价值')
ax2.plot(df['date'], df['investment_total'], linewidth=2, color='gray', alpha=0.8, label='累计投资总额', linestyle='--')
ax2.set_title('投资组合价值对比', fontsize=14, fontweight='bold')
ax2.set_ylabel('价值 (USD)', fontsize=12)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')  # 使用对数坐标

# 子图3: 收益率对比（相对于投资总额的倍数）
df['qqq_return_ratio'] = df['portfolio_value'] / df['investment_total']
df['3x_return_ratio'] = df['3x_portfolio_value'] / df['investment_total']

ax3.plot(df['date'], df['qqq_return_ratio'], linewidth=2, color='blue', alpha=0.8, label='QQQ收益倍数')
ax3.plot(df['date'], df['3x_return_ratio'], linewidth=2, color='red', alpha=0.8, label='3倍杠杆收益倍数')
ax3.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='盈亏平衡线')
ax3.set_title('收益倍数对比（投资组合价值/投资总额）', fontsize=14, fontweight='bold')
ax3.set_ylabel('收益倍数', fontsize=12)
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_yscale('log')

# 子图4: 绝对收益对比
df['qqq_absolute_return'] = df['portfolio_value'] - df['investment_total']
df['3x_absolute_return'] = df['3x_portfolio_value'] - df['investment_total']

ax4.plot(df['date'], df['qqq_absolute_return'], linewidth=2, color='green', alpha=0.8, label='QQQ绝对收益')
ax4.plot(df['date'], df['3x_absolute_return'], linewidth=2, color='purple', alpha=0.8, label='3倍杠杆绝对收益')
ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='盈亏平衡线')
ax4.set_title('绝对收益对比', fontsize=14, fontweight='bold')
ax4.set_ylabel('绝对收益 (USD)', fontsize=12)
ax4.set_xlabel('日期', fontsize=12)
ax4.legend()
ax4.grid(True, alpha=0.3)

# 设置所有子图的x轴日期格式
for ax in [ax1, ax2, ax3, ax4]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_minor_locator(mdates.YearLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig('QQQ_vs_3x_comprehensive_analysis.png', dpi=300, bbox_inches='tight')

# 显示图表
plt.show()

# 创建第二个图表：单独的综合对比图
plt.figure(figsize=(16, 10))

# 标准化处理，将所有数据转换为相对于初始值的倍数
initial_close = df['close'].iloc[0]
initial_3x_close = df['3x_close'].iloc[0]
initial_portfolio = df['portfolio_value'].iloc[0]
initial_3x_portfolio = df['3x_portfolio_value'].iloc[0]
initial_investment = df['investment_total'].iloc[0]

plt.plot(df['date'], df['close'] / initial_close, linewidth=2, color='blue', alpha=0.8, label='QQQ收盘价 (标准化)')
plt.plot(df['date'], df['3x_close'] / initial_3x_close, linewidth=2, color='red', alpha=0.8, label='3倍杠杆QQQ收盘价 (标准化)')
plt.plot(df['date'], df['portfolio_value'] / initial_portfolio, linewidth=2, color='green', alpha=0.8, label='QQQ投资组合价值 (标准化)')
plt.plot(df['date'], df['3x_portfolio_value'] / initial_3x_portfolio, linewidth=2, color='orange', alpha=0.8, label='3倍杠杆投资组合价值 (标准化)')
plt.plot(df['date'], df['investment_total'] / initial_investment, linewidth=3, color='gray', alpha=0.8, label='累计投资总额 (标准化)', linestyle='--')

plt.title('QQQ vs 3倍杠杆QQQ 标准化对比图', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('日期', fontsize=12)
plt.ylabel('相对初始值的倍数', fontsize=12)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.yscale('log')

# 设置x轴日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
plt.gca().xaxis.set_minor_locator(mdates.YearLocator())
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('QQQ_vs_3x_normalized_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 打印统计信息
print("=" * 60)
print("QQQ vs 3倍杠杆QQQ 投资分析报告")
print("=" * 60)

print(f"\n数据时间范围: {df['date'].min().strftime('%Y-%m-%d')} 至 {df['date'].max().strftime('%Y-%m-%d')}")
print(f"投资期间: {(df['date'].max() - df['date'].min()).days} 天")

print(f"\n【QQQ 定投表现】")
print(f"累计投资总额: ${df['investment_total'].max():,.2f}")
print(f"最终投资组合价值: ${df['portfolio_value'].iloc[-1]:,.2f}")
print(f"总收益: ${df['qqq_absolute_return'].iloc[-1]:,.2f}")
print(f"收益率: {((df['portfolio_value'].iloc[-1] / df['investment_total'].max()) - 1) * 100:.2f}%")
print(f"年化收益率: {(((df['portfolio_value'].iloc[-1] / df['investment_total'].max()) ** (365.25 / (df['date'].max() - df['date'].min()).days)) - 1) * 100:.2f}%")

print(f"\n【3倍杠杆QQQ 定投表现】")
print(f"累计投资总额: ${df['investment_total'].max():,.2f}")
print(f"最终投资组合价值: ${df['3x_portfolio_value'].iloc[-1]:,.2f}")
print(f"总收益: ${df['3x_absolute_return'].iloc[-1]:,.2f}")
print(f"收益率: {((df['3x_portfolio_value'].iloc[-1] / df['investment_total'].max()) - 1) * 100:.2f}%")
print(f"年化收益率: {(((df['3x_portfolio_value'].iloc[-1] / df['investment_total'].max()) ** (365.25 / (df['date'].max() - df['date'].min()).days)) - 1) * 100:.2f}%")

print(f"\n【对比分析】")
print(f"3倍杠杆收益是QQQ收益的: {df['3x_absolute_return'].iloc[-1] / df['qqq_absolute_return'].iloc[-1]:.2f} 倍")
print(f"3倍杠杆最终价值是QQQ最终价值的: {df['3x_portfolio_value'].iloc[-1] / df['portfolio_value'].iloc[-1]:.2f} 倍")

# 计算最大回撤
def calculate_max_drawdown(values):
    peak = values.expanding().max()
    drawdown = (values - peak) / peak
    return drawdown.min() * 100

qqq_max_drawdown = calculate_max_drawdown(df['portfolio_value'])
x3_max_drawdown = calculate_max_drawdown(df['3x_portfolio_value'])

print(f"\n【风险分析】")
print(f"QQQ最大回撤: {qqq_max_drawdown:.2f}%")
print(f"3倍杠杆最大回撤: {x3_max_drawdown:.2f}%")

print("\n图表已保存为:")
print("- QQQ_vs_3x_comprehensive_analysis.png (四宫格分析图)")
print("- QQQ_vs_3x_normalized_comparison.png (标准化对比图)")

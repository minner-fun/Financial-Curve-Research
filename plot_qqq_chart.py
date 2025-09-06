import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('QQQ_daily.csv')

# 将日期列转换为datetime格式
df['date'] = pd.to_datetime(df['date'])

# 创建图表
plt.figure(figsize=(15, 8))
plt.plot(df['date'], df['close'], linewidth=1, color='blue', alpha=0.8)

# 设置图表标题和标签
plt.title('QQQ纳指基金历史收盘价走势图', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('日期', fontsize=12)
plt.ylabel('收盘价 (USD)', fontsize=12)

# 设置x轴日期格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=6))

# 旋转x轴标签以避免重叠
plt.xticks(rotation=45)

# 添加网格线
plt.grid(True, alpha=0.3)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()

# 打印一些基本统计信息
print(f"数据时间范围: {df['date'].min().strftime('%Y-%m-%d')} 至 {df['date'].max().strftime('%Y-%m-%d')}")
print(f"总交易日数: {len(df)} 天")
print(f"收盘价范围: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
print(f"平均收盘价: ${df['close'].mean():.2f}")

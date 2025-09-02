import akshare as ak
import pandas as pd

# 1) 东方财富 ETF 历史行情（支持 period="daily"/"weekly"/"monthly"）
codes = ["159941", "513100"]  # 深市不带后缀；上证代码同样直接填
frames = {}

for code in codes:
    df = ak.fund_etf_hist_em(symbol=code, period="monthly", adjust="qfq")  # 前复权月K
    df.rename(columns={
        "日期":"date","开盘":"open","收盘":"close","最高":"high","最低":"low",
        "成交量":"volume","成交额":"amount"
    }, inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    frames[code] = df

# 2) 示例查看与保存
frames["159941"].head()
frames["159941"].to_csv("159941_monthly.csv", encoding="utf-8-sig")

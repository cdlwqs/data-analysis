"""第10章 效应分解法-AirPassengers时间序列预测 -> Python
原素材: AirPassengers.csv (1949-1960月度航空旅客, 含ln_AIR)
内涵: 效应分解法把序列分解为 趋势+季节+残差(加法模型,对ln(AIR)分解),
      趋势线性外推叠加季节分量完成预测。无statsmodels, 手动实现移动平均分解。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第10章 使用效应分解方法做预报" / "AirPassengers.csv"
df = pd.read_csv(F)
df["DATE"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
df = df.sort_values("DATE").reset_index(drop=True)
y = df["ln_AIR"].values
n = len(y)
month = df["DATE"].dt.month.values

trend = pd.Series(y).rolling(12, center=True, min_periods=12).mean().values
detrend = y - trend
seasonal = np.zeros(n)
smean = {}
for m in range(1, 13):
    vals = detrend[month == m]
    vals = vals[~np.isnan(vals)]
    smean[m] = vals.mean() if vals.size else 0
seasonal = np.array([smean[m] for m in month])
seasonal = seasonal - seasonal.mean()
resid = y - trend - seasonal

valid = ~np.isnan(trend)
b1, b0 = np.polyfit(np.arange(n)[valid], trend[valid], 1)
fh = 12
fx = np.arange(n, n + fh)
ftrend = b1 * fx + b0
fmonth = [(month[-1] + i - 1) % 12 + 1 for i in range(1, fh + 1)]
fseasonal = np.array([smean[m] for m in fmonth]) - seasonal.mean()
flog = ftrend + fseasonal
forecast = np.exp(flog)
last_date = df["DATE"].iloc[-1]
fdates = pd.date_range(last_date + pd.offsets.MonthBegin(1), periods=fh, freq="MS")
print(f"样本{n}个月  趋势斜率(对数){b1:.4f}/月")
print("\n== 未来12个月预测 ==")
for d, v in zip(fdates, forecast):
    print(f"{d.strftime('%Y-%m')}  {v:.0f}")

fig, axes = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
axes[0].plot(df["DATE"], df["AIR"], color="#4C78A8", label="实际")
axes[0].plot(fdates, forecast, color="#E45756", ls="--", marker="o", ms=3, label="预测")
axes[0].set_title("AirPassengers 实际与预测", fontsize=10); axes[0].legend(fontsize=7)
axes[1].plot(df["DATE"], np.exp(trend), color="#F58518"); axes[1].set_title("趋势分量", fontsize=10)
axes[2].plot(df["DATE"], np.exp(seasonal), color="#54A24B"); axes[2].set_title("季节分量", fontsize=10)
axes[3].plot(df["DATE"], np.exp(resid), color="#9D9D9D"); axes[3].set_title("残差分量", fontsize=10)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第10章_AirPassengers效应分解.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

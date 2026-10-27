"""第10章 效应分解法-信用卡消费额(含节日) -> Python
原素材: 信用卡消费额_含节日.xlsx (pos: 2013-03起31天日度消费额, 含节日效应)
内涵: 效应分解法分解为 趋势+星期季节+残差, 残差中显著正偏差即节日效应,
      分离节日后看真实趋势与周内规律, 辅助预测与节日备付。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第10章 使用效应分解方法做预报" / "信用卡消费额_含节日.xlsx"
df = pd.read_excel(F, sheet_name="pos")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
y = df["amount"].values.astype(float)
n = len(y)
dow = df["date"].dt.dayofweek.values

trend = pd.Series(y).rolling(7, center=True, min_periods=7).mean().values
detrend = y - trend
smean = {}
for d in range(7):
    vals = detrend[dow == d]
    vals = vals[~np.isnan(vals)]
    smean[d] = vals.mean() if vals.size else 0
seasonal = np.array([smean[d] for d in dow])
seasonal = seasonal - seasonal.mean()
resid = y - trend - seasonal
thr = 1.5 * np.nanstd(resid)
festival = resid > thr
print(f"样本{n}天  残差阈值(节日){thr:.0f}")
print("== 各星期季节分量 ==")
for d in range(7):
    print(f"  星期{d}  {smean[d]-seasonal.mean():.0f}")
print("\n== 识别节日效应日 ==")
print(df.loc[festival, ["date", "amount"]].to_string(index=False))

fig, axes = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
axes[0].plot(df["date"], y, color="#4C78A8", label="实际")
axes[0].plot(df["date"], trend + seasonal, color="#E45756", ls="--", label="趋势+季节")
axes[0].set_title("信用卡日消费额 实际 vs 拟合", fontsize=10); axes[0].legend(fontsize=7)
axes[1].plot(df["date"], trend, color="#F58518"); axes[1].set_title("趋势分量", fontsize=10)
axes[2].plot(df["date"], seasonal, color="#54A24B"); axes[2].set_title("星期季节分量", fontsize=10)
axes[3].plot(df["date"], resid, color="#9D9D9D")
axes[3].scatter(df["date"][festival], resid[festival], color="#E45756", s=30, label="节日效应")
axes[3].axhline(thr, color="#E45756", ls="--", lw=0.8)
axes[3].set_title("残差(红色=识别的节日效应)", fontsize=10); axes[3].legend(fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第10章_信用卡节日效应分解.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

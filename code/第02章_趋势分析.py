"""第2章 趋势分析 -> Python
原素材: 2、引申方法/data-有答案/1趋势分析-参考.xlsx (year vs 订单量, 约45年)
内涵: 趋势分析用折线图展示指标随时间的变化, 并叠加线性趋势线与移动平均, 识别长期走向与波动。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "1趋势分析-参考.xlsx"
raw = pd.read_excel(F, sheet_name="趋势图", header=None)
df = raw.iloc[:, [1, 2]].copy()
df.columns = ["year", "订单量"]
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
df = df.dropna()
df = df.sort_values("year").reset_index(drop=True)
df["MA5"] = df["订单量"].rolling(5, center=True).mean()

b1, b0 = np.polyfit(df["year"], df["订单量"], 1)
print("== 趋势分析 ==")
print(df.to_string(index=False))
print(f"\n线性趋势: 订单量 = {b1:.2f} * year + {b0:.1f}")

fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(df["year"], df["订单量"], marker="o", ms=3, lw=1, color="#4C78A8", label="订单量")
ax.plot(df["year"], df["MA5"], color="#F58518", lw=1.2, label="5期移动平均")
ax.plot(df["year"], b1 * df["year"] + b0, color="#E45756", ls="--", lw=1, label="线性趋势线")
ax.set_xlabel("年份"); ax.set_ylabel("订单量")
ax.set_title("订单量趋势分析", fontsize=10)
ax.legend(fontsize=8)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_趋势分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

"""第2章 相关分析 -> Python
原素材: 3-1相关分析-参考.xlsx (原始数据58行, x/y两变量)
内涵: 相关分析用散点图和相关系数衡量两个数值变量的线性相关程度与方向, 并拟合回归线。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "3-1相关分析-参考.xlsx"
df = pd.read_excel(F, sheet_name="原始数据")
r = df["x"].corr(df["y"])
print(f"样本数={len(df)}  相关系数r={r:.4f}")
print(df.describe().to_string())

fig, ax = plt.subplots(figsize=(7, 4.8))
ax.scatter(df["x"], df["y"], s=18, color="#4C78A8", alpha=0.7)
import numpy as np
b1, b0 = np.polyfit(df["x"], df["y"], 1)
xs = np.linspace(df["x"].min(), df["x"].max(), 50)
ax.plot(xs, b1 * xs + b0, color="#E45756", lw=1.2, label=f"y={b1:.3f}x+{b0:.1f}")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(f"相关分析散点图  r={r:.4f}", fontsize=10)
ax.legend(fontsize=8)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_相关分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

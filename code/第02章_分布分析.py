"""第2章 分布分析 -> Python
原素材: 2、引申方法/data-有答案/3分布分析-参考.xlsx (门店客流量时序 + 用户年龄 + 客单价, 含均值/Q1/中位数/Q3)
内涵: 分布分析用直方图、箱线图展示数值变量的分布形态, 标注均值与分位数, 识别集中趋势、离散度与异常值。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "3分布分析-参考.xlsx"
raw = pd.read_excel(F, sheet_name="分布分析", header=None)

age = pd.to_numeric(raw.iloc[1:, 12], errors="coerce").dropna()
price = pd.to_numeric(raw.iloc[1:, 20], errors="coerce").dropna()
print(f"客单价: n={len(price)} 均值={price.mean():.2f} min={price.min():.1f} Q1={price.quantile(.25):.2f} 中位数={price.median():.2f} Q3={price.quantile(.75):.2f} max={price.max():.1f}")
print(f"年龄:   n={len(age)} 均值={age.mean():.2f} 中位数={age.median():.1f}")

fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
axes[0].hist(price, bins=20, color="#4C78A8", edgecolor="white")
axes[0].axvline(price.mean(), color="#E45756", ls="--", lw=1, label=f"均值{price.mean():.1f}")
axes[0].axvline(price.median(), color="#54A24B", ls="--", lw=1, label=f"中位数{price.median():.1f}")
axes[0].set_title("客单价分布", fontsize=10); axes[0].legend(fontsize=7)
axes[0].set_xlabel("客单价"); axes[0].set_ylabel("频数")

axes[1].boxplot([price, age], labels=["客单价", "年龄"], widths=0.5)
axes[1].set_title("箱线图(分布与异常值)", fontsize=10)

axes[2].hist(age, bins=15, color="#F58518", edgecolor="white")
axes[2].axvline(age.mean(), color="#E45756", ls="--", lw=1, label=f"均值{age.mean():.1f}")
axes[2].set_title("年龄分布", fontsize=10); axes[2].legend(fontsize=7)
axes[2].set_xlabel("年龄"); axes[2].set_ylabel("频数")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_分布分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

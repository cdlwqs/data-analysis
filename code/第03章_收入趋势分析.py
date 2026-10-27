"""第3章 案例1 收入趋势分析 -> Python
原素材: 案例1：收入趋势分析原始数据.xlsx (1187行: 订单年份/订单月份/销售省份/销售额)
内涵: 收入趋势分析按年/月/省份拆解销售额, 看年度趋势、月度季节性、省份贡献与同比, 支撑收入预测。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架" / "案例1：收入趋势分析" / "案例1：收入趋势分析原始数据.xlsx"
df = pd.read_excel(F)
yearly = df.groupby("订单年份")["销售额"].sum()
ym = df.groupby(["订单年份", "订单月份"])["销售额"].sum().unstack(0)
prov = df.groupby("销售省份")["销售额"].sum().sort_values(ascending=False).head(15)
yoy = yearly.pct_change()
print("== 年度销售额与同比 ==")
print(pd.DataFrame({"销售额": yearly, "同比": yoy}).to_string())

fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
axes[0, 0].bar([str(y) for y in yearly.index], yearly.values, width=0.5, color="#4C78A8")
axes[0, 0].set_title("年度销售额趋势", fontsize=10)
for i, v in enumerate(yearly.values):
    axes[0, 0].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=7)
for y in ym.columns:
    axes[0, 1].plot(ym.index, ym[y], marker="o", ms=3, lw=1, label=str(y))
axes[0, 1].set_title("各年月度销售额", fontsize=10); axes[0, 1].set_xlabel("月份"); axes[0, 1].legend(fontsize=7)
axes[1, 0].barh(range(len(prov)), prov.values, height=0.6, color="#F58518")
axes[1, 0].set_yticks(range(len(prov))); axes[1, 0].set_yticklabels(prov.index, fontsize=7)
axes[1, 0].invert_yaxis(); axes[1, 0].set_title("TOP15省份销售额", fontsize=10)
valid = yoy.dropna()
axes[1, 1].bar([str(y) for y in valid.index], valid.values, width=0.5, color=["#54A24B" if v > 0 else "#E45756" for v in valid.values])
axes[1, 1].set_title("年度同比增长率", fontsize=10); axes[1, 1].axhline(0, color="gray", lw=0.8)
for i, v in enumerate(valid.values):
    axes[1, 1].text(i, v, f"{v:.0%}", ha='center', va='bottom' if v > 0 else 'top', fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第03章_收入趋势分析.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

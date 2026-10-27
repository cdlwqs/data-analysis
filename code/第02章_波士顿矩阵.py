"""第2章 波士顿矩阵 -> Python
原素材: 1-1波士顿矩阵-参考.xlsx (销售表9284行, 14品牌, 2021-07~08)
内涵: 波士顿矩阵以"相对市场份额"(横轴)和"市场增长率"(纵轴)把品牌分入四象限:
      明星(高份额高增长)/现金牛(高份额低增长)/问题(低份额高增长)/瘦狗(低份额低增长),
      指导品牌资源配置。用7月vs8月销售额算增长率, 份额=品牌销售额/总销售额。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "1-1波士顿矩阵-参考.xlsx"
df = pd.read_excel(F, sheet_name="销售表")
df["销售日期"] = pd.to_datetime(df["销售日期"])
df["月"] = df["销售日期"].dt.month

g7 = df[df["月"] == 7].groupby("品牌")["订单金额"].sum()
g8 = df[df["月"] == 8].groupby("品牌")["订单金额"].sum()
total = g7.add(g8, fill_value=0)
share = total / total.sum()
rel_share = share / share.max()
growth = (g8 / g7 - 1).replace([np.inf, -np.inf], np.nan).fillna(0)

res = pd.DataFrame({"销售额": total, "相对份额": rel_share, "增长率": growth})
def quad(r):
    return ("明星" if r["相对份额"] >= 0.5 and r["增长率"] >= 0 else
            "现金牛" if r["相对份额"] >= 0.5 and r["增长率"] < 0 else
            "问题" if r["相对份额"] < 0.5 and r["增长率"] >= 0 else "瘦狗")
res["象限"] = res.apply(quad, axis=1)
print("== 波士顿矩阵品牌分类 ==")
print(res.sort_values("销售额", ascending=False).to_string())
print("\n各象限品牌数:\n", res["象限"].value_counts().to_string())

color = {"明星": "#E45756", "现金牛": "#4C78A8", "问题": "#F58518", "瘦狗": "#9D9D9D"}
fig, ax = plt.subplots(figsize=(8, 5.5))
for q, c in color.items():
    sub = res[res["象限"] == q]
    ax.scatter(sub["相对份额"], sub["增长率"], s=sub["销售额"] / 300, color=c, alpha=0.7, label=q, edgecolor="white")
for b, r in res.iterrows():
    ax.annotate(b, (r["相对份额"], r["增长率"]), fontsize=8, ha="center", va="center")
ax.axhline(0, color="gray", lw=0.8, ls="--")
ax.axvline(0.5, color="gray", lw=0.8, ls="--")
ax.set_xlabel("相对市场份额"); ax.set_ylabel("市场增长率")
ax.set_title("波士顿矩阵-品牌四象限(气泡=销售额)", fontsize=10)
ax.legend(fontsize=8, loc="upper left")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_波士顿矩阵.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

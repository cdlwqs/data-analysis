"""第2章 桑基图(Sankey) -> Python
原素材: 2、引申方法/data-无答案/6桑吉图.xlsx (来源->目标->流量, 15条流向)
内涵: 桑基图用流量带展示节点间的流向与规模, 宽度代表流量大小, 直观呈现转化/流转结构。
      matplotlib无原生桑基, 这里手绘两列流向图(左来源/右目标, 带宽=流量)。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-无答案" / "6桑吉图.xlsx"
df = pd.read_excel(F, sheet_name="Sheet1")
df = df[["来源", "目标", "流量"]].dropna()
df["流量"] = df["流量"].astype(float)
print("== 桑基流向 ==")
print(df.to_string(index=False))

srcs = df.groupby("来源")["流量"].sum().sort_values(ascending=False)
tgts = df.groupby("目标")["流量"].sum().sort_values(ascending=False)
H = 10.0
gap = 0.4

def layout(series):
    total = series.sum() + gap * (len(series) - 1)
    y0 = {}
    y = 0
    for n, v in series.items():
        h = v / series.sum() * H
        y0[n] = (y, y + h)
        y += h + gap
    return y0

ys = layout(srcs)
yt = layout(tgts)
xL, xR = 0.0, 1.0
w = 0.06

fig, ax = plt.subplots(figsize=(9, 6))
for n, (a, b) in ys.items():
    ax.add_patch(Polygon([[xL-w, a], [xL, a], [xL, b], [xL-w, b]], closed=True, color="#4C78A8"))
    ax.text(xL - w - 0.02, (a + b) / 2, f"{n} {int(srcs[n])}", ha="right", va="center", fontsize=8)
for n, (a, b) in yt.items():
    ax.add_patch(Polygon([[xR, a], [xR+w, a], [xR+w, b], [xR, b]], closed=True, color="#F58518"))
    ax.text(xR + w + 0.02, (a + b) / 2, f"{n} {int(tgts[n])}", ha="left", va="center", fontsize=8)

cur = {n: 0.0 for n in ys}
curt = {n: 0.0 for n in yt}
for _, row in df.iterrows():
    s, t, fl = row["来源"], row["目标"], row["流量"]
    hs = fl / srcs.sum() * H
    ht = fl / tgts.sum() * H
    sa, sb = ys[s][0] + cur[s], ys[s][0] + cur[s] + hs
    ta, tb = yt[t][0] + curt[t], yt[t][0] + curt[t] + ht
    cur[s] += hs
    curt[t] += ht
    pts = [[xL, sa], [xR, ta], [xR, tb], [xL, sb]]
    ax.add_patch(Polygon(pts, closed=True, color="#9D9D9D", alpha=0.45, edgecolor="none"))

ax.set_xlim(-0.35, 1.35); ax.set_ylim(-0.5, H + 1)
ax.axis("off")
ax.set_title("桑基图-页面流量流向", fontsize=10)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_桑基图.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

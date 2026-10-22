"""第2章 RFM模型 -> Python
原素材: 1-2RFM模型-参考.xlsx (原始数据65989行, 7178用户, 2019-01~07, 分析时点2019-08-03)
内涵: RFM按最近消费间隔R、消费频次F、消费金额M, 以均值为界分高低, 组合出8类客户
      (重要价值/重要发展/重要保持/重要挽留/一般价值/一般发展/一般保持/一般挽留),
      指导差异化运营。并做消费金额帕累托(累计占比)。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "1-2RFM模型-参考.xlsx"
df = pd.read_excel(F, sheet_name="原始数据")
df["销售日期"] = pd.to_datetime(df["销售日期"])
SP = pd.Timestamp("2019-08-03")

g = df.groupby("用户编号").agg(
    R=("销售日期", lambda x: (SP - x.max()).days),
    F=("流水号", "nunique"),
    M=("销售金额", "sum"),
)
rM, fM, mM = g["R"].mean(), g["F"].mean(), g["M"].mean()
g["R高"] = g["R"] < rM
g["F高"] = g["F"] > fM
g["M高"] = g["M"] > mM
name = {
    (1,1,1):"重要价值客户",(1,1,0):"重要发展客户",(1,0,1):"重要保持客户",(1,0,0):"重要挽留客户",
    (0,1,1):"一般价值客户",(0,1,0):"一般发展客户",(0,0,1):"一般保持客户",(0,0,0):"一般挽留客户",
}
g["客户类型"] = g.apply(lambda r: name[(r["R高"],r["F高"],r["M高"])], axis=1)
print(f"R均值={rM:.1f} F均值={fM:.1f} M均值={mM:.1f}")
print("\n== 8类客户数与金额 ==")
agg = g.groupby("客户类型").agg(人数=("M","count"), 金额=("M","sum")).sort_values("金额", ascending=False)
print(agg.to_string())

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
axes[0].bar(range(len(agg)), agg["人数"], width=0.6, color="#4C78A8")
axes[0].set_xticks(range(len(agg))); axes[0].set_xticklabels(agg.index, rotation=40, ha="right", fontsize=7)
axes[0].set_title("RFM 8类客户人数", fontsize=10)
for i, v in enumerate(agg["人数"]):
    axes[0].text(i, v, str(v), ha="center", va="bottom", fontsize=7)

s = g.sort_values("M", ascending=False).reset_index(drop=True)
s["累计占比"] = s["M"].cumsum() / s["M"].sum()
ax2 = axes[1]
ax2.bar(range(len(s)), s["M"], width=1.0, color="#4C78A8")
ax2.set_title("消费金额帕累托图", fontsize=10)
ax2.set_ylabel("消费金额")
axr = ax2.twinx()
axr.plot(range(len(s)), s["累计占比"], color="#E45756", lw=1)
axr.axhline(0.8, color="gray", ls="--", lw=0.8)
axr.set_ylabel("累计占比")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_RFM模型.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

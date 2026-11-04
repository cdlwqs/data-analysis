"""第2章 用户忠诚度模型 -> Python
原素材: 1-3用户忠诚度模型-参考.xlsx (销售流水表80111行, 分析时点2021-01-01, 最近13周=2020-10-02)
内涵: 忠诚度模型按消费次数、消费额的分位数(0.25/0.75)把会员分忠诚度等级,
      结合"是否最近13周内消费"识别流失风险。指标=度量+汇总规则(消费次数distinctcount订单, 消费额sum)。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "1-3用户忠诚度模型-参考.xlsx"
df = pd.read_excel(F, sheet_name="销售流水表")
df["消费日期"] = pd.to_datetime(df["消费日期"])

g = df.groupby("会员编号").agg(
    消费次数=("订单编号", "nunique"),
    消费额=("消费金额", "sum"),
    最近消费=("消费日期", "max"),
    近13周=("是否最近13周内消费", lambda x: x.dropna().iloc[0] if x.dropna().size else "否"),
)
qt = g["消费次数"].quantile([0.25, 0.75])
qa = g["消费额"].quantile([0.25, 0.75])
def lvl(v, q):
    return "高" if v >= q[0.75] else ("低" if v <= q[0.25] else "中")
g["次数等级"] = g["消费次数"].apply(lambda x: lvl(x, qt))
g["金额等级"] = g["消费额"].apply(lambda x: lvl(x, qa))
def loyal(r):
    if r["次数等级"] == "高" and r["金额等级"] == "高": return "高忠诚"
    if r["次数等级"] == "低" and r["金额等级"] == "低": return "低忠诚"
    return "中忠诚"
g["忠诚度"] = g.apply(loyal, axis=1)
g["流失风险"] = g["近13周"].apply(lambda x: "是" if str(x).strip() == "否" else "否")

print(f"消费次数分位 q25={qt[0.25]:.0f} q75={qt[0.75]:.0f}  消费额分位 q25={qa[0.25]:.0f} q75={qa[0.75]:.0f}")
print("\n== 忠诚度等级分布 ==")
print(g["忠诚度"].value_counts().to_string())
print("\n== 流失风险分布 ==")
print(g["流失风险"].value_counts().to_string())
print("\n== 忠诚度×流失 交叉 ==")
print(pd.crosstab(g["忠诚度"], g["流失风险"]).to_string())

fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
a = g["忠诚度"].value_counts().reindex(["高忠诚", "中忠诚", "低忠诚"])
axes[0].bar(a.index, a.values, width=0.5, color=["#54A24B", "#F58518", "#9D9D9D"])
axes[0].set_title("用户忠诚度等级分布", fontsize=10)
for i, v in enumerate(a.values):
    axes[0].text(i, v, str(v), ha="center", va="bottom", fontsize=8)
b = g["流失风险"].value_counts()
axes[1].bar(b.index, b.values, width=0.4, color=["#4C78A8", "#E45756"])
axes[1].set_title("流失风险分布(最近13周未消费)", fontsize=10)
for i, v in enumerate(b.values):
    axes[1].text(i, v, str(v), ha="center", va="bottom", fontsize=8)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_用户忠诚度.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

"""第2章 关系分析 -> Python
原素材: 2、引申方法/data-有答案/5关系分析-参考.xlsx (分类变量×下单 + 营销活动数值 + 产出收益vs投入成本)
内涵: 关系分析探究变量间关联——分类变量间用堆叠条形/列联, 连续变量间用散点+相关系数,
      分类×连续用分组对比。
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "5关系分析-参考.xlsx"
raw = pd.read_excel(F, sheet_name="关系图", header=None)

camp = []
for i in range(raw.shape[0]):
    v = str(raw.iloc[i, 1]).strip()
    if v.startswith("营销活动"):
        camp.append((v, float(raw.iloc[i, 2]), float(raw.iloc[i, 3])))
camp = pd.DataFrame(camp, columns=["营销活动", "下单用户", "未下单用户"])
y = pd.to_numeric(raw.iloc[:, 24], errors="coerce")
x = pd.to_numeric(raw.iloc[:, 25], errors="coerce")
cont = pd.concat([x.rename("投入成本"), y.rename("产出收益")], axis=1).dropna()

print("== 营销活动×下单(分类变量关系) ==")
print(camp.to_string(index=False))
r = cont["投入成本"].corr(cont["产出收益"])
print(f"\n产出收益 vs 投入成本 相关系数={r:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
axes[0].bar(camp["营销活动"], camp["下单用户"], width=0.5, label="下单用户", color="#4C78A8")
axes[0].bar(camp["营销活动"], camp["未下单用户"], bottom=camp["下单用户"], width=0.5, label="未下单用户", color="#F58518")
axes[0].set_title("营销活动与下单关系(堆叠)", fontsize=10)
axes[0].legend(fontsize=8)
for i, row in camp.iterrows():
    axes[0].text(i, row["下单用户"] / 2, int(row["下单用户"]), ha='center', va='center', fontsize=7, color="white")

axes[1].scatter(cont["投入成本"], cont["产出收益"], s=16, color="#4C78A8", alpha=0.7)
b1, b0 = np.polyfit(cont["投入成本"], cont["产出收益"], 1)
xs = np.linspace(cont["投入成本"].min(), cont["投入成本"].max(), 50)
axes[1].plot(xs, b1 * xs + b0, color="#E45756", lw=1, label=f"y={b1:.2f}x+{b0:.0f}")
axes[1].set_title(f"产出收益 vs 投入成本  r={r:.3f}", fontsize=10)
axes[1].set_xlabel("投入成本"); axes[1].set_ylabel("产出收益")
axes[1].legend(fontsize=8)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_关系分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

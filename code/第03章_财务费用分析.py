"""第3章 案例2 财务费用分析 -> Python
原素材: 案例2：财务费用分析-原始数据.xlsx (总费用/三大期间费用/管理费用明细)
内涵: 财务费用分析拆解总费用——三大期间费用(管理/销售/财务)构成, 管理费用明细构成, 月度对比。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架" / "案例2：财务费用分析" / "案例2：财务费用分析-原始数据.xlsx"
total = pd.read_excel(F, "总费用数据")
three = pd.read_excel(F, "财务三大期间费用数据").iloc[:, :4].dropna(subset=["金额"])
mgmt = pd.read_excel(F, "管理费用数据")

three_sum = three.groupby("期间费用项")["金额"].sum()
mgmt_sum = mgmt.groupby("管理费用项")["金额"].sum().sort_values(ascending=False)
print("== 总费用 ==")
print(total.to_string(index=False))
print("\n== 三大期间费用合计 ==")
print(three_sum.to_string())
print("\n== 管理费用明细合计 ==")
print(mgmt_sum.to_string())

fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
axes[0].bar([f"{int(r['年份'])}-{int(r['月份'])}" for _, r in total.iterrows()], total["金额"], width=0.4, color="#4C78A8")
axes[0].set_title("总费用月度对比", fontsize=10)
for i, v in enumerate(total["金额"]):
    axes[0].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=8)
axes[1].pie(three_sum.values, labels=three_sum.index, autopct="%1.1f%%", textprops={"fontsize": 8})
axes[1].set_title("三大期间费用构成", fontsize=10)
axes[2].bar(mgmt_sum.index, mgmt_sum.values, width=0.6, color="#F58518")
axes[2].set_title("管理费用明细构成", fontsize=10); axes[2].tick_params(axis='x', rotation=30, labelsize=7)
for i, v in enumerate(mgmt_sum.values):
    axes[2].text(i, v, f"{v/1e4:.0f}", ha='center', va='bottom', fontsize=6)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第03章_财务费用分析.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

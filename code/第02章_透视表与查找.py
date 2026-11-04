"""第2章 WPS电子表格-数据透视表与查找(VLOOKUP) -> Python
原素材: 2透视表&条件格式&引用&查找练习.xlsx + sale.csv
内涵: 透视表用 pandas.pivot_table 复现——按销售人员汇总、按品名×地区交叉;
       VLOOKUP近似匹配用 pd.cut 分桶映射(成绩→等级); sale.csv 按年×地区透视.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "WPS电子表格" / "4、WPS电子表格的公式与函数"
f = B / "2透视表&条件格式&引用&查找练习.xlsx"

# === 1 透视表: 源数据 ===
src = pd.read_excel(f, sheet_name="数据透视表")
print("== 源数据(前4行) ==")
print(src.head(4).to_string(index=False))

p1 = src.pivot_table(index="销售人员", values=["数量", "销售金额"], aggfunc="sum")
p1["金额占比"] = p1["销售金额"] / p1["销售金额"].sum()
print("\n== 透视表1: 按销售人员汇总 ==")
print(p1.round(4).to_string())

p2 = src.pivot_table(index="品名", columns="销售地区", values="销售金额", aggfunc="sum", fill_value=0, margins=True, margins_name="合计")
print("\n== 透视表2: 品名×地区 销售金额交叉 ==")
print(p2.to_string())

# === 2 VLOOKUP近似匹配: 成绩→等级 ===
lk = pd.read_excel(f, sheet_name="查找", header=None)
stu = lk.iloc[1:41, 0:2].copy(); stu.columns = ["学生姓名", "成绩"]; stu["成绩"] = stu["成绩"].astype(int)
bins = [-1, 59, 69, 79, 89, 100]
labels = ["不及格", "及格", "可以", "良好", "优秀"]
stu["成绩等级"] = pd.cut(stu["成绩"], bins=bins, labels=labels)
print("\n== VLOOKUP: 成绩→等级(前10行) ==")
print(stu.head(10).to_string(index=False))
grade_cnt = stu["成绩等级"].value_counts().reindex(labels)

# === 3 sale.csv 透视: 年×地区 ===
sale = pd.read_csv(B / "sale.csv", encoding="gbk")
ps = sale.pivot_table(index="year", columns="market", values="sale", aggfunc="sum")
print("\n== sale.csv 透视: 年×地区 销售额 ==")
print(ps.to_string())

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
axes[0, 0].barh(p1.index, p1["销售金额"], color="#4C78A8")
axes[0, 0].set_title("透视表1: 销售人员销售金额")
for i, v in enumerate(p1["销售金额"].values):
    axes[0, 0].text(v, i, f"{v:,}", va="center", fontsize=7)
p2n = p2.drop("合计", errors="ignore").drop("合计", axis=1, errors="ignore")
im = axes[0, 1].imshow(p2n.values, cmap="YlOrRd")
axes[0, 1].set_xticks(range(len(p2n.columns))); axes[0, 1].set_xticklabels(p2n.columns, fontsize=7)
axes[0, 1].set_yticks(range(len(p2n.index))); axes[0, 1].set_yticklabels(p2n.index, fontsize=7)
axes[0, 1].set_title("透视表2: 品名×地区 金额热力图")
for i in range(len(p2n.index)):
    for j in range(len(p2n.columns)):
        axes[0, 1].text(j, i, f"{p2n.values[i,j]/1e4:.0f}", ha="center", va="center", fontsize=6, color="black")
axes[1, 0].bar(grade_cnt.index, grade_cnt.values, color="#F58518")
axes[1, 0].set_title("VLOOKUP: 成绩等级分布")
for i, v in enumerate(grade_cnt.values):
    axes[1, 0].text(i, v, str(v), ha="center", va="bottom", fontsize=7)
ps.plot(kind="bar", ax=axes[1, 1], color=["#4C78A8", "#F58518", "#54A24B", "#E45756"], width=0.8)
axes[1, 1].set_title("sale: 年×地区 销售额"); axes[1, 1].legend(fontsize=7)
axes[1, 1].set_xticklabels(ps.index, rotation=0)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_透视表与查找.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

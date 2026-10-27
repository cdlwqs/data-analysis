"""第2章 PowerBI案例-人力资源看板 -> Python
原素材: 5、PowerBI基本操作/函数练习文件/人力案例/员工信息.xlsx (200行)
内涵: 人力资源看板展示员工结构——部门/性别/学历/在职离职/年龄/司龄分布, 支撑人事决策。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "5、PowerBI基本操作" / "函数练习文件" / "人力案例" / "员工信息.xlsx"
df = pd.read_excel(F)
df["出生日期"] = pd.to_datetime(df["出生日期"])
df["入职日期"] = pd.to_datetime(df["入职日期"])
now = pd.Timestamp("2024-01-01")
df["年龄"] = now.year - df["出生日期"].dt.year
df["司龄"] = (now - df["入职日期"]).dt.days / 365

dep = df["部门"].value_counts()
sex = df["性别"].value_counts()
edu = df["文化程度"].value_counts()
stat = df["员工状态"].value_counts()
print("部门分布:\n", dep.to_string())
print("\n员工状态:\n", stat.to_string())

fig, axes = plt.subplots(2, 3, figsize=(13, 7))
axes[0, 0].bar(dep.index, dep.values, width=0.6, color="#4C78A8"); axes[0, 0].set_title("部门人数", fontsize=10)
axes[0, 0].tick_params(axis='x', rotation=30, labelsize=7)
axes[0, 1].bar(sex.index, sex.values, width=0.4, color="#F58518"); axes[0, 1].set_title("性别分布", fontsize=10)
axes[0, 2].bar(edu.index, edu.values, width=0.5, color="#54A24B"); axes[0, 2].set_title("学历分布", fontsize=10)
axes[1, 0].bar(stat.index, stat.values, width=0.4, color="#E45756"); axes[1, 0].set_title("在职/离职", fontsize=10)
axes[1, 1].hist(df["年龄"].dropna(), bins=15, color="#4C78A8", edgecolor="white"); axes[1, 1].set_title("年龄分布", fontsize=10)
axes[1, 2].hist(df["司龄"].dropna(), bins=15, color="#F58518", edgecolor="white"); axes[1, 2].set_title("司龄分布(年)", fontsize=10)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_人力资源看板.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

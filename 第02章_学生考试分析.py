"""第2章 PowerBI案例-学生考试分析 -> Python
原素材: 5、PowerBI基本操作/函数练习文件/学生考试案例 (学生信息59+教师信息3+考试记录59)
内涵: 学生考试分析——合并学生/考试/班主任, 比较各科成绩分布、班级均分、总分排名、性别差异。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "5、PowerBI基本操作" / "函数练习文件" / "学生考试案例"
stu = pd.read_excel(D / "学生及老师信息.xlsx", sheet_name="学生信息")
tea = pd.read_excel(D / "学生及老师信息.xlsx", sheet_name="教师信息")
exam = pd.read_excel(D / "考试记录.xlsx")
stu["性别"] = stu["性别(1男生,2女生)"].map({1: "男", 2: "女"})
m = stu.merge(exam, on="学号").merge(tea, on="班级", how="left")
m["总分"] = m["语文"] + m["数学"] + m["英语"]
print("== 各班各科均分 ==")
print(m.groupby("班级")[["语文", "数学", "英语", "总分"]].mean().round(1).to_string())
print("\n== 总分前5 ==")
print(m.nlargest(5, "总分")[["姓名", "班级", "班主任姓名", "总分"]].to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))
axes[0, 0].boxplot([m["语文"], m["数学"], m["英语"]], labels=["语文", "数学", "英语"], widths=0.5)
axes[0, 0].set_title("各科成绩分布", fontsize=10)
cls = m.groupby("班级")[["语文", "数学", "英语"]].mean()
x = range(len(cls))
axes[0, 1].bar([i - 0.25 for i in x], cls["语文"], width=0.25, label="语文", color="#4C78A8")
axes[0, 1].bar(x, cls["数学"], width=0.25, label="数学", color="#F58518")
axes[0, 1].bar([i + 0.25 for i in x], cls["英语"], width=0.25, label="英语", color="#54A24B")
axes[0, 1].set_xticks(list(x)); axes[0, 1].set_xticklabels(cls.index)
axes[0, 1].set_title("各班各科均分", fontsize=10); axes[0, 1].legend(fontsize=7)
top10 = m.nlargest(10, "总分")
axes[1, 0].barh(range(len(top10)), top10["总分"], height=0.6, color="#4C78A8")
axes[1, 0].set_yticks(range(len(top10))); axes[1, 0].set_yticklabels(top10["姓名"], fontsize=7)
axes[1, 0].invert_yaxis(); axes[1, 0].set_title("总分TOP10", fontsize=10)
gen = m.groupby("性别")[["语文", "数学", "英语", "总分"]].mean()
axes[1, 1].bar(gen.columns, gen.loc["男"], width=0.3, label="男", color="#4C78A8")
axes[1, 1].bar(gen.columns, gen.loc["女"], width=0.3, bottom=0, label="女", color="#F58518", alpha=0.5)
axes[1, 1].set_title("性别成绩对比(男柱/女半透)", fontsize=10); axes[1, 1].legend(fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_学生考试分析.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

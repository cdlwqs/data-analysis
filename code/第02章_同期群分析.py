"""第2章 同期群(Cohort)分析 -> Python
原素材: 1-4同期群分析-参考.xlsx (用户登录明细13102行, 注册日期2020-07起)
内涵: 同期群分析按注册日期对用户分群(cohort), 跟踪各cohort在注册后第N日的登录用户数/留存率,
      形成留存矩阵, 衡量不同批次用户的留存衰减。第几日=登录日期-注册日期。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "1-4同期群分析-参考.xlsx"
df = pd.read_excel(F, sheet_name="用户登录明细")
df["注册日期"] = pd.to_datetime(df["注册日期"])
df["登录日期"] = pd.to_datetime(df["登录日期"])
df["cohort"] = df["注册日期"].dt.to_period("W").dt.start_time
df["第几日"] = (df["登录日期"] - df["注册日期"]).dt.days

cohort_size = df.groupby("cohort")["用户编号"].nunique()
mat = df.groupby(["cohort", "第几日"])["用户编号"].nunique().unstack(fill_value=0)
ret = mat.div(cohort_size, axis=0)
N = 14
ret = ret.loc[:, :N]

print("== 各cohort注册用户数 ==")
print(cohort_size.to_string())
print("\n== 留存率矩阵(前14日) ==")
print(ret.round(2).to_string())

fig, ax = plt.subplots(figsize=(9, 5))
data = ret.fillna(0).values
im = ax.imshow(data, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
ax.set_xticks(range(len(ret.columns))); ax.set_xticklabels(ret.columns, fontsize=8)
ax.set_yticks(range(len(ret.index))); ax.set_yticklabels([d.strftime("%m-%d") for d in ret.index], fontsize=7)
ax.set_xlabel("第几日"); ax.set_ylabel("cohort(注册周起始)")
ax.set_title("同期群留存率热力图", fontsize=10)
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        if data[i, j] > 0:
            ax.text(j, i, f"{data[i,j]:.2f}", ha="center", va="center", fontsize=6, color="black")
plt.colorbar(im, ax=ax, fraction=0.04)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_同期群分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

"""第2章 漏斗图 -> Python
原素材: 2-1漏斗图-参考.xlsx (销售漏斗8阶段: 潜在100->接触90->意向80->明确70->谈判60->成交50)
内涵: 漏斗分析展示用户在转化路径各阶段的人数、阶段转化率(本阶段/上一阶段)与总体转化率(本阶段/潜在),
      定位流失环节。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "1、分析的基础范式" / "data-有答案" / "2-1漏斗图-参考.xlsx"
raw = pd.read_excel(F, sheet_name="Sheet1", header=None, skiprows=3)
raw = raw.iloc[:, [0, 2]].copy()
raw.columns = ["阶段", "用户数"]
raw = raw.dropna(subset=["阶段"]).reset_index(drop=True)
raw["用户数"] = pd.to_numeric(raw["用户数"], errors="coerce")
raw = raw.dropna(subset=["用户数"]).reset_index(drop=True)
raw["总体转化率"] = raw["用户数"] / raw["用户数"].iloc[0]
raw["阶段转化率"] = raw["用户数"] / raw["用户数"].shift(1)
raw.loc[0, "阶段转化率"] = 1.0
print("== 销售漏斗 ==")
print(raw.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4.8))
y = range(len(raw))
w = raw["用户数"].values
ax.barh(y, w, height=0.7, color="#4C78A8")
ax.set_yticks(y); ax.set_yticklabels(raw["阶段"], fontsize=9)
ax.invert_yaxis()
for i, r in raw.iterrows():
    ax.text(r["用户数"], i, f' {r["用户数"]}人  总体{r["总体转化率"]:.0%}', va="center", fontsize=8)
ax.set_title("销售漏斗分析", fontsize=10)
ax.set_xlabel("用户数")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_漏斗图.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

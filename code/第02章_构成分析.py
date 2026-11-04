"""第2章 构成分析 -> Python
原素材: 2、引申方法/data-有答案/4构成分析-参考.xlsx (产品类型 vs 销售量)
内涵: 构成分析用饼图/占比条形展示各部分占整体的比重, 揭示结构构成。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "4构成分析-参考.xlsx"
raw = pd.read_excel(F, sheet_name="构成分析", header=None)
df = raw.iloc[:, [1, 2]].copy()
df.columns = ["产品类型", "销售量"]
df["产品类型"] = df["产品类型"].astype(str)
df["销售量"] = pd.to_numeric(df["销售量"], errors="coerce")
df = df.dropna(subset=["销售量"])
df = df[df["产品类型"].str.contains("产品", na=False)].reset_index(drop=True)
df["占比"] = df["销售量"] / df["销售量"].sum()
print("== 构成分析 ==")
print(df.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
axes[0].pie(df["销售量"], labels=df["产品类型"], autopct="%1.1f%%", textprops={"fontsize": 8})
axes[0].set_title("各产品销售量占比", fontsize=10)
axes[1].bar(df["产品类型"], df["占比"], width=0.6, color="#4C78A8")
axes[1].set_title("构成占比条形图", fontsize=10)
axes[1].tick_params(axis='x', rotation=20, labelsize=8)
for i, v in enumerate(df["占比"]):
    axes[1].text(i, v, f"{v:.1%}", ha='center', va='bottom', fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_构成分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

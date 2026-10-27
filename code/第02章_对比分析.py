"""第2章 对比分析 -> Python
原素材: 2、引申方法/data-有答案/2对比分析-参考.xlsx (产品类型 vs 订单量)
内涵: 对比分析用条形图比较不同类别的指标大小, 识别高低差异。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "2、由基础分析范式引申出的分析方法" / "data-有答案" / "2对比分析-参考.xlsx"
raw = pd.read_excel(F, sheet_name="对比分析", header=None, skiprows=1)
df = raw.iloc[:, [1, 2]].copy()
df.columns = ["产品类型", "订单量"]
df = df.dropna()
df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
df = df.dropna().sort_values("订单量", ascending=False).reset_index(drop=True)
print("== 对比分析 ==")
print(df.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.bar(df["产品类型"], df["订单量"], width=0.6, color="#4C78A8")
ax.set_title("各产品类型订单量对比", fontsize=10)
ax.tick_params(axis='x', rotation=20, labelsize=8)
for i, v in enumerate(df["订单量"]):
    ax.text(i, v, str(int(v)), ha='center', va='bottom', fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_对比分析.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

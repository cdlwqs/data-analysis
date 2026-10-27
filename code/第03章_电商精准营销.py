"""第3章 案例3 电商平台精准营销 -> Python
原素材: 案例3：电商平台的精准营销-原始数据.xlsx (3926行: 客户ID/性别/年龄/品类/数量/支付方式/订单月份/订单年份)
内涵: 精准营销通过客户画像(性别/年龄/年龄段)、品类偏好、支付方式, 识别高价值客群并定向营销。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架" / "案例3：电商平台的精准营销" / "案例3：电商平台的精准营销-原始数据.xlsx"
df = pd.read_excel(F)

def age_band(a):
    if a < 18: return "18岁以下"
    if a <= 25: return "18-25岁"
    if a <= 35: return "26-35岁"
    if a <= 50: return "36-50岁"
    return "50岁以上"
df["年龄段"] = df["年龄"].apply(age_band)
sex = df.groupby("性别")["数量"].sum()
band = df.groupby("年龄段")["数量"].sum().reindex(["18岁以下", "18-25岁", "26-35岁", "36-50岁", "50岁以上"])
cat = df.groupby("品类")["数量"].sum().sort_values(ascending=False)
pay = df.groupby("支付方式")["数量"].sum().sort_values(ascending=False)
cross = df.groupby(["年龄段", "品类"])["数量"].sum().unstack(fill_value=0)
print("== 性别销量 ==\n", sex.to_string())
print("\n== 年龄段销量 ==\n", band.to_string())
print("\n== 品类销量 ==\n", cat.to_string())

fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
axes[0, 0].bar(sex.index, sex.values, width=0.4, color=["#4C78A8", "#F58518"])
axes[0, 0].set_title("性别销量分布", fontsize=10)
for i, v in enumerate(sex.values):
    axes[0, 0].text(i, v, str(v), ha='center', va='bottom', fontsize=8)
axes[0, 1].bar(band.index, band.values, width=0.6, color="#54A24B")
axes[0, 1].set_title("年龄段销量分布", fontsize=10); axes[0, 1].tick_params(axis='x', rotation=20, labelsize=7)
for i, v in enumerate(band.values):
    axes[0, 1].text(i, v, str(v), ha='center', va='bottom', fontsize=7)
axes[1, 0].barh(range(len(cat)), cat.values, height=0.6, color="#4C78A8")
axes[1, 0].set_yticks(range(len(cat))); axes[1, 0].set_yticklabels(cat.index, fontsize=7)
axes[1, 0].invert_yaxis(); axes[1, 0].set_title("各品类销量", fontsize=10)
axes[1, 1].bar(pay.index, pay.values, width=0.5, color="#E45756")
axes[1, 1].set_title("支付方式销量", fontsize=10)
for i, v in enumerate(pay.values):
    axes[1, 1].text(i, v, str(v), ha='center', va='bottom', fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第03章_电商精准营销.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

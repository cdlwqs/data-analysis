"""第1章 维度模型演示 -> Python
原素材: 第1章 数据分析思维/维度模型演示/商场销售数据表.xlsx
内涵: 星型模型——1个事实表(产品销售数据表)+5个维度表(品牌/类别/商铺城市/产品信息/日期)。
      维度模型面向分析,事实表通过外键关联维度表,便于多维聚合。用pandas复现星型连接与多维分析。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第1章 数据分析思维" / "维度模型演示" / "商场销售数据表.xlsx"

brand = pd.read_excel(F, "品牌")
cat = pd.read_excel(F, "类别")
city = pd.read_excel(F, "商铺城市")
prod = pd.read_excel(F, "产品信息表")
fact = pd.read_excel(F, "产品销售数据表")
date = pd.read_excel(F, "日期表")

print("== 星型模型结构 ==")
print(f"事实表  产品销售数据表  shape={fact.shape}")
print(f"维度表  品牌{brand.shape} 类别{cat.shape} 商铺城市{city.shape} 产品信息表{prod.shape} 日期表{date.shape}")
print("\n事实表外键: 产品编号->产品信息表, 商铺城市->商铺城市, 订单日期->日期表, 品牌名称->品牌, 产品类别->类别")

fact["订单日期"] = pd.to_datetime(fact["订单日期"])
date["日期"] = pd.to_datetime(date["日期"])
star = fact.merge(date, left_on="订单日期", right_on="日期", how="left")

print("\n== 多维聚合分析 ==")
by_brand = fact.groupby("品牌名称")["销售额"].sum().sort_values(ascending=False)
by_cat = fact.groupby("产品类别")["销售额"].sum().sort_values(ascending=False)
by_city = fact.groupby("商铺城市")["销售额"].sum().sort_values(ascending=False)
by_year = star.groupby("年度")["销售额"].sum()
print("按品牌销售额:\n", by_brand.to_string())
print("\n按类别销售额:\n", by_cat.to_string())
print("\n按城市销售额:\n", by_city.to_string())

fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
def bar(ax, s, title, color="#4C78A8"):
    ax.bar(s.index.astype(str), s.values, width=0.6, color=color)
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    for i, v in enumerate(s.values):
        ax.text(i, v, f"{v/1e6:.1f}M", ha='center', va='bottom', fontsize=7)
bar(axes[0, 0], by_brand, "各品牌销售额")
bar(axes[0, 1], by_cat, "各产品类别销售额", "#F58518")
bar(axes[1, 0], by_city, "各城市销售额", "#54A24B")
axes[1, 1].plot(by_year.index.astype(str), by_year.values, marker="o", color="#E45756")
axes[1, 1].set_title("年度销售额趋势", fontsize=10)
axes[1, 1].tick_params(labelsize=8)
for i, v in enumerate(by_year.values):
    axes[1, 1].text(i, v, f"{v/1e6:.0f}M", ha='center', va='bottom', fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第01章_维度模型.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

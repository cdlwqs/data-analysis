"""第2章 PowerBI案例-快速搭建销售看板 -> Python
原素材: 5、PowerBI基本操作/零售订单表.xlsx (6644行: 订单号/订单时间/实际支付/城市/数量/商品名称/商品类别)
内涵: 销售看板多维度展示销售——按日期趋势、按城市、按商品类别、TOP商品, 快速掌握经营全貌。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "5、PowerBI基本操作" / "零售订单表.xlsx"
df = pd.read_excel(F)
df["订单时间"] = pd.to_datetime(df["订单时间"])
df["日期"] = df["订单时间"].dt.date
daily = df.groupby("日期")["实际支付"].sum()
city = df.groupby("城市")["实际支付"].sum().sort_values(ascending=False)
cat = df.groupby("商品类别")["实际支付"].sum().sort_values(ascending=False)
top = df.groupby("商品名称")["实际支付"].sum().sort_values(ascending=False).head(10)
print(f"总订单{len(df)} 总销售额{df['实际支付'].sum():.0f} 城市{df['城市'].nunique()} 类别{df['商品类别'].nunique()}")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(range(len(daily)), daily.values, color="#4C78A8", lw=1)
axes[0, 0].set_title("每日销售额趋势", fontsize=10); axes[0, 0].set_ylabel("销售额")
axes[0, 1].bar(city.index, city.values, width=0.6, color="#4C78A8")
axes[0, 1].set_title("各城市销售额", fontsize=10); axes[0, 1].tick_params(axis='x', rotation=30, labelsize=7)
for i, v in enumerate(city.values):
    axes[0, 1].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=6)
axes[1, 0].bar(cat.index, cat.values, width=0.6, color="#F58518")
axes[1, 0].set_title("各商品类别销售额", fontsize=10); axes[1, 0].tick_params(axis='x', rotation=30, labelsize=7)
for i, v in enumerate(cat.values):
    axes[1, 0].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=6)
axes[1, 1].barh(range(len(top)), top.values, height=0.6, color="#54A24B")
axes[1, 1].set_yticks(range(len(top))); axes[1, 1].set_yticklabels([s[:18] for s in top.index], fontsize=6)
axes[1, 1].invert_yaxis(); axes[1, 1].set_title("TOP10商品销售额", fontsize=10)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_销售看板.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

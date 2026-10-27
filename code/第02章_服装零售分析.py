"""第2章 PowerBI案例-服装零售分析 -> Python
原素材: 5、PowerBI基本操作/案例2/服装零售-原始数据.xlsx (12表星型模型: 零售单32106+店铺/员工/月目标等)
内涵: 服装代理商销售分析——多表关联, 按店铺/员工/月汇总成交金额, 对比月目标算完成率, 辅助业绩管理。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "5、PowerBI基本操作" / "案例2" / "服装零售-原始数据.xlsx"
ret = pd.read_excel(F, "零售单")
shop = pd.read_excel(F, "店铺表")
emp = pd.read_excel(F, "员工表")
smt = pd.read_excel(F, "店铺月目标表")
emt = pd.read_excel(F, "员工月目标表")

ret["订单日期"] = pd.to_datetime(ret["订单日期"])
ret["年月"] = ret["订单日期"].dt.strftime("%Y%m").astype(int)
ms = ret.groupby("年月")["成交金额"].sum().sort_index()

last = ret["年月"].max()
ss = ret[ret["年月"] == last].groupby("店铺id")["成交金额"].sum()
smt_l = smt[smt["年月"] == last].set_index("店铺id")["基础目标"]
comp = pd.DataFrame({"实际": ss, "目标": smt_l}).dropna()
comp = comp.merge(shop[["店铺id", "店铺名称"]], on="店铺id").sort_values("实际", ascending=False)
comp["完成率"] = comp["实际"] / comp["目标"]

es = ret.dropna(subset=["员工id"]).groupby(["年月", "员工id"])["成交金额"].sum().reset_index()
ec = es.merge(emt, on=["年月", "员工id"])
ec["完成率"] = ec["成交金额"] / ec["基础目标"]
print(f"月份: {sorted(ret['年月'].unique())}  总成交额={ret['成交金额'].sum():.0f}")
print(f"\n== 最近月({last})店铺目标完成率 ==")
print(comp[["店铺名称", "实际", "目标", "完成率"]].to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
axes[0, 0].bar(range(len(comp)), comp["目标"], width=0.4, color="#D9D9D9", label="基础目标", zorder=1)
axes[0, 0].bar([i + 0.42 for i in range(len(comp))], comp["实际"], width=0.4, color="#4C78A8", label="实际成交", zorder=3)
axes[0, 0].set_xticks([i + 0.2 for i in range(len(comp))]); axes[0, 0].set_xticklabels(comp["店铺名称"], rotation=30, ha="right", fontsize=7)
axes[0, 0].set_title(f"最近月({last})店铺实际vs基础目标", fontsize=10); axes[0, 0].legend(fontsize=7)
for i, r in comp.reset_index(drop=True).iterrows():
    axes[0, 0].text(i + 0.42, r["实际"], f"{r['完成率']:.0%}", ha='center', va='bottom', fontsize=6)

axes[0, 1].bar([str(m) for m in ms.index], ms.values, width=0.5, color="#F58518")
axes[0, 1].set_title("月度成交金额趋势", fontsize=10); axes[0, 1].tick_params(axis='x', rotation=30, labelsize=7)
for i, v in enumerate(ms.values):
    axes[0, 1].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=6)

valid = ec["完成率"][(ec["完成率"] > 0) & (ec["完成率"] < 3)]
axes[1, 0].hist(valid, bins=20, color="#4C78A8", edgecolor="white")
axes[1, 0].axvline(1.0, color="#E45756", ls="--", lw=1, label="100%完成")
axes[1, 0].set_title("员工月目标完成率分布", fontsize=10); axes[1, 0].legend(fontsize=7)

shop_all = ret.groupby("店铺id")["成交金额"].sum().reset_index().merge(shop[["店铺id", "店铺名称"]], on="店铺id").sort_values("成交金额", ascending=False)
axes[1, 1].bar(shop_all["店铺名称"], shop_all["成交金额"], width=0.6, color="#54A24B")
axes[1, 1].set_title("各店铺总成交金额", fontsize=10); axes[1, 1].tick_params(axis='x', rotation=30, labelsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_服装零售分析.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

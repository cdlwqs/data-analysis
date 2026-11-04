"""第5章 WPS归因分析-银行贷款申请 -> Python
原素材: 第5章 WPS归因分析案例-银行案例/归因分析数据.xlsx (贷款申请表1597行: 申请书/申请日期/申请渠道)
内涵: 归因分析按渠道、月份拆解贷款申请量, 量化各渠道对总量的贡献(归因),
      输出2021年5月月度报告, 指导线上化运营。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第5章 业务数据分析" / "第5章 WPS归因分析案例-银行案例" / "归因分析数据.xlsx"
df = pd.read_excel(F)
df["申请日期"] = pd.to_datetime(df["申请日期"])
df["年月"] = df["申请日期"].dt.strftime("%Y年%m月")

monthly = df.groupby("年月")["申请书编号（主键）"].count().sort_index()
chan = df.groupby("申请渠道")["申请书编号（主键）"].count().sort_values(ascending=False)
may = df[df["年月"] == "2021年5月"]
may_chan = may.groupby("申请渠道")["申请书编号（主键）"].count().sort_values(ascending=False)
print(f"总申请{len(df)}  渠道数={df['申请渠道'].nunique()}")
print("\n== 各渠道申请量(归因) ==\n", chan.to_string())
print(f"\n== 2021年5月 各渠道 ==\n{may_chan.to_string()}")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].bar(range(len(monthly)), monthly.values, width=0.6, color="#4C78A8")
axes[0, 0].set_xticks(range(len(monthly))); axes[0, 0].set_xticklabels(monthly.index, rotation=45, ha="right", fontsize=6)
axes[0, 0].set_title("各月贷款申请量趋势", fontsize=10)
axes[0, 1].pie(chan.values, labels=chan.index, autopct="%1.1f%%", textprops={"fontsize": 7})
axes[0, 1].set_title("各渠道申请量占比(归因)", fontsize=10)
axes[1, 0].bar(may_chan.index, may_chan.values, width=0.5, color="#F58518")
axes[1, 0].set_title("2021年5月各渠道申请量", fontsize=10); axes[1, 0].tick_params(axis='x', rotation=20, labelsize=7)
for i, v in enumerate(may_chan.values):
    axes[1, 0].text(i, v, str(v), ha='center', va='bottom', fontsize=7)
pivot = df.groupby(["年月", "申请渠道"])["申请书编号（主键）"].count().unstack(fill_value=0).sort_index()
pivot.plot(kind="bar", stacked=True, ax=axes[1, 1], width=0.7, legend=True, fontsize=6)
axes[1, 1].set_title("渠道×月份堆叠(归因)", fontsize=10); axes[1, 1].tick_params(axis='x', rotation=45, labelsize=6)
axes[1, 1].legend(fontsize=6, loc="upper left")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第05章_贷款归因分析.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

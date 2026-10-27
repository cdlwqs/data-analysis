"""第5章 银行PowerBI业务看板 -> Python
原素材: 第5章 PowerBI业务看板案例-银行案例/银行案例数据-学员用.xlsx
内涵: 银行理财销售BI看板——客户画像(年龄/性别/学历/收入/风险偏好)×购买行为(品类/金额/期限),
      本月销售目标2500万 vs 实际完成, 优化营销策略。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第5章 业务数据分析" / "第5章  PowerBI业务看板案例-银行案例" / "银行案例数据 - 学员用.xlsx"
risk = pd.read_excel(F, "风险偏好说明表")
cat = pd.read_excel(F, "品类说明表")
edu = pd.read_excel(F, "学历说明表")
df = pd.read_excel(F, "销售数据")
df = df.merge(cat, on="品类编号").merge(risk, on="风险编号").merge(edu, on="学历编号")

TARGET = 25000000
actual = df["购买金额"].sum()
print(f"销售目标={TARGET/1e4:.0f}万 实际完成={actual/1e4:.0f}万 完成率={actual/TARGET:.1%}")
by_cat = df.groupby("品类名称")["购买金额"].sum().sort_values(ascending=False)
by_age = df.groupby("年龄")["购买金额"].sum()
by_sex = df.groupby("性别")["购买金额"].sum()
by_risk = df.groupby("风险说明")["购买金额"].sum()
print("\n按品类:\n", by_cat.to_string())

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes[0, 0].bar(["目标", "实际"], [TARGET, actual], width=0.4, color=["#D9D9D9", "#4C78A8"])
axes[0, 0].set_title(f"销售目标完成率 {actual/TARGET:.1%}", fontsize=10)
for i, v in enumerate([TARGET, actual]):
    axes[0, 0].text(i, v, f"{v/1e4:.0f}万", ha='center', va='bottom', fontsize=8)
axes[0, 1].bar(by_cat.index, by_cat.values, width=0.6, color="#F58518")
axes[0, 1].set_title("各品类购买金额", fontsize=10); axes[0, 1].tick_params(axis='x', rotation=30, labelsize=7)
axes[0, 2].bar(by_age.index, by_age.values, width=0.6, color="#54A24B")
axes[0, 2].set_title("各年龄段购买金额", fontsize=10); axes[0, 2].tick_params(axis='x', labelsize=7)
axes[1, 0].bar(by_sex.index, by_sex.values, width=0.4, color="#4C78A8")
axes[1, 0].set_title("性别购买金额", fontsize=10)
axes[1, 1].bar(by_risk.index, by_risk.values, width=0.5, color="#E45756")
axes[1, 1].set_title("风险偏好购买金额", fontsize=10); axes[1, 1].tick_params(axis='x', labelsize=7)
by_edu = df.groupby("学历名称")["购买金额"].sum().sort_values(ascending=False)
axes[1, 2].bar(by_edu.index, by_edu.values, width=0.6, color="#9D9D9D")
axes[1, 2].set_title("学历购买金额", fontsize=10); axes[1, 2].tick_params(axis='x', rotation=20, labelsize=6)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第05章_银行理财看板.png"
plt.savefig(out, dpi=130)
print(f"图已保存: {out.name}")

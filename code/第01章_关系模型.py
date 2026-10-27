"""第1章 关系模型演示 -> Python
原素材: 第1章 数据分析思维/关系模型演示-不建议用poweBI操作关系型数据模型
内涵: 用8张3NF关系表(KDD99捷克银行)演示关系型数据模型——表通过外键关联,
      教材提示关系模型应在数据库中操作而非PowerBI。这里用pandas复现多表外键连接,
      体现关系模型"分解-连接"的核心价值。
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第1章 数据分析思维" / "关系模型演示-不建议用poweBI操作关系型数据模型"

accounts = pd.read_csv(D / "accounts.csv", encoding="gbk")
card = pd.read_csv(D / "card.csv", encoding="gbk")
clients = pd.read_csv(D / "clients.csv", encoding="gbk")
disp = pd.read_csv(D / "disp.csv", encoding="gbk")
district = pd.read_csv(D / "district.csv", encoding="gbk")
loans = pd.read_csv(D / "loans.csv", encoding="gbk")
order = pd.read_csv(D / "order.csv", encoding="gbk")
trans = pd.read_csv(D / "trans.csv", encoding="gbk", thousands=",", low_memory=False)

tables = {"accounts": accounts, "card": card, "clients": clients, "disp": disp,
          "district": district, "loans": loans, "order": order, "trans": trans}

print("== 关系模型: 8张表结构 ==")
for name, df in tables.items():
    print(f"{name:9s} shape={df.shape}  cols={list(df.columns)}")

print("\n== 外键关系 ==")
print("accounts.district_id -> district.A1")
print("clients.district_id  -> district.A1")
print("disp.client_id       -> clients.client_id")
print("disp.account_id      -> accounts.account_id")
print("card.disp_id         -> disp.disp_id")
print("loans.account_id     -> accounts.account_id")
print("order.account_id     -> accounts.account_id")
print("trans.account_id     -> accounts.account_id")

print("\n== 多表连接: 客户->账户->贷款->信用卡 (关系模型核心能力) ==")
cust_acct = clients.merge(disp, on="client_id").rename(columns={"type": "disp_type"})
cust_acct = cust_acct.merge(accounts, on="account_id")
wide = cust_acct.merge(loans, on="account_id", how="left").merge(card, on="disp_id", how="left").rename(columns={"type": "card_type"})
print(wide[["client_id", "sex", "account_id", "frequency", "loan_id", "amount", "status", "card_id", "card_type"]].head(8).to_string(index=False))

print("\n== 由连接结果得出的分析 ==")
loan_status = loans["status"].value_counts().sort_index()
print("贷款状态分布:\n", loan_status.to_string())
gender_loan = wide.groupby("sex")["amount"].agg(["count", "mean", "sum"])
print("\n男女客户贷款金额:\n", gender_loan.to_string())

fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
counts = pd.Series({k: len(v) for k, v in tables.items()})
axes[0].bar(counts.index, counts.values, width=0.6, color="#4C78A8")
axes[0].set_title("各表记录数", fontsize=10)
axes[0].tick_params(axis='x', rotation=30, labelsize=8)
for i, v in enumerate(counts.values):
    axes[0].text(i, v, f"{v:,}", ha='center', va='bottom', fontsize=7)

axes[1].bar(loan_status.index, loan_status.values, width=0.5, color="#F58518")
axes[1].set_title("贷款状态分布(A=正常结清 B=未结清)", fontsize=10)
for i, v in enumerate(loan_status.values):
    axes[1].text(i, v, str(v), ha='center', va='bottom', fontsize=8)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第01章_关系模型.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

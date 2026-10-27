"""第9章 用户标签体系与用户画像专题-信用卡客户画像 -> Python
原素材: 信用卡客户画像.sql + KDD99银行数据(accounts/card/clients/disp/trans.csv)
内涵: 以信用卡发卡为取数时点, 从账户交易流水构造客户画像变量:
  var1 性别+发卡时年龄;  var2 开卡前最后一笔交易间隔天数与账户余额;
  var3 开卡前365天内交易笔数/入账(借)/出账(贷)/出账占均余额比/出入账比.
  关联三表得信用卡用户画像, 用于发卡风控与客群刻画.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第9章 用户标签体系与用户画像专题" / "data"


def _money(s):
    return pd.to_numeric(s.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False), errors="coerce")


card = pd.read_csv(D / "card.csv", encoding="gbk")
disp = pd.read_csv(D / "disp.csv", encoding="gbk")
clients = pd.read_csv(D / "clients.csv", encoding="gbk")
trans = pd.read_csv(D / "trans.csv", encoding="gbk", low_memory=False)
trans["amount"] = _money(trans["amount"])
trans["balance"] = _money(trans["balance"])
trans["date"] = pd.to_datetime(trans["date"])
card["issued"] = pd.to_datetime(card["issued"])
clients["birth_date"] = pd.to_datetime(clients["birth_date"])

# var1: 性别 + 发卡时年龄
var1 = card.merge(disp[["disp_id", "client_id"]], on="disp_id", how="left")
var1 = var1.merge(clients[["client_id", "sex", "birth_date"]], on="client_id", how="left")
var1["age"] = (var1["issued"] - var1["birth_date"]).dt.days / 365
var1 = var1[["card_id", "disp_id", "issued", "type", "sex", "age"]]

# var2: 开卡前最后一笔交易的间隔天数与账户余额
cd = card[["card_id", "disp_id", "issued", "type"]].rename(columns={"type": "card_type"}).merge(disp[["disp_id", "account_id"]], on="disp_id", how="left")
v21 = cd.merge(trans[["account_id", "date", "balance"]], on="account_id", how="left")
v21 = v21[v21["issued"] > v21["date"]].copy()
v21["last_days"] = (v21["issued"] - v21["date"]).dt.days
idx = v21.groupby("card_id")["date"].idxmax()
var2 = v21.loc[idx].groupby(["card_id", "disp_id", "issued", "card_type", "date", "last_days"], as_index=False)["balance"].mean()
var2 = var2.rename(columns={"date": "trans_date"})[["card_id", "last_days", "balance"]]

# var3: 开卡前365天内交易笔数/入账/出账/出账占均余额比/出入账比
v3 = cd.merge(trans[["account_id", "date", "type", "amount", "balance", "trans_id"]], on="account_id", how="left")
gap = (v3["issued"] - v3["date"]).dt.days
v3 = v3[(gap > 0) & (gap < 365)].copy()
v3["in_amt"] = np.where(v3["type"] == "借", v3["amount"], 0)
v3["out_amt"] = np.where(v3["type"] == "贷", v3["amount"], 0)
g = v3.groupby("card_id")
var3 = pd.DataFrame({
    "card_id": list(g.groups.keys()),
}).set_index("card_id")
var3["trans_count"] = g["trans_id"].count()
var3["trans_in_amount"] = g["in_amt"].sum()
var3["trans_out_amount"] = g["out_amt"].sum()
var3["out_ratio"] = var3["trans_out_amount"] / g["balance"].mean()
var3["out_in_ratio"] = var3["trans_out_amount"] / var3["trans_in_amount"]
var3 = var3.reset_index()

# 关联得信用卡用户画像
pic = var1.merge(var2, on="card_id", how="left").merge(var3, on="card_id", how="left").sort_values("card_id")
print(f"画像样本 {len(pic)} 张卡")
print("== var1 性别/年龄 ==")
print(pic.groupby("sex")["age"].describe()[["count", "mean", "std", "min", "max"]].round(1).to_string())
print("\n== var2 开卡前末次交易间隔(天)与余额 ==")
print(pic[["last_days", "balance"]].describe().round(1).to_string())
print("\n== var3 开卡前365天交易特征 ==")
print(pic[["trans_count", "trans_in_amount", "trans_out_amount", "out_in_ratio"]].describe().round(2).to_string())

fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for sx, c in [("女", "#E45756"), ("男", "#4C78A8")]:
    a = pic.loc[pic["sex"] == sx, "age"].dropna()
    axes[0, 0].hist(a, bins=30, alpha=0.6, color=c, label=sx)
axes[0, 0].set_title("发卡时年龄分布(按性别)"); axes[0, 0].legend(fontsize=7)
axes[0, 1].hist(pic["last_days"].dropna(), bins=30, color="#F58518")
axes[0, 1].set_title("开卡前末次交易间隔(天)")
axes[0, 2].hist(np.log10(pic["balance"].dropna().clip(lower=1)), bins=30, color="#54A24B")
axes[0, 2].set_title("开卡前末次余额(log10)")
axes[1, 0].hist(pic["trans_count"].fillna(0), bins=30, color="#72B7B2")
axes[1, 0].set_title("开卡前365天交易笔数")
axes[1, 1].hist(pic["out_in_ratio"].replace([np.inf, -np.inf], np.nan).dropna(), bins=30, range=(0, 5), color="#B279A2")
axes[1, 1].set_title("出入账比(出/入)")
vc = pic.groupby("type")["card_id"].count()
axes[1, 2].bar(vc.index, vc.values, color="#9D9D9D")
axes[1, 2].set_title("卡类型分布")
for i, v in enumerate(vc.values):
    axes[1, 2].text(i, v, str(v), ha="center", va="bottom", fontsize=7)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第09章_信用卡客户画像.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

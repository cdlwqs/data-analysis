"""第2章 PowerBI基本操作-ETL练习(合并/拆分/清洗) -> Python
原素材: ETL练习文件/ (BI横向合并/纵向合并字段一致&不一致/拆分列/数据清洗 示例xlsx)
内涵: ETL四类核心操作用 pandas 复现——
  横向合并=merge(JOIN); 纵向合并=concat(字段一致直连, 不一致先rename再连);
  拆分列=str.split分列与爆炸; 数据清洗=跳标题行/去无效订单/修异常值.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法" / "5、PowerBI基本操作" / "ETL练习文件"

# === 1 横向合并: 学生表 JOIN 选课表 JOIN 课程表 ===
f = B / "合并演示数据" / "BI横向合并练习文件 .xlsx"
stu = pd.read_excel(f, sheet_name="学生表")
cou = pd.read_excel(f, sheet_name="课程表")
sc = pd.read_excel(f, sheet_name="选课表")
joined = sc.merge(stu, on="学号").merge(cou, on="课程号")
joined = joined[["学号", "姓名", "系别", "课程名", "学分", "成绩"]]
print("== 横向合并: 学生选课明细(前6行) ==")
print(joined.head(6).to_string(index=False))
avg_grade = joined.groupby("姓名")["成绩"].mean().sort_values(ascending=False)

# === 2 纵向合并-字段一致 ===
f1 = B / "合并演示数据" / "纵向合并演示-各字段名称一致.xlsx"
q1 = pd.read_excel(f1, sheet_name="第一季度"); q1["季度"] = "Q1"
q2 = pd.read_excel(f1, sheet_name="第二季度"); q2["季度"] = "Q2"
vsame = pd.concat([q1, q2], ignore_index=True)
print("\n== 纵向合并(字段一致) ==")
print(vsame.to_string(index=False))

# === 3 纵向合并-字段不一致(金额→销售额) ===
f2 = B / "合并演示数据" / "纵向合并演示-字段名称不一致.xlsx"
q1b = pd.read_excel(f2, sheet_name="第一季度"); q1b["季度"] = "Q1"
q2b = pd.read_excel(f2, sheet_name="第二季度").rename(columns={"金额": "销售额"}); q2b["季度"] = "Q2"
vdiff = pd.concat([q1b, q2b], ignore_index=True)
print("\n== 纵向合并(字段不一致,先重命名) ==")
print(vdiff.to_string(index=False))
store_sales = vsame.groupby("门店")["销售额"].sum()

# === 4 拆分列: 收货地址拆省/市/区, 订单号逗号分隔爆炸 ===
f3 = B / "ETL演示数据" / "拆分列示例数据.xlsx"
sp = pd.read_excel(f3)
sp[["省", "市", "区"]] = sp["收货地址"].str.extract(r"(.+?省|.+?市|.+?自治区)(.+?市|.+?州|.+?地区)(.+)")
sp = sp.assign(订单号=sp["订单号"].str.split(",")).explode("订单号")
print("\n== 拆分列: 地址拆省市区 + 订单号爆炸 ==")
print(sp[["订单号", "省", "市", "区", "商品名称", "客户姓名"]].to_string(index=False))

# === 5 数据清洗: 跳标题行/去无效订单/修异常ip ===
f4 = B / "ETL演示数据" / "数据清洗示例数据.xlsx"
raw = pd.read_excel(f4, sheet_name="sheet1", header=1)
n_raw = len(raw)
clean = raw[(raw["实付金额"] > 0) & (raw["下单数量"] > 0)].copy()
clean.loc[~clean["ip地址"].astype(str).str.contains(r"[\u4e00-\u9fff]市"), "ip地址"] = np.nan
n_clean = len(clean)
print(f"\n== 数据清洗: 原始{n_raw}行 → 清洗后{n_clean}行(去金额/数量≤0, 异常ip置空) ==")
print(clean[["订单号", "实付金额", "下单城市", "商品名称", "一级类别"]].head(5).to_string(index=False))
city_top = clean.groupby("下单城市")["实付金额"].sum().sort_values(ascending=False).head(8)

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
axes[0, 0].barh(avg_grade.index, avg_grade.values, color="#4C78A8")
axes[0, 0].set_title("横向合并: 各学生平均成绩"); axes[0, 0].invert_yaxis()
axes[0, 1].bar(store_sales.index, store_sales.values, color="#F58518")
axes[0, 1].set_title("纵向合并: 各门店两季度销售额")
for i, v in enumerate(store_sales.values):
    axes[0, 1].text(i, v, str(v), ha="center", va="bottom", fontsize=7)
prov_cnt = sp.groupby("省")["订单号"].count()
axes[1, 0].bar(prov_cnt.index, prov_cnt.values, color="#54A24B")
axes[1, 0].set_title("拆分列: 订单按省分布")
axes[1, 1].barh(city_top.index[::-1], city_top.values[::-1], color="#72B7B2")
axes[1, 1].set_title(f"数据清洗: 有效订单Top城市实付金额(清洗率{n_clean/n_raw:.0%})")
plt.tight_layout()
out = Path(__file__).resolve().parent / "第02章_ETL合并演示.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

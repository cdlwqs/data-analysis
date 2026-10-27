"""
02_clean.py — 数据清洗与治理
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

RAW_CSV = ROOT / "data" / "raw" / "listings.csv"
CLEAN_CSV = ROOT / "data" / "clean" / "listings_clean.csv"
REPORT_CSV = ROOT / "outputs" / "tables" / "cleaning_report.csv"


def main():
    # 读取原始数据
    df = pd.read_csv(RAW_CSV)
    n0 = len(df)
    print(f"原始数据行数: {n0}")

    steps = []  # 清洗步骤记录

    # 1) price 去掉 $ 和逗号，转 float
    df["price"] = (
        df["price"].astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace("nan", np.nan)
        .astype(float)
    )

    # 2) 过滤 price 异常值：0 < price <= 2000
    mask = (df["price"] > 0) & (df["price"] <= 2000)
    n_drop_price = int((~mask).sum())
    df = df[mask].copy()
    steps.append(("过滤price异常值(0<p<=2000)", n_drop_price))

    # 3) 过滤 availability_365 > 0
    mask = df["availability_365"] > 0
    n_drop_avail = int((~mask).sum())
    df = df[mask].copy()
    steps.append(("过滤availability_365<=0", n_drop_avail))

    # 4) review_scores_rating 缺失值填充中位数
    med = df["review_scores_rating"].median()
    df["review_scores_rating"] = df["review_scores_rating"].fillna(med)

    # 5) bedrooms / beds 缺失值填充 1
    df["bedrooms"] = df["bedrooms"].fillna(1)
    df["beds"] = df["beds"].fillna(1)

    # 6) last_review 转 datetime
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    # 7) 去重（按 id）
    n_before = len(df)
    df = df.drop_duplicates(subset=["id"]).copy()
    n_drop_dup = n_before - len(df)
    steps.append(("按id去重", n_drop_dup))

    # 8) 派生字段
    # price_per_person = price / accommodates
    df["price_per_person"] = df["price"] / df["accommodates"].replace(0, np.nan)

    # review_category: 高/中/低/无
    def review_cat(x):
        if pd.isna(x):
            return "无"
        if x >= 90:
            return "高"
        if x >= 80:
            return "中"
        return "低"
    df["review_category"] = df["review_scores_rating"].apply(review_cat)

    # is_superhost: t -> True, f -> False
    df["is_superhost"] = df["host_is_superhost"].astype(str).str.strip().str.lower().map(
        {"t": True, "f": False}
    )

    n1 = len(df)
    print(f"清洗后行数: {n1}")
    print(f"各步骤删除数:")
    for name, n in steps:
        print(f"  - {name}: {n}")

    # 输出清洗后数据
    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV, index=False)
    print(f"[完成] 清洗数据已保存: {CLEAN_CSV}")

    # 输出清洗报告
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    report = pd.DataFrame(steps, columns=["步骤", "删除行数"])
    report.loc[len(report)] = ["原始行数", n0]
    report.loc[len(report)] = ["清洗后行数", n1]
    report.to_csv(REPORT_CSV, index=False, encoding="utf-8-sig")
    print(f"[完成] 清洗报告已保存: {REPORT_CSV}")


if __name__ == "__main__":
    main()

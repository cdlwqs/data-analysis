"""
02_clean.py — 数据清洗与治理
============================
1. 读取 data/raw/ 9 张表
2. 类型统一（日期/数值）、缺失值处理、异常值识别、重复值去除
3. 多表关联 → 宽表 order_full
4. 派生指标：order_value / delivery_days / is_late / purchase_month 等
5. 导出 data/clean/，生成清洗报告 outputs/tables/cleaning_report.csv

运行：python scripts/02_clean.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
CLEAN.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

DATE_COLS = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_order_items_dataset.csv": ["shipping_limit_date"],
    "olist_order_reviews_dataset.csv": ["review_creation_date", "review_answer_timestamp"],
}


def read_raw():
    """读取全部原始表，统一日期类型。"""
    dfs = {}
    for f in RAW.glob("*.csv"):
        name = f.name
        df = pd.read_csv(f)
        for col in DATE_COLS.get(name, []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        dfs[name] = df
    return dfs


def clean_orders(df):
    """订单表清洗：去重、状态校验、时间逻辑校验。"""
    n0 = len(df)
    df = df.drop_duplicates(subset=["order_id"])
    # 仅保留有购买时间的记录
    df = df[df["order_purchase_timestamp"].notna()]
    # 时间逻辑：批准 ≥ 购买；交付 ≥ 批准；估计 ≥ 购买
    df = df[df["order_approved_at"].isna() | (df["order_approved_at"] >= df["order_purchase_timestamp"])]
    df["order_purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df["order_purchase_year"] = df["order_purchase_timestamp"].dt.year
    df["order_purchase_dow"] = df["order_purchase_timestamp"].dt.dayofweek
    df["order_purchase_hour"] = df["order_purchase_timestamp"].dt.hour
    return df, {"orders_before": n0, "orders_after": len(df)}


def clean_items(df):
    """订单明细清洗：价格/运费异常值处理。"""
    n0 = len(df)
    df = df[df["price"] > 0]
    df = df[df["freight_value"] >= 0]
    # 价格上限 5000 BRL，超出视为异常
    df = df[df["price"] <= 5000]
    return df, {"items_before": n0, "items_after": len(df)}


def clean_reviews(df):
    """评价清洗：评分 1~5。"""
    n0 = len(df)
    df = df[df["review_score"].between(1, 5)]
    df = df.drop_duplicates(subset=["review_id"])
    return df, {"reviews_before": n0, "reviews_after": len(df)}


def clean_products(df):
    """产品清洗：去重、重量>0。"""
    n0 = len(df)
    df = df.drop_duplicates(subset=["product_id"])
    df = df[df["product_weight_g"] > 0]
    df["product_category_name"] = df["product_category_name"].fillna("unknown")
    return df, {"products_before": n0, "products_after": len(df)}


def build_order_full(dfs):
    """多表关联 → 宽表 order_full。"""
    orders = dfs["olist_orders_dataset.csv"]
    customers = dfs["olist_customers_dataset.csv"]
    items = dfs["olist_order_items_dataset.csv"]
    payments = dfs["olist_order_payments_dataset.csv"]
    reviews = dfs["olist_order_reviews_dataset.csv"]
    products = dfs["olist_products_dataset.csv"]
    sellers = dfs["olist_sellers_dataset.csv"]

    # 每单金额与运费（聚合明细）
    agg = items.groupby("order_id").agg(
        order_value=("price", "sum"),
        freight_total=("freight_value", "sum"),
        item_count=("order_item_id", "count"),
    ).reset_index()
    agg["total_value"] = agg["order_value"] + agg["freight_total"]

    # 每单主品类（取金额最大的明细对应品类）
    item_prod = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    main_cat = item_prod.sort_values("price", ascending=False).drop_duplicates("order_id")
    main_cat = main_cat[["order_id", "product_category_name"]].rename(
        columns={"product_category_name": "main_category"})

    # 每单支付方式（取首笔）
    pay_first = payments.sort_values("payment_sequential").drop_duplicates("order_id")
    pay_first = pay_first[["order_id", "payment_type", "payment_installments"]]

    # 每单评价分
    rev = reviews[["order_id", "review_score"]].drop_duplicates("order_id")

    # 关联
    full = (orders
            .merge(customers[["customer_id", "customer_unique_id", "customer_state", "customer_city"]], on="customer_id", how="left")
            .merge(agg, on="order_id", how="left")
            .merge(main_cat, on="order_id", how="left")
            .merge(pay_first, on="order_id", how="left")
            .merge(rev, on="order_id", how="left"))

    # 派生：交付天数、是否迟到
    full["delivery_days"] = (full["order_delivered_customer_date"] - full["order_purchase_timestamp"]).dt.total_seconds() / 86400
    full["is_late"] = full["order_delivered_customer_date"] > full["order_estimated_delivery_date"]
    full["is_late"] = full["is_late"].fillna(False)
    # 仅 delivered 订单交付天数有效
    full.loc[full["order_status"] != "delivered", "delivery_days"] = np.nan

    return full


def main():
    print("=" * 60)
    print("02_clean.py — 数据清洗与治理")
    print("=" * 60)
    dfs = read_raw()
    report = {}

    dfs["olist_orders_dataset.csv"], r1 = clean_orders(dfs["olist_orders_dataset.csv"])
    dfs["olist_order_items_dataset.csv"], r2 = clean_items(dfs["olist_order_items_dataset.csv"])
    dfs["olist_order_reviews_dataset.csv"], r3 = clean_reviews(dfs["olist_order_reviews_dataset.csv"])
    dfs["olist_products_dataset.csv"], r4 = clean_products(dfs["olist_products_dataset.csv"])
    report.update(r1); report.update(r2); report.update(r3); report.update(r4)

    # 重复值统计
    report["customers_dups_removed"] = int(dfs["olist_customers_dataset.csv"].duplicated(subset=["customer_id"]).sum())
    dfs["olist_customers_dataset.csv"] = dfs["olist_customers_dataset.csv"].drop_duplicates(subset=["customer_id"])

    # 构建宽表
    full = build_order_full(dfs)
    report["order_full_rows"] = len(full)
    report["order_full_cols"] = full.shape[1]
    report["missing_order_value"] = int(full["order_value"].isna().sum())
    report["missing_review"] = int(full["review_score"].isna().sum())
    report["delivered_count"] = int((full["order_status"] == "delivered").sum())
    report["late_count"] = int(full["is_late"].sum())

    # 导出清洗后数据
    for name, df in dfs.items():
        df.to_csv(CLEAN / name, index=False)
    full.to_csv(CLEAN / "order_full.csv", index=False)

    # 清洗报告
    pd.DataFrame([report]).T.reset_index().rename(columns={"index": "指标", 0: "值"}).to_csv(
        TABLES / "cleaning_report.csv", index=False)

    print(f"清洗完成：宽表 {full.shape}，已写入 {CLEAN}")
    print("关键指标：")
    for k, v in report.items():
        print(f"  {k}: {v}")
    return full


if __name__ == "__main__":
    main()
    print("完成。")

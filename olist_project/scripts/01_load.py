"""
01_load.py — 数据获取（合规、非爬虫）
================================================
数据源：Kaggle · Olist Brazilian E-Commerce Public Dataset
URL   : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

获取方式（白名单，二选一）：
  1) Kaggle 官方 CLI 下载（需 ~/.kaggle/kaggle.json 凭证）
  2) Faker 按 Olist 官方 Schema 生成合成数据（回退，单独标注 is_synthetic=True）

严禁爬虫。本脚本不涉及任何网页抓取行为。
运行：python scripts/01_load.py
"""
import os
import sys
import time
import random
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

KAGGLE_DATASET = "olistbr/brazilian-ecommerce"
EXPECTED_FILES = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
]


def try_kaggle_download() -> bool:
    """尝试用 Kaggle 官方 CLI 下载真实数据集。成功返回 True。"""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        zip_path = RAW / "brazilian-ecommerce.zip"
        api.dataset_download_files(KAGGLE_DATASET, path=str(RAW), unzip=True)
        if all((RAW / f).exists() for f in EXPECTED_FILES):
            print("[Kaggle] 真实数据下载成功。")
            return True
    except Exception as e:
        print(f"[Kaggle] 不可用（{type(e).__name__}: {e}），将回退到 Faker 合成数据。")
    return False


def generate_synthetic() -> None:
    """用 Faker 按 Olist 官方 Schema 生成合成数据，分布贴近真实电商。"""
    from faker import Faker
    Faker.seed(42)
    random.seed(42)
    np.random.seed(42)
    fk = Faker("pt_BR")

    n_orders = 15000
    n_unique_customers = 12000
    n_products = 3000
    n_sellers = 600

    # 巴西 27 州及主要城市
    states = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "DF", "ES",
              "PE", "CE", "PA", "MT", "MS", "PB", "RN", "AL", "SE", "PI",
              "TO", "MA", "AM", "RO", "AC", "AP", "RR"]
    cities = {
        "SP": ["sao paulo", "campinas", "guarulhos", "santo andre"],
        "RJ": ["rio de janeiro", "niteroi", "duque de caxias"],
        "MG": ["belo horizonte", "uberlandia", "contagem"],
    }

    def city_of(st):
        return random.choice(cities.get(st, [fk.city().lower()]))

    # 真实 Olist 产品类别（葡语）
    categories = [
        "cama_mesa_banho", "moveis_decoracao", "esporte_lazer", "beleza_saude",
        "utilidades_domesticas", "automotivo", "moveis_escritorio", "informatica_acessorios",
        "brinquedos", "relogios_presentes", "telefonia", "ferramentas_ferramentas",
        "perfumaria", "instrumentos_musicais", "consoles_games", "cool_stuff",
        "eletroportateis", "eletrodomesticos", "papelaria", "agro_industria_e_comercio",
        "pc_gamer", "audio", "alimentos_bebidas", "bebes", "pet_shop",
        "moveis_sala", "moveis_quarto", "moveis_cozinha", "casa_conforto_2",
        "fashion_bolsas_e_acessorios", "fashion_roupa_masculina", "fashion_roupa_feminina",
        "fashion_calcados", "fashion_underwear_e_moda_praia", "la_cuisine",
        "artes_e_artesanato", "dvds_blu_ray", "livros_interesse_geral",
        "musica", "tablets_impressao_imagem_e_notebook", "climatizacao",
        "construcao_ferramentas_construcao", "construcao_ferramentas_jardim",
        "construcao_ferramentas_seguranca", "industria_comercio_e_negocios",
        "market_place", "portateis_cozinha_e_preparadores_de_alimentos",
        "cds_dvds_musica_e_livros", "seguros_e_servicos", "alimentos", "bebidas",
    ]

    print(f"[Faker] 开始生成合成数据：{n_orders} 订单 / {n_unique_customers} 客户 / {n_products} 产品 / {n_sellers} 卖家 ...")

    # 1) sellers
    seller_states = np.random.choice(states, n_sellers)
    sellers = pd.DataFrame({
        "seller_id": [f"SELL_{i:06d}" for i in range(n_sellers)],
        "seller_zip_code_prefix": np.random.randint(1000, 99999, n_sellers),
        "seller_city": [city_of(st) for st in seller_states],
        "seller_state": seller_states,
    })

    # 2) products
    prod_cat = np.random.choice(categories, n_products, p=np.random.dirichlet(np.ones(len(categories))))
    products = pd.DataFrame({
        "product_id": [f"PROD_{i:06d}" for i in range(n_products)],
        "product_category_name": prod_cat,
        "product_name_lenght": np.random.randint(20, 80, n_products),
        "product_description_lenght": np.random.randint(100, 2000, n_products),
        "product_photos_qty": np.random.poisson(1.5, n_products) + 1,
        "product_weight_g": np.random.lognormal(5.5, 0.8, n_products).round(0),
        "product_length_cm": np.random.randint(5, 60, n_products),
        "product_height_cm": np.random.randint(2, 40, n_products),
        "product_width_cm": np.random.randint(5, 50, n_products),
    })

    # 3) customers (unique + order-level)
    cust_states = np.random.choice(states, n_unique_customers)
    unique_ids = [f"UNIQ_{i:07d}" for i in range(n_unique_customers)]
    unique_state_map = dict(zip(unique_ids, cust_states))
    # 每个订单一个 customer_id（Olist 约定），多数客户仅 1 单，少量复购
    order_customer_unique = np.random.choice(unique_ids, n_orders, p=np.random.dirichlet(np.ones(n_unique_customers) * 2))
    order_states = [unique_state_map[u] for u in order_customer_unique]
    customers = pd.DataFrame({
        "customer_id": [f"CUST_{i:07d}" for i in range(n_orders)],
        "customer_unique_id": order_customer_unique,
        "customer_zip_code_prefix": np.random.randint(1000, 99999, n_orders),
        "customer_city": [city_of(st) for st in order_states],
        "customer_state": order_states,
    })

    # 4) orders（时间 2016-10 ~ 2018-08）
    start = pd.Timestamp("2016-10-01")
    end = pd.Timestamp("2018-08-31")
    span_days = (end - start).days
    purchase_ts = start + pd.to_timedelta(np.random.randint(0, span_days * 24 * 60, n_orders), unit="m")
    purchase_ts = pd.to_datetime(purchase_ts)
    status_choices = ["delivered", "shipped", "canceled", "unavailable", "invoiced", "processing", "approved", "created"]
    status_p = [0.97, 0.005, 0.012, 0.001, 0.004, 0.003, 0.003, 0.002]
    order_status = np.random.choice(status_choices, n_orders, p=status_p)
    orders = pd.DataFrame({
        "order_id": [f"ORD_{i:07d}" for i in range(n_orders)],
        "customer_id": customers["customer_id"].values,
        "order_status": order_status,
        "order_purchase_timestamp": purchase_ts,
    })
    # 派生时间字段
    approved = purchase_ts + pd.to_timedelta(np.random.exponential(0.5, n_orders), unit="h")
    carrier = approved + pd.to_timedelta(np.random.exponential(24, n_orders), unit="h")
    delivered = carrier + pd.to_timedelta(np.random.exponential(72, n_orders), unit="h")
    estimated = approved + pd.to_timedelta(np.random.uniform(5, 25, n_orders), unit="D")
    orders["order_approved_at"] = approved
    orders["order_delivered_carrier_date"] = carrier
    orders["order_delivered_customer_date"] = delivered
    orders["order_estimated_delivery_date"] = estimated
    # canceled 订单无后续时间
    mask_cancel = orders["order_status"] == "canceled"
    for col in ["order_approved_at", "order_delivered_carrier_date",
                "order_delivered_customer_date", "order_estimated_delivery_date"]:
        orders.loc[mask_cancel, col] = pd.NaT

    # 5) order_items（每单 1~4 件）
    rows = []
    for oid, pid_pool in zip(orders["order_id"], range(n_orders)):
        n_item = np.random.choice([1, 2, 3, 4], p=[0.78, 0.15, 0.05, 0.02])
        for j in range(1, n_item + 1):
            rows.append({
                "order_id": oid,
                "order_item_id": j,
                "product_id": f"PROD_{np.random.randint(0, n_products):06d}",
                "seller_id": f"SELL_{np.random.randint(0, n_sellers):06d}",
                "shipping_limit_date": pd.Timestamp("2016-10-01") + pd.to_timedelta(np.random.randint(0, 700 * 24), unit="h"),
                "price": round(float(np.random.lognormal(4.35, 0.7)), 2),
                "freight_value": round(float(np.random.lognormal(2.0, 0.6)), 2),
            })
    order_items = pd.DataFrame(rows)

    # 6) payments（用 groupby 预算每单金额，避免 O(n²)）
    pay_types = ["credit_card", "boleto", "voucher", "debit_card"]
    pay_p = [0.74, 0.19, 0.05, 0.02]
    amt_per_order = order_items.groupby("order_id")["price"].sum()
    pay_rows = []
    for oid in orders["order_id"]:
        amt = float(amt_per_order.get(oid, 0.0))
        pay_rows.append({
            "order_id": oid,
            "payment_sequential": 1,
            "payment_type": np.random.choice(pay_types, p=pay_p),
            "payment_installments": int(np.random.choice([1, 1, 1, 2, 3, 6, 10], p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05])),
            "payment_value": round(amt, 2),
        })
    payments = pd.DataFrame(pay_rows)

    # 7) reviews
    scores = np.random.choice([1, 2, 3, 4, 5], n_orders, p=[0.08, 0.05, 0.10, 0.22, 0.55])
    reviews = pd.DataFrame({
        "review_id": [f"REV_{i:07d}" for i in range(n_orders)],
        "order_id": orders["order_id"].values,
        "review_score": scores,
        "review_comment_title": "",
        "review_comment_message": "",
        "review_creation_date": purchase_ts + pd.to_timedelta(np.random.randint(1, 30, n_orders), unit="D"),
        "review_answer_timestamp": purchase_ts + pd.to_timedelta(np.random.randint(2, 35, n_orders), unit="D"),
    })

    # 8) geolocation（按州聚合若干坐标）
    geo_rows = []
    for st in states:
        for _ in range(20):
            geo_rows.append({
                "geolocation_zip_code_prefix": int(np.random.randint(1000, 99999)),
                "geolocation_lat": round(float(np.random.uniform(-33, 5)), 6),
                "geolocation_lng": round(float(np.random.uniform(-74, -34)), 6),
                "geolocation_city": city_of(st),
                "geolocation_state": st,
            })
    geolocation = pd.DataFrame(geo_rows)

    # 9) category translation
    cat_trans = pd.DataFrame({
        "product_category_name": categories,
        "product_category_name_english": [c.replace("_", " ").title() for c in categories],
    })

    # 标注合成
    for df in [orders, customers, order_items, payments, reviews, products, sellers, geolocation]:
        df["is_synthetic"] = True

    tables = {
        "olist_orders_dataset.csv": orders,
        "olist_customers_dataset.csv": customers,
        "olist_order_items_dataset.csv": order_items,
        "olist_order_payments_dataset.csv": payments,
        "olist_order_reviews_dataset.csv": reviews,
        "olist_products_dataset.csv": products,
        "olist_sellers_dataset.csv": sellers,
        "olist_geolocation_dataset.csv": geolocation,
        "product_category_name_translation.csv": cat_trans,
    }
    for name, df in tables.items():
        df.to_csv(RAW / name, index=False)
    print(f"[Faker] 合成数据已写入 {RAW}（共 {len(tables)} 张表）。")


def main() -> str:
    print("=" * 60)
    print("01_load.py — Olist 数据获取")
    print("=" * 60)
    # 若 raw 已有完整数据则跳过
    if all((RAW / f).exists() for f in EXPECTED_FILES):
        print("[Skip] data/raw/ 已存在完整数据，跳过获取。")
        return "skip"
    if try_kaggle_download():
        return "kaggle"
    generate_synthetic()
    return "synthetic"


if __name__ == "__main__":
    mode = main()
    print(f"\n获取方式：{mode}")
    print("完成。")

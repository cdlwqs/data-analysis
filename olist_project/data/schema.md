# Olist 巴西电商数据集 Schema 说明

> 数据源：Kaggle · Olist Brazilian E-Commerce Public Dataset
> URL：https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
> License：Olist 已公开发布用于分析与教学用途

## 获取方式（白名单）

1. **首选**：Kaggle 官方 CLI `kaggle datasets download -d olistbr/brazilian-ecommerce`（需配置 `~/.kaggle/kaggle.json` 凭证）。
2. **回退**：当本机无 Kaggle 凭证时，`scripts/01_load.py` 使用 Faker 按 Olist 官方 Schema 生成结构一致、分布贴近真实的合成数据，并在每条记录上标注 `is_synthetic=True`，便于复用与验证。

## 9 张表结构与主外键

| 表文件 | 主键 | 外键 | 主要字段 |
|---|---|---|---|
| olist_orders_dataset.csv | order_id | customer_id | order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date |
| olist_customers_dataset.csv | customer_id | customer_unique_id, customer_zip_code_prefix | customer_city, customer_state |
| olist_order_items_dataset.csv | (order_id, order_item_id) | order_id, product_id, seller_id | shipping_limit_date, price, freight_value |
| olist_order_payments_dataset.csv | (order_id, payment_sequential) | order_id | payment_type, payment_installments, payment_value |
| olist_order_reviews_dataset.csv | review_id | order_id | review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp |
| olist_products_dataset.csv | product_id | product_category_name | product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm |
| olist_sellers_dataset.csv | seller_id | seller_zip_code_prefix | seller_city, seller_state |
| olist_geolocation_dataset.csv | (geolocation_zip_code_prefix, ...) | — | geolocation_lat, geolocation_lng, geolocation_city, geolocation_state |
| product_category_name_translation.csv | product_category_name | — | product_category_name_english |

## 关联关系

```
orders.customer_id        -> customers.customer_id
customers.customer_unique_id  -> (客户唯一身份，跨订单)
order_items.order_id      -> orders.order_id
order_items.product_id    -> products.product_id
order_items.seller_id     -> sellers.seller_id
payments.order_id         -> orders.order_id
reviews.order_id          -> orders.order_id
customers.customer_zip_code_prefix -> geolocation.geolocation_zip_code_prefix
```

## 合成数据声明

当使用 Faker 回退生成时：
- 订单量约 15,000 条，唯一客户约 12,000，产品约 3,000，卖家约 600；
- 价格服从对数正态分布（中位数≈85 BRL），评价分偏向 4–5，支付方式以 credit_card 为主；
- 时间范围 2016-10 至 2018-08，与真实 Olist 一致；
- 所有合成记录 `is_synthetic=True`，已在 README 与论文中单独标注。

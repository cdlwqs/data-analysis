"""
03_analysis.py — 商业分析模型（核心模块）
纽约Airbnb民宿项目：5种商业分析模型
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

INPUT = ROOT / "data" / "clean" / "listings_clean.csv"


def load_data():
    """读取清洗后数据"""
    df = pd.read_csv(INPUT)
    print(f"读取数据: {df.shape[0]} 行, {df.shape[1]} 列")
    return df


# ============================================================
# 1. K-Means 聚类（房源类型聚类）
# ============================================================
def kmeans_cluster(df):
    print("\n" + "=" * 60)
    print("1. K-Means 聚类（房源类型聚类）")
    print("=" * 60)

    features = ["price", "minimum_nights", "number_of_reviews",
                "availability_365", "review_scores_rating",
                "calculated_host_listings_count"]
    X = df[features].copy()
    # 缺失值填充
    X = X.fillna(X.median())

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means 聚类
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)

    # 输出每个房源的 cluster 标签
    cluster_df = pd.DataFrame({
        "id": df["id"].values,
        "cluster": labels
    })
    cluster_df.to_csv(TABLES / "kmeans_clusters.csv", index=False)

    # 输出聚类中心（反标准化为原始量纲）
    centers = pd.DataFrame(
        scaler.inverse_transform(km.cluster_centers_),
        columns=features
    )
    centers.insert(0, "cluster", range(4))
    centers.to_csv(TABLES / "kmeans_centers.csv", index=False)

    # 打印各聚类数量和特征均值
    tmp = df.copy()
    tmp["cluster"] = labels
    print("\n各聚类数量:")
    print(tmp["cluster"].value_counts().sort_index())
    print("\n各聚类特征均值:")
    print(tmp.groupby("cluster")[features].mean().round(2))


# ============================================================
# 2. 随机森林回归（定价预测）
# ============================================================
def rf_price_predict(df):
    print("\n" + "=" * 60)
    print("2. 随机森林回归（定价预测）")
    print("=" * 60)

    cat_cols = ["room_type", "neighbourhood_group_cleansed"]
    num_cols = ["accommodates", "bedrooms", "beds", "minimum_nights",
                "availability_365", "number_of_reviews",
                "review_scores_rating", "calculated_host_listings_count"]

    X = df[cat_cols + num_cols].copy()
    y = df["price"].copy()

    # one-hot 编码
    X = pd.get_dummies(X, columns=cat_cols, drop_first=False)
    # 缺失值填充
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())
    y = y.fillna(y.median())

    # 80/20 训练测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 随机森林回归
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    # 评估指标
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    print(f"\nR2 = {r2:.4f}")
    print(f"RMSE = {rmse:.4f}")

    # 输出预测值 vs 实际值
    pred_df = pd.DataFrame({
        "y_true": y_test.values,
        "y_pred": y_pred
    })
    pred_df.to_csv(TABLES / "rf_predictions.csv", index=False)

    # 特征重要性排序
    fi = pd.DataFrame({
        "feature": X.columns,
        "importance": rf.feature_importances_
    }).sort_values("importance", ascending=False)
    fi.to_csv(TABLES / "rf_feature_importance.csv", index=False)

    # 评估指标
    metrics_df = pd.DataFrame({
        "metric": ["R2", "RMSE", "MAE"],
        "value": [r2, rmse, mae]
    })
    metrics_df.to_csv(TABLES / "rf_metrics.csv", index=False)


# ============================================================
# 3. RFM 变体（房东价值分层）
# ============================================================
def rfm_host(df):
    print("\n" + "=" * 60)
    print("3. RFM 变体（房东价值分层）")
    print("=" * 60)

    today = pd.Timestamp.today().normalize()

    # 处理 last_review
    df_r = df.copy()
    df_r["last_review"] = pd.to_datetime(df_r["last_review"], errors="coerce")

    # R: 最近评论距今天数（越小越好）
    r = df_r.groupby("host_id")["last_review"].max()
    r_days = (today - r).dt.days
    r_days = r_days.fillna(r_days.max() + 365)  # 无评论者给最大值

    # F: 总评论数
    f = df_r.groupby("host_id")["number_of_reviews"].sum()

    # M: 总房源数 * 平均价格
    m_count = df_r.groupby("host_id")["id"].count()
    m_price = df_r.groupby("host_id")["price"].mean()
    m = m_count * m_price

    rfm = pd.DataFrame({
        "host_id": r_days.index,
        "R": r_days.values,
        "F": f.values,
        "M": m.values
    })

    # 以中位数分高低
    r_med = rfm["R"].median()
    f_med = rfm["F"].median()
    m_med = rfm["M"].median()
    rfm["R_label"] = np.where(rfm["R"] <= r_med, 1, 0)  # R 越小越好 → 1=高
    rfm["F_label"] = np.where(rfm["F"] >= f_med, 1, 0)
    rfm["M_label"] = np.where(rfm["M"] >= m_med, 1, 0)

    # 8 类命名
    seg_map = {
        (1, 1, 1): "重要价值", (1, 1, 0): "重要发展",
        (1, 0, 1): "重要保持", (1, 0, 0): "重要挽留",
        (0, 1, 1): "一般价值", (0, 1, 0): "一般发展",
        (0, 0, 1): "一般保持", (0, 0, 0): "一般挽留",
    }
    rfm["segment"] = rfm.apply(
        lambda x: seg_map[(x["R_label"], x["F_label"], x["M_label"])], axis=1
    )

    rfm_out = rfm[["host_id", "R", "F", "M", "segment"]]
    rfm_out.to_csv(TABLES / "host_rfm.csv", index=False)

    # 各 segment 统计
    summary = rfm.groupby("segment").agg(
        房东数=("host_id", "count"),
        R均值=("R", "mean"),
        F均值=("F", "mean"),
        M均值=("M", "mean"),
    ).round(2)
    summary.to_csv(TABLES / "host_rfm_summary.csv")

    print("\n各 segment 房东数:")
    print(rfm["segment"].value_counts())


# ============================================================
# 4. 帕累托 / ABC 分析（街区贡献）
# ============================================================
def pareto_abc(df):
    print("\n" + "=" * 60)
    print("4. 帕累托 / ABC 分析（街区贡献）")
    print("=" * 60)

    g = df.groupby("neighbourhood_cleansed").agg(
        房源数=("id", "count"),
        平均价格=("price", "mean"),
    )
    g["贡献"] = g["房源数"] * g["平均价格"]
    g = g.sort_values("贡献", ascending=False)

    total = g["贡献"].sum()
    g["累计占比"] = g["贡献"].cumsum() / total

    # ABC 分类
    def abc_class(x):
        if x <= 0.70:
            return "A"
        elif x <= 0.90:
            return "B"
        else:
            return "C"
    g["ABC"] = g["累计占比"].apply(abc_class)

    g.reset_index().to_csv(TABLES / "pareto_abc.csv", index=False)

    # 打印各类数量和贡献占比
    print("\nA/B/C 各类数量:")
    print(g["ABC"].value_counts().sort_index())
    print("\nA/B/C 各类贡献占比:")
    print((g.groupby("ABC")["贡献"].sum() / total).round(4))


# ============================================================
# 5. 时间序列 / 移动平均（评论趋势）
# ============================================================
def monthly_trend(df):
    print("\n" + "=" * 60)
    print("5. 时间序列 / 移动平均（评论趋势）")
    print("=" * 60)

    d = df.copy()
    d["last_review"] = pd.to_datetime(d["last_review"], errors="coerce")
    d = d.dropna(subset=["last_review"])
    d["month"] = d["last_review"].dt.to_period("M").astype(str)

    monthly = d.groupby("month")["number_of_reviews"].sum().sort_index()
    trend = pd.DataFrame({
        "month": monthly.index,
        "评论数": monthly.values,
    })

    # 3 月移动平均
    trend["3月移动平均"] = trend["评论数"].rolling(window=3, min_periods=1).mean()

    # 同比增长率（与 12 个月前相比）
    trend["同比增长率"] = trend["评论数"].pct_change(periods=12)
    trend["同比增长率"] = trend["同比增长率"].round(4)

    trend.to_csv(TABLES / "monthly_trend.csv", index=False)

    print(f"\n月份数: {len(trend)}")
    print(f"最近月份评论数: {trend['评论数'].iloc[-1]}")


# ============================================================
# 主流程
# ============================================================
def main():
    df = load_data()
    kmeans_cluster(df)
    rf_price_predict(df)
    rfm_host(df)
    pareto_abc(df)
    monthly_trend(df)
    print("\n全部完成，结果已输出到:", TABLES)


if __name__ == "__main__":
    main()

"""
03_analysis.py — 商业分析模型（核心模块）
=========================================
应用 4 种模型于 Olist 清洗后数据，每种产出结果表 + 商业结论：
  1. RFM 用户价值八分类（中位数切分）
  2. 同期群留存分析（首次购买月分群，月度留存率矩阵）
  3. 帕累托 / ABC 分类（产品类别销售额 20/80）
  4. 环比/同比 + 移动平均（月度销售额趋势）

结果写入 outputs/tables/，供 04_visuals.py 绘图。
运行：python scripts/03_analysis.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)


def load():
    return pd.read_csv(CLEAN / "order_full.csv", parse_dates=["order_purchase_timestamp"])


# ---------- 1. RFM ----------
def rfm_model(full):
    """RFM 八分类。R/F/M 用中位数切分高低（业务依据：中位数对偏态分布稳健）。"""
    df = full[full["order_status"].isin(["delivered", "shipped"])].copy()
    df = df[df["order_value"].notna() & (df["order_value"] > 0)]
    snapshot = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("customer_unique_id").agg(
        R=("order_purchase_timestamp", lambda x: (snapshot - x.max()).days),
        F=("order_id", "nunique"),
        M=("order_value", "sum"),
    ).reset_index()
    # 中位数切分（>中位数为高）
    r_rmed, f_rmed, m_rmed = rfm["R"].median(), rfm["F"].median(), rfm["M"].median()
    rfm["R_high"] = rfm["R"] <= r_rmed          # R 越小越好
    rfm["F_high"] = rfm["F"] > f_rmed
    rfm["M_high"] = rfm["M"] > m_rmed

    def segment(row):
        r, f, m = row["R_high"], row["F_high"], row["M_high"]
        if r and f and m: return "重要价值客户"
        if r and f and not m: return "重要保持客户"
        if r and not f and m: return "重要发展客户"
        if r and not f and not m: return "重要挽留客户"
        if not r and f and m: return "一般价值客户"
        if not r and f and not m: return "一般保持客户"
        if not r and not f and m: return "一般发展客户"
        return "一般挽留客户"
    rfm["segment"] = rfm.apply(segment, axis=1)
    rfm.to_csv(TABLES / "rfm.csv", index=False)
    seg_summary = rfm.groupby("segment").agg(
        客户数=("customer_unique_id", "count"),
        平均R=("R", "mean"), 平均F=("F", "mean"), 平均M=("M", "mean"),
        累计金额=("M", "sum"),
    ).reset_index().sort_values("累计金额", ascending=False)
    seg_summary.to_csv(TABLES / "rfm_segment_summary.csv", index=False)
    print(f"[RFM] 客户 {len(rfm)}，中位数 R={r_rmed:.0f} F={f_rmed:.0f} M={m_rmed:.1f}，8 类已划分。")
    print(f"[RFM] 结论：重要价值客户 {int((rfm['segment']=='重要价值客户').sum())} 人，"
          f"贡献金额占比 {rfm.loc[rfm['segment']=='重要价值客户','M'].sum()/rfm['M'].sum()*100:.1f}%。")
    return rfm, seg_summary


# ---------- 2. 同期群留存 ----------
def cohort_model(full):
    """同期群留存：按首次购买月分群，计算后续每月留存率。"""
    df = full[full["order_status"].isin(["delivered", "shipped"])].copy()
    first = df.groupby("customer_unique_id")["order_purchase_timestamp"].min().dt.to_period("M")
    df["first_month"] = df["customer_unique_id"].map(first)
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
    df["cohort_index"] = (df["order_month"] - df["first_month"]).apply(lambda x: x.n)
    cohort = df.groupby(["first_month", "cohort_index"])["customer_unique_id"].nunique().reset_index()
    cohort = cohort.rename(columns={"customer_unique_id": "users"})
    base = cohort[cohort["cohort_index"] == 0][["first_month", "users"]].rename(columns={"users": "cohort_size"})
    cohort = cohort.merge(base, on="first_month")
    cohort["retention_rate"] = cohort["users"] / cohort["cohort_size"]
    # 透视矩阵
    matrix = cohort.pivot(index="first_month", columns="cohort_index", values="retention_rate")
    cohort.to_csv(TABLES / "cohort.csv", index=False)
    matrix.to_csv(TABLES / "cohort_matrix.csv")
    print(f"[同期群] {matrix.shape[0]} 个群，最大跨度 {matrix.shape[1]} 月。")
    if matrix.shape[1] >= 3:
        m3 = matrix[2].mean()
        print(f"[同期群] 结论：第 3 月平均留存率 {m3*100:.1f}%，可作为复购健康度基线。")
    return cohort, matrix


# ---------- 3. 帕累托 / ABC ----------
def pareto_abc_model(full):
    """按产品类别销售额降序，累计占比 ABC 分类（A:0-70% B:70-90% C:90-100%）。"""
    df = full[full["order_value"].notna() & (full["order_value"] > 0)].copy()
    cat = df.groupby("main_category")["order_value"].sum().reset_index()
    cat = cat.sort_values("order_value", ascending=False)
    cat["cum_share"] = cat["order_value"].cumsum() / cat["order_value"].sum()
    cat["ABC"] = np.where(cat["cum_share"] <= 0.70, "A",
                 np.where(cat["cum_share"] <= 0.90, "B", "C"))
    cat.to_csv(TABLES / "pareto_abc.csv", index=False)
    abc_summary = cat.groupby("ABC").agg(类别数=("main_category", "count"),
                                         销售额=("order_value", "sum"),
                                         占比=("order_value", lambda x: x.sum() / cat["order_value"].sum()))
    abc_summary.to_csv(TABLES / "abc_summary.csv")
    n_a = int((cat["ABC"] == "A").sum())
    share_a = cat.loc[cat["ABC"] == "A", "order_value"].sum() / cat["order_value"].sum()
    print(f"[帕累托/ABC] 共 {len(cat)} 类，A 类 {n_a} 类贡献 {share_a*100:.1f}% 销售额（20/80 验证）。")
    return cat


# ---------- 4. 环比/同比 + 移动平均 ----------
def trend_model(full):
    """月度销售额趋势：环比、年同比、3 月移动平均。"""
    df = full[full["order_value"].notna() & (full["order_value"] > 0)].copy()
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly = df.groupby("month").agg(订单数=("order_id", "nunique"),
                                      销售额=("order_value", "sum")).reset_index()
    monthly["month_dt"] = pd.to_datetime(monthly["month"])
    monthly = monthly.sort_values("month_dt")
    monthly["环比增长率"] = monthly["销售额"].pct_change()
    # 年同比：同月去年
    monthly["year"] = monthly["month_dt"].dt.year
    monthly["mon"] = monthly["month_dt"].dt.month
    yoy = monthly.set_index(["year", "mon"])["销售额"]
    monthly["同比增长率"] = monthly.apply(
        lambda r: (yoy.get((r["year"], r["mon"]), np.nan) / yoy.get((r["year"] - 1, r["mon"]), np.nan) - 1)
        if yoy.get((r["year"] - 1, r["mon"]), np.nan) > 0 else np.nan, axis=1)
    monthly["3月移动平均"] = monthly["销售额"].rolling(3, min_periods=1).mean()
    monthly.to_csv(TABLES / "monthly_trend.csv", index=False)
    print(f"[趋势] {len(monthly)} 月，最近月销售额 {monthly['销售额'].iloc[-1]:.0f}，"
          f"3 月均线 {monthly['3月移动平均'].iloc[-1]:.0f}。")
    return monthly


# ---------- 5. SARIMA 预测 ----------
def sarima_model(full):
    """SARIMA 月度销售额预测：点预测 + 95% 置信区间，末 6 月回测 MAPE/RMSE。"""
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    df = full[full["order_value"].notna() & (full["order_value"] > 0)].copy()
    s = df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))["order_value"].sum()
    s.index = s.index.to_timestamp()
    series = s.asfreq("MS").ffill()
    monthly_counts = df.groupby(df["order_purchase_timestamp"].dt.to_period("M")).size()
    monthly_counts.index = monthly_counts.index.to_timestamp()
    valid = monthly_counts[monthly_counts >= 50]
    start_m, end_m = valid.index.min(), valid.index.max()
    series = series[(series.index >= start_m) & (series.index <= end_m)].asfreq("MS").ffill()
    h = 6
    train, test = series.iloc[:-h], series.iloc[-h:]
    candidates = [((1, 1, 1), (1, 0, 1, 12)), ((1, 1, 1), (0, 0, 0, 0)), ((0, 1, 1), (0, 0, 0, 0))]
    fit_test, used = None, None
    for order, seas in candidates:
        try:
            m = SARIMAX(train, order=order, seasonal_order=seas,
                        enforce_stationarity=False, enforce_invertibility=False)
            fit_test = m.fit(disp=False, maxiter=200)
            used = (order, seas); break
        except Exception:
            continue
    if fit_test is None:
        print("[SARIMA] 全部候选阶数拟合失败，跳过。"); return None
    fc_test = fit_test.get_forecast(steps=h)
    pred_test = fc_test.predicted_mean
    mape = (abs((test - pred_test) / test)).mean() * 100
    smape = (2 * abs(test - pred_test) / (abs(test) + abs(pred_test))).mean() * 100
    if mape > 100:
        mape = smape
    rmse = (((test - pred_test) ** 2).mean()) ** 0.5
    # 全量拟合 + 未来 6 月预测
    fit_full = SARIMAX(series, order=used[0], seasonal_order=used[1],
                       enforce_stationarity=False, enforce_invertibility=False).fit(disp=False, maxiter=200)
    fc = fit_full.get_forecast(steps=h)
    pred = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)
    hist = pd.DataFrame({"month": series.index, "actual": series.values, "type": "历史"})
    fut = pd.DataFrame({"month": pred.index, "actual": np.nan,
                        "forecast": pred.values,
                        "lower": ci.iloc[:, 0].values, "upper": ci.iloc[:, 1].values, "type": "预测"})
    out = pd.concat([hist, fut], ignore_index=True)
    out.to_csv(TABLES / "sarima_forecast.csv", index=False)
    pd.DataFrame([{"MAPE": mape, "RMSE": rmse, "order": str(used[0]),
                   "seasonal_order": str(used[1]), "回测步数": h}]).to_csv(TABLES / "sarima_metrics.csv", index=False)
    print(f"[SARIMA] order={used[0]} seasonal={used[1]}，回测 MAPE={mape:.2f}% RMSE={rmse:.0f}。")
    print(f"[SARIMA] 未来 {h} 月预测：首月 {pred.iloc[0]:.0f}，末月 {pred.iloc[-1]:.0f} BRL。")
    return out


def main():
    print("=" * 60)
    print("03_analysis.py — 商业分析模型")
    print("=" * 60)
    full = load()
    print(f"载入宽表：{full.shape}")
    rfm, seg = rfm_model(full)
    cohort, matrix = cohort_model(full)
    pareto = pareto_abc_model(full)
    trend = trend_model(full)
    sarima = sarima_model(full)
    print("\n5 个模型全部完成，结果已写入 outputs/tables/。")
    return {"rfm": rfm, "cohort": cohort, "pareto": pareto, "trend": trend, "sarima": sarima}


if __name__ == "__main__":
    main()
    print("完成。")

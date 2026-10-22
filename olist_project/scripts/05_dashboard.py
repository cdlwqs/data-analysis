"""
05_dashboard.py — 交互式可视化大屏（Streamlit）+ 静态大屏截图
==============================================================
组件 ≥6 且联动：筛选器(州/品类/时间)、KPI 卡、趋势图、结构图、
散点(RFM)、明细表、同期群热力图。全 Python 实现，未使用 Power BI/Tableau。

交互运行：streamlit run scripts/05_dashboard.py
静态截图：python scripts/05_dashboard.py --snapshot  → outputs/figures/dashboard.png
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

for _fp in [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\msyh.ttc"]:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

C_BLUE, C_ORANGE, C_GREEN, C_RED = "#2E86AB", "#F24157", "#06D6A0", "#FFD23F"
C_PURPLE, C_CYAN, C_GOLD, C_DARK = "#9B5DE5", "#00BBF9", "#F15B29", "#3D405B"
PALETTE = [C_BLUE, C_ORANGE, C_GREEN, C_GOLD, C_PURPLE, C_CYAN, C_RED, C_DARK]


def load_full():
    return pd.read_csv(CLEAN / "order_full.csv", parse_dates=["order_purchase_timestamp"])


def filter_data(full, states, cats, daterange):
    df = full.copy()
    if states:
        df = df[df["customer_state"].isin(states)]
    if cats:
        df = df[df["main_category"].isin(cats)]
    if daterange:
        df = df[(df["order_purchase_timestamp"] >= daterange[0]) & (df["order_purchase_timestamp"] <= daterange[1])]
    return df


# ---------- 静态大屏截图 ----------
def generate_dashboard_png():
    """用 matplotlib GridSpec 组合 KPI + 6 子图，生成 dashboard.png。"""
    full = load_full()
    df = full[full["order_value"].notna()].copy()
    df["m"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    kpi_sales = df["order_value"].sum()
    kpi_orders = df["order_id"].nunique()
    kpi_review = df["review_score"].mean()
    kpi_customers = df["customer_unique_id"].nunique()

    fig = plt.figure(figsize=(16, 9), constrained_layout=True)
    gs = fig.add_gridspec(4, 4, hspace=0.35, wspace=0.25)

    # 标题
    fig.suptitle("Olist 巴西电商商业分析可视化大屏", fontsize=16, fontweight="bold", y=0.995)

    # KPI 卡（第 0 行）
    kpis = [("总销售额(BRL)", f"{kpi_sales/1e6:.2f}M", C_BLUE),
            ("订单数", f"{kpi_orders:,}", C_ORANGE),
            ("平均评价", f"{kpi_review:.2f}", C_GREEN),
            ("客户数", f"{kpi_customers:,}", C_RED)]
    for j, (title, val, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, j])
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color=color, alpha=0.15))
        ax.text(0.5, 0.62, val, ha="center", va="center", fontsize=18, fontweight="bold", color=color, transform=ax.transAxes)
        ax.text(0.5, 0.22, title, ha="center", va="center", fontsize=10, color="#555", transform=ax.transAxes)

    # 1. 月度趋势
    ax1 = fig.add_subplot(gs[1, :2])
    g = df.groupby("m")["order_value"].sum()
    ax1.bar(g.index, g.values, color=C_BLUE, width=0.6)
    ax1.set_title("月度销售额趋势", fontsize=10); ax1.tick_params(axis="x", rotation=90, labelsize=6)

    # 2. 支付方式
    ax2 = fig.add_subplot(gs[1, 2])
    p = full["payment_type"].value_counts()
    ax2.pie(p.values, labels=p.index, autopct="%1.0f%%", colors=[C_BLUE, C_ORANGE, C_GREEN, C_RED], textprops={"fontsize": 7})
    ax2.set_title("支付方式占比", fontsize=10)

    # 3. 订单状态
    ax3 = fig.add_subplot(gs[1, 3])
    s = full["order_status"].value_counts().head(4)
    ax3.barh(s.index, s.values, color=C_GREEN, height=0.6)
    ax3.set_title("订单状态", fontsize=10); ax3.tick_params(labelsize=7)

    # 4. RFM 气泡
    ax4 = fig.add_subplot(gs[2, :2])
    rfm = pd.read_csv(TABLES / "rfm.csv")
    for i, seg in enumerate(rfm["segment"].unique()):
        d = rfm[rfm["segment"] == seg]
        ax4.scatter(d["R"], d["F"], s=d["M"] / 8, alpha=0.5, color=[C_BLUE, C_ORANGE, C_GREEN, C_RED, "#FFC000", "#5B9BD5", "#7030A0", "#264478"][i % 8], label=seg, edgecolor="w", linewidth=0.2)
    ax4.set_title("RFM 八分类气泡散点图", fontsize=10); ax4.set_xlabel("R", fontsize=8); ax4.set_ylabel("F", fontsize=8)
    ax4.legend(fontsize=5, ncol=2, loc="upper right")

    # 5. Top 品类
    ax5 = fig.add_subplot(gs[2, 2:])
    top = df.groupby("main_category")["order_value"].sum().nlargest(10).sort_values()
    ax5.barh(top.index, top.values, color=C_ORANGE, height=0.6)
    ax5.set_title("Top10 品类销售额", fontsize=10); ax5.tick_params(labelsize=7)

    # 6. 同期群热力图
    ax6 = fig.add_subplot(gs[3, :])
    import seaborn as sns
    matrix = pd.read_csv(TABLES / "cohort_matrix.csv", index_col=0)
    sns.heatmap(matrix, annot=False, cmap="YlGnBu", ax=ax6, cbar=False)
    ax6.set_title("同期群留存热力图", fontsize=10); ax6.set_xlabel("距首购月数", fontsize=8); ax6.set_ylabel("首购月", fontsize=8)
    ax6.tick_params(labelsize=6)

    out = FIG / "dashboard.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"静态大屏截图已保存：{out}")
    return out


# ---------- Streamlit 交互大屏 ----------
def run_streamlit():
    import streamlit as st

    st.set_page_config(page_title="Olist 商业分析大屏", layout="wide", page_icon="📊")
    st.title("📊 Olist 巴西电商商业分析可视化大屏")
    st.caption("全 Python 实现 · Streamlit · 组件≥6 联动")

    full = load_full()

    # 筛选器（联动）
    with st.sidebar:
        st.header("🔍 筛选器")
        states = st.multiselect("选择州", sorted(full["customer_state"].dropna().unique()))
        cats = st.multiselect("选择品类", sorted(full["main_category"].dropna().unique()))
        daterange = st.date_input("时间范围", [full["order_purchase_timestamp"].min().date(),
                                                full["order_purchase_timestamp"].max().date()])

    df = filter_data(full, states, cats,
                     [pd.Timestamp(daterange[0]), pd.Timestamp(daterange[1])] if len(daterange) == 2 else None)
    dfv = df[df["order_value"].notna()].copy()

    # KPI 卡
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("总销售额 (BRL)", f"{dfv['order_value'].sum():,.0f}")
    c2.metric("订单数", f"{dfv['order_id'].nunique():,}")
    c3.metric("平均评价", f"{dfv['review_score'].mean():.2f}" if dfv["review_score"].notna().any() else "N/A")
    c4.metric("客户数", f"{dfv['customer_unique_id'].nunique():,}")

    # 趋势 + 结构
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("月度销售额趋势")
        dfv["m"] = dfv["order_purchase_timestamp"].dt.to_period("M").astype(str)
        g = dfv.groupby("m")["order_value"].sum()
        st.bar_chart(g)
    with col2:
        st.subheader("支付方式占比")
        p = df["payment_type"].value_counts()
        st.bar_chart(p)

    # 散点 + 明细表
    col3, col4 = st.columns([3, 2])
    with col3:
        st.subheader("RFM 八分类气泡散点图")
        rfm = pd.read_csv(TABLES / "rfm.csv")
        st.scatter_chart(rfm, x="R", y="F", size="M", color="segment")
    with col4:
        st.subheader("Top10 订单明细")
        top = dfv.nlargest(10, "order_value")[["order_id", "customer_state", "main_category", "order_value", "review_score"]]
        st.dataframe(top, use_container_width=True)

    # 同期群热力图
    st.subheader("同期群留存热力图")
    matrix = pd.read_csv(TABLES / "cohort_matrix.csv", index_col=0)
    st.dataframe(matrix.style.background_gradient(cmap="YlGnBu", axis=None), use_container_width=True)


def main():
    if "--snapshot" in sys.argv:
        generate_dashboard_png()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()

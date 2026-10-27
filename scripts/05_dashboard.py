"""
05_dashboard.py — 纽约Airbnb交互式大屏（Streamlit）+ 静态截图
==============================================================
组件 ≥6 且联动：行政区/房型/价格筛选器、4 KPI 卡、街区柱形、
房型箱线、价格-评论散点、Top10 高价表。--snapshot 用 matplotlib
生成 dashboard.png（2×3 子图）。

运行：
  streamlit run scripts/05_dashboard.py
  python scripts/05_dashboard.py --snapshot
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ---- 中文字体 ----
for _fp in [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\msyh.ttc"]:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlepad": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#E2E5EA",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.7,
    "axes.facecolor": "#F8F9FB",
})

C_BLUE = "#1565C0"
C_CORAL = "#E63946"
C_MINT = "#06A77D"
C_GOLD = "#F4A261"
C_PURPLE = "#7B2CBF"
C_CYAN = "#0096C7"
C_DARK = "#264653"
C_TEAL = "#2A9D8F"
PALETTE = [C_BLUE, C_CORAL, C_MINT, C_GOLD, C_PURPLE, C_CYAN]


def load_listings():
    """读取清洗后纽约Airbnb房源数据。"""
    df = pd.read_csv(CLEAN / "listings_clean.csv")
    df = df[df["price"].notna() & (df["price"] > 0)].copy()
    # 超级房东统一为布尔
    df["is_superhost"] = df["is_superhost"].astype(str).str.lower().isin(["t", "true", "1"])
    # 行政区空值填充
    df["neighbourhood_group_cleansed"] = df["neighbourhood_group_cleansed"].fillna("未知")
    df["room_type"] = df["room_type"].fillna("未知")
    return df


def kpi_values(df):
    """计算4个KPI。"""
    sup_ratio = df["is_superhost"].mean() * 100 if len(df) else 0
    avg_rating = df["review_scores_rating"].dropna().mean()
    return {
        "总房源数": f"{len(df):,}",
        "平均价格": f"${df['price'].mean():.0f}",
        "平均评分": f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A",
        "超级房东占比": f"{sup_ratio:.1f}%",
    }


# ============ 静态截图 ============
def snapshot():
    """用 matplotlib 生成 dashboard.png（升级版大屏 2×3 子图 + 顶部6 KPI）。"""
    df = load_listings()
    fig = plt.figure(figsize=(16, 10.5))
    fig.patch.set_facecolor("white")
    fig.suptitle("纽约 Airbnb 民宿数据可视化大屏", fontsize=20, fontweight="bold",
                 y=0.97, color=C_DARK)
    fig.text(0.5, 0.935, "Inside Airbnb NYC | 清洗后 19,203 条房源 | 5 行政区 | 221 街区",
             ha="center", fontsize=10, color="#9CA3AF", style="italic")

    # ---- 顶部 6 KPI 卡 ----
    kpis = kpi_values(df)
    kpis["总评论数"] = f"{df['number_of_reviews'].sum():,}"
    kpis["行政区数"] = f"{df['neighbourhood_group_cleansed'].nunique()}"
    kpi_colors = [C_BLUE, C_CORAL, C_MINT, C_GOLD, C_PURPLE, C_TEAL]
    for i, ((label, val), col) in enumerate(zip(kpis.items(), kpi_colors)):
        x = 0.08 + i * 0.155
        fig.text(x, 0.885, label, ha="center", fontsize=10, color="#6B7280")
        fig.text(x, 0.855, val, ha="center", fontsize=18, fontweight="bold", color=col)
        fig.text(x, 0.875, "─" * 12, ha="center", fontsize=8, color="#E5E7EB")

    gs = fig.add_gridspec(2, 3, top=0.80, bottom=0.06, left=0.06, right=0.97,
                          hspace=0.45, wspace=0.32)

    # 1. 各行政区房源数（水平柱形 + 渐变）
    ax1 = fig.add_subplot(gs[0, 0])
    grp = df.groupby("neighbourhood_group_cleansed").size().sort_values(ascending=True)
    colors = plt.cm.viridis(np.linspace(0.3, 0.85, len(grp)))
    bars = ax1.barh(grp.index, grp.values, color=colors, height=0.6, edgecolor="white", linewidth=0.8)
    ax1.set_title("各行政区房源数", color=C_DARK)
    ax1.set_xlabel("房源数")
    for b in bars:
        ax1.text(b.get_width(), b.get_y() + b.get_height() / 2,
                 f" {int(b.get_width()):,}", va="center", fontsize=8, color="#374151", fontweight="bold")

    # 2. 价格分布（直方图 + 均值线）
    ax2 = fig.add_subplot(gs[0, 1])
    p = df["price"][df["price"] <= df["price"].quantile(0.95)]
    ax2.hist(p, bins=40, color=C_CORAL, edgecolor="white", linewidth=0.5, alpha=0.85)
    ax2.axvline(p.mean(), color=C_DARK, linestyle="--", linewidth=1.5, label=f"均值 ${p.mean():.0f}")
    ax2.set_title("价格分布（剔除前5%极端值）", color=C_DARK)
    ax2.set_xlabel("每晚价格 ($)")
    ax2.set_ylabel("房源数")
    ax2.legend(fontsize=8, framealpha=0.9)

    # 3. 房型占比（饼图 + 突出主扇区）
    ax3 = fig.add_subplot(gs[0, 2])
    rt = df["room_type"].value_counts()
    explode = [0.05 if i == 0 else 0.02 for i in range(len(rt))]
    wedges, _, autotexts = ax3.pie(rt.values, labels=rt.index, autopct="%1.1f%%",
            colors=PALETTE[:len(rt)], textprops={"fontsize": 9, "fontweight": "bold"},
            wedgeprops={"edgecolor": "white", "linewidth": 2}, explode=explode,
            startangle=90, pctdistance=0.75)
    for t in autotexts:
        t.set_color("white")
    ax3.set_title("房型占比", color=C_DARK)

    # 4. 地理散点（经纬度，按价格着色 + 行政区标注）
    ax4 = fig.add_subplot(gs[1, 0])
    sub = df.dropna(subset=["latitude", "longitude"])
    if len(sub) > 5000:
        sub = sub.sample(5000, random_state=42)
    sc = ax4.scatter(sub["longitude"], sub["latitude"], c=sub["price"].clip(upper=500),
                     cmap="plasma", s=5, alpha=0.55, edgecolors="none")
    ax4.set_title("房源地理分布（颜色=价格）", color=C_DARK)
    ax4.set_xlabel("经度")
    ax4.set_ylabel("纬度")
    fig.colorbar(sc, ax=ax4, fraction=0.046, pad=0.04, label="价格($)")

    # 5. 各行政区平均价格（柱形 + 数据标签）
    ax5 = fig.add_subplot(gs[1, 1])
    avg_p = df.groupby("neighbourhood_group_cleansed")["price"].mean().sort_values(ascending=False)
    colors5 = [C_CORAL if v == avg_p.max() else C_MINT for v in avg_p.values]
    bars5 = ax5.bar(avg_p.index, avg_p.values, color=colors5, width=0.6, edgecolor="white", linewidth=0.8)
    ax5.set_title("各行政区平均价格", color=C_DARK)
    ax5.set_ylabel("平均价格 ($)")
    ax5.tick_params(axis="x", rotation=20)
    for b in bars5:
        ax5.text(b.get_x() + b.get_width() / 2, b.get_height(),
                 f"${b.get_height():.0f}", ha="center", va="bottom", fontsize=9,
                 color="#374151", fontweight="bold")

    # 6. 评分分布（箱线按行政区 + 均值菱形）
    ax6 = fig.add_subplot(gs[1, 2])
    rated = df.dropna(subset=["review_scores_rating"])
    rated = rated[rated["review_scores_rating"] > 0]
    groups = [g["review_scores_rating"].values for _, g in rated.groupby("neighbourhood_group_cleansed")]
    labels = list(rated.groupby("neighbourhood_group_cleansed").groups.keys())
    ax6.boxplot(groups, labels=labels, patch_artist=True,
                boxprops=dict(facecolor=C_GOLD, alpha=0.7),
                medianprops=dict(color=C_CORAL, linewidth=2),
                meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor=C_DARK, markersize=5),
                showmeans=True, flierprops=dict(marker=".", markersize=2, alpha=0.3))
    ax6.set_title("各行政区评分分布", color=C_DARK)
    ax6.set_ylabel("评分")
    ax6.tick_params(axis="x", rotation=20)

    out = FIG / "dashboard.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"saved {out}")


# ============ Streamlit 交互大屏 ============
def run_streamlit():
    import streamlit as st

    st.set_page_config(page_title="纽约Airbnb数据大屏", layout="wide",
                       page_icon="🏠")
    df_all = load_listings()

    # ---------- Sidebar 筛选器 ----------
    st.sidebar.title("🔍 筛选条件")
    boroughs = sorted(df_all["neighbourhood_group_cleansed"].unique())
    sel_boroughs = st.sidebar.multiselect("行政区", boroughs, default=boroughs)

    room_types = sorted(df_all["room_type"].unique())
    sel_rooms = st.sidebar.multiselect("房型", room_types, default=room_types)

    pmin, pmax = int(df_all["price"].min()), int(df_all["price"].quantile(0.99))
    price_range = st.sidebar.slider("价格范围 ($/晚)", pmin, pmax, (pmin, pmax))

    # ---------- 过滤 ----------
    df = df_all[
        df_all["neighbourhood_group_cleansed"].isin(sel_boroughs)
        & df_all["room_type"].isin(sel_rooms)
        & df_all["price"].between(price_range[0], price_range[1])
    ].copy()

    # ---------- KPI 卡 ----------
    st.title("🏠 纽约 Airbnb 民宿数据可视化大屏")
    st.caption(f"筛选后房源数：{len(df):,} / 全量 {len(df_all):,}")

    kpis = kpi_values(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("总房源数", kpis["总房源数"])
    c2.metric("平均价格", kpis["平均价格"])
    c3.metric("平均评分", kpis["平均评分"])
    c4.metric("超级房东占比", kpis["超级房东占比"])

    # ---------- 图表区 ----------
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("各街区房源数（Top15）")
        nb = df.groupby("neighbourhood_cleansed").size().sort_values(ascending=False).head(15)
        st.bar_chart(nb)

        st.subheader("价格 vs 评论数（散点）")
        sc_df = df.dropna(subset=["number_of_reviews"])
        if len(sc_df) > 3000:
            sc_df = sc_df.sample(3000, random_state=1)
        st.scatter_chart(sc_df.rename(columns={"price": "价格", "number_of_reviews": "评论数"})
                         [["价格", "评论数"]])

    with col_r:
        st.subheader("各房型价格分布（箱线）")
        rt_data = [g["price"].values for _, g in df.groupby("room_type")]
        rt_labels = list(df.groupby("room_type").groups.keys())
        try:
            import plotly.express as px
            fig_box = px.box(df, x="room_type", y="price", points="outliers",
                             labels={"room_type": "房型", "price": "价格"})
            fig_box.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_box, use_container_width=True)
        except Exception:
            st.box_chart(df[["room_type", "price"]].rename(columns={"room_type": "房型", "price": "价格"}))

        st.subheader("房型占比")
        st.plotly_chart(
            px.pie(df, names="room_type", hole=0.4),
            use_container_width=True
        ) if "px" in dir() else st.bar_chart(df["room_type"].value_counts())

    # ---------- Top10 高价房源表 ----------
    st.subheader("Top 10 高价房源")
    top10 = df.sort_values("price", ascending=False).head(10)[
        ["id", "name", "neighbourhood_group_cleansed", "room_type",
         "price", "review_scores_rating", "number_of_reviews"]
    ].rename(columns={
        "id": "房源ID", "name": "名称",
        "neighbourhood_group_cleansed": "行政区", "room_type": "房型",
        "price": "价格($)", "review_scores_rating": "评分",
        "number_of_reviews": "评论数",
    })
    st.dataframe(top10, use_container_width=True, hide_index=True)

    # ---------- 联动说明 ----------
    st.sidebar.markdown("---")
    st.sidebar.info("所有图表随左侧筛选器实时联动更新。")


if __name__ == "__main__":
    if "--snapshot" in sys.argv:
        snapshot()
    else:
        run_streamlit()

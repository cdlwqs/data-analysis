"""
04_visuals.py — 数据可视化（全 Python 实现）
============================================
对照《Excel数据可视化——从图表到数据大屏》30 种模板，复现 12 种模板图；
7 张业务模型图与第 4 章 5 个模型一一对应。共 19 张，分辨率 200dpi。
统一命名 fig01_*.png … fig19_*.png，输出到 outputs/figures/。

运行：python scripts/04_visuals.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ---- 全局样式：现代精致风格 ----
from matplotlib import font_manager
for _fp in [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\msyh.ttc"]:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)

plt.rcParams.update({
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "DejaVu Sans"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "figure.dpi": 130,
    "savefig.dpi": 200,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlepad": 12,
    "axes.labelsize": 10,
    "axes.labelweight": "medium",
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.frameon": True,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "#CCCCCC",
    "figure.facecolor": "white",
    "axes.facecolor": "#FAFAFA",
    "axes.edgecolor": "#BBBBBB",
    "axes.linewidth": 0.7,
    "axes.grid": True,
    "grid.color": "#E0E0E0",
    "grid.linestyle": "-",
    "grid.linewidth": 0.5,
    "grid.alpha": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
})

# 精致配色方案
C_BLUE = "#2E86AB"
C_CORAL = "#F24157"
C_MINT = "#06D6A0"
C_GOLD = "#FFD23F"
C_PURPLE = "#9B5DE5"
C_CYAN = "#00BBF9"
C_ORANGE = "#F15B29"
C_DARK = "#3D405B"
PALETTE = [C_BLUE, C_CORAL, C_MINT, C_GOLD, C_PURPLE, C_CYAN, C_ORANGE, C_DARK]
PALETTE_SOFT = ["#5FA8C9", "#F58A97", "#4FE0B8", "#FFE57F", "#B88DEB", "#4FD3FA", "#F89B6E", "#7A7D94"]


def save(fig, name):
    path = FIG / name
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved {name}")


def load_full():
    return pd.read_csv(CLEAN / "order_full.csv", parse_dates=["order_purchase_timestamp"])


def style_ax(ax):
    """统一美化坐标轴。"""
    ax.spines["left"].set_color("#888888")
    ax.spines["bottom"].set_color("#888888")
    ax.tick_params(colors="#555555")


def add_value_labels(ax, bars, fmt="{:.0f}", offset=0, fontsize=7, color="#444"):
    """为柱形添加数值标签。"""
    for b in bars:
        h = b.get_height()
        if h > 0:
            ax.text(b.get_x() + b.get_width() / 2, h + offset, fmt.format(h),
                    ha="center", va="bottom", fontsize=fontsize, color=color, fontweight="medium")


# ============ 模板复现类 12 种 ============

def fig01_monthly_orders_bar(full):
    """模板1·柱形图：月度订单数。"""
    m = full.groupby(full["order_purchase_timestamp"].dt.to_period("M").astype(str))["order_id"].nunique()
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(m)))
    bars = ax.bar(m.index, m.values, color=colors, width=0.65, edgecolor="white", linewidth=0.5)
    ax.set_title("月度订单数分布", color=C_DARK)
    ax.set_ylabel("订单数", color="#555")
    ax.tick_params(axis="x", rotation=90)
    ax.set_ylim(0, max(m.values) * 1.12)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig01_月度订单数_柱形图.png")


def fig02_sales_line(full):
    """模板2·折线图：月度销售额趋势。"""
    df = full[full["order_value"].notna()].copy()
    df["m"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    s = df.groupby("m")["order_value"].sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(s.index, s.values, alpha=0.12, color=C_BLUE)
    ax.plot(s.index, s.values, color=C_BLUE, marker="o", markersize=4, linewidth=2.2,
            markerfacecolor="white", markeredgecolor=C_BLUE, markeredgewidth=1.5)
    ax.set_title("月度销售额趋势", color=C_DARK)
    ax.set_ylabel("销售额 (BRL)", color="#555")
    ax.tick_params(axis="x", rotation=90)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig02_月度销售额_折线图.png")


def fig03_payment_pie(full):
    """模板3·饼图：支付方式占比。"""
    p = full["payment_type"].value_counts()
    fig, ax = plt.subplots(figsize=(7.5, 6))
    explode = [0.06 if i == 0 else 0.02 for i in range(len(p))]
    wedges, texts, autotexts = ax.pie(
        p.values, labels=None, autopct="%1.1f%%", colors=PALETTE, startangle=90,
        explode=explode, textprops={"fontsize": 11, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2.5}, pctdistance=0.72)
    for t in autotexts:
        t.set_fontsize(11); t.set_fontweight("bold"); t.set_color("white")
    labels = [f"{idx}  ({val:,})" for idx, val in p.items()]
    ax.legend(wedges, labels, title="支付方式", loc="center left",
              bbox_to_anchor=(1.0, 0.5), fontsize=10, title_fontsize=11, framealpha=0.9)
    ax.set_title("支付方式占比", color=C_DARK, fontsize=15)
    plt.tight_layout(); save(fig, "fig03_支付方式占比_饼图.png")


def fig04_dual_axis(full):
    """模板4·双轴组合图：销售额柱 + 订单数折线。"""
    df = full[full["order_value"].notna()].copy()
    df["m"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    g = df.groupby("m").agg(销售额=("order_value", "sum"), 订单数=("order_id", "nunique"))
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(g.index, g["销售额"], color=C_BLUE, width=0.55, alpha=0.75, label="销售额", edgecolor="white", linewidth=0.5)
    ax1.set_ylabel("销售额 (BRL)", color=C_BLUE)
    ax1.tick_params(axis="x", rotation=90)
    ax1.tick_params(axis="y", colors=C_BLUE)
    ax2 = ax1.twinx()
    ax2.plot(g.index, g["订单数"], color=C_CORAL, marker="o", markersize=4, linewidth=2.2,
             markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=1.5, label="订单数")
    ax2.set_ylabel("订单数", color=C_CORAL)
    ax2.tick_params(axis="y", colors=C_CORAL)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(C_CORAL)
    ax1.set_title("销售额与订单数双轴组合图", color=C_DARK)
    fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.93), fontsize=9, framealpha=0.9)
    style_ax(ax1)
    plt.tight_layout(); save(fig, "fig04_销售额订单数_双轴组合图.png")


def fig05_stacked_bar_state(full):
    """模板5·堆积柱形图：Top8 州按年堆积销售额。"""
    df = full[full["order_value"].notna()].copy()
    top_states = df.groupby("customer_state")["order_value"].sum().nlargest(8).index
    df = df[df["customer_state"].isin(top_states)]
    df["year"] = df["order_purchase_timestamp"].dt.year
    pivot = df.pivot_table(index="customer_state", columns="year", values="order_value", aggfunc="sum").fillna(0)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(9, 5))
    pivot.plot.bar(stacked=True, ax=ax, color=[C_BLUE, C_CORAL, C_MINT], width=0.6, edgecolor="white", linewidth=0.5)
    ax.set_title("Top8 州年度销售额（堆积柱形图）", color=C_DARK)
    ax.set_ylabel("销售额 (BRL)", color="#555")
    ax.set_xlabel("州", color="#555")
    ax.legend(title="年份", fontsize=9, framealpha=0.9)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig05_州年度销售额_堆积柱形图.png")


def fig06_price_review_scatter(full):
    """模板6·散点图：价格 vs 评价分。"""
    df = full[full["order_value"].notna() & full["review_score"].notna()].copy()
    df = df[df["order_value"] < 2000]
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(df["order_value"], df["review_score"], s=10, alpha=0.25,
                    c=df["review_score"], cmap="RdYlGn", edgecolors="none")
    ax.set_title("订单金额与评价分（散点图）", color=C_DARK)
    ax.set_xlabel("订单金额 (BRL)", color="#555")
    ax.set_ylabel("评价分", color="#555")
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("评价分", fontsize=9)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig06_金额评价_散点图.png")


def fig07_boxplot_state(full):
    """模板7·箱线图：Top10 州订单金额分布。"""
    df = full[full["order_value"].notna() & (full["order_value"] < 1000)].copy()
    top = df.groupby("customer_state")["order_value"].sum().nlargest(10).index
    df = df[df["customer_state"].isin(top)]
    order = df.groupby("customer_state")["order_value"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df, x="customer_state", y="order_value", ax=ax, order=order,
                palette=PALETTE_SOFT, fliersize=1, linewidth=1.2,
                boxprops=dict(alpha=0.8), medianprops=dict(color=C_DARK, linewidth=1.5))
    ax.set_title("Top10 州订单金额分布（箱线图）", color=C_DARK)
    ax.set_xlabel("州", color="#555")
    ax.set_ylabel("订单金额 (BRL)", color="#555")
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig07_州金额分布_箱线图.png")


def fig08_heatmap_dow_hour(full):
    """模板8·热力图：购买星期 × 小时。"""
    df = full.copy()
    df["dow"] = df["order_purchase_timestamp"].dt.dayofweek
    df["hour"] = df["order_purchase_timestamp"].dt.hour
    pivot = df.pivot_table(index="dow", columns="hour", values="order_id", aggfunc="count").fillna(0)
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(pivot, cmap="YlOrRd", annot=False, ax=ax, cbar_kws={"label": "订单数"},
                linewidths=0.3, linecolor="white")
    ax.set_title("购买时段热力图（星期 × 小时）", color=C_DARK)
    ax.set_xlabel("小时", color="#555")
    ax.set_ylabel("星期", color="#555")
    ax.set_yticklabels(["周一", "周二", "周三", "周四", "周五", "周六", "周日"], rotation=0)
    plt.tight_layout(); save(fig, "fig08_购买时段_热力图.png")


def fig09_top_category_hbar(full):
    """模板9·水平条形图：Top10 品类销售额。"""
    df = full[full["order_value"].notna()].copy()
    g = df.groupby("main_category")["order_value"].sum().nlargest(10).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.viridis(np.linspace(0.3, 0.85, len(g)))
    bars = ax.barh(g.index, g.values, color=colors, height=0.6, edgecolor="white", linewidth=0.5)
    for b, v in zip(bars, g.values):
        ax.text(v + g.max() * 0.01, b.get_y() + b.get_height() / 2, f"{v/1e6:.2f}M",
                fontsize=8, va="center", color="#444", fontweight="medium")
    ax.set_title("Top10 品类销售额（水平条形图）", color=C_DARK)
    ax.set_xlabel("销售额 (BRL)", color="#555")
    ax.set_xlim(0, g.max() * 1.12)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig09_品类销售额_水平条形图.png")


def fig10_status_donut(full):
    """模板10·圆环图：订单状态占比。"""
    s = full["order_status"].value_counts()
    if len(s) > 4:
        rest = s.iloc[3:].sum()
        s = s.iloc[:3]
        s["其他"] = rest
    fig, ax = plt.subplots(figsize=(7.5, 6))
    colors_donut = PALETTE[:len(s)]
    wedges, _, autotexts = ax.pie(
        s.values, labels=None, autopct="%1.1f%%", colors=colors_donut,
        startangle=90, pctdistance=0.82, textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 3, "width": 0.45})
    for t in autotexts:
        t.set_fontsize(10); t.set_fontweight("bold"); t.set_color("white")
    ax.add_artist(plt.Circle((0, 0), 0.52, fc="white", ec="#E0E0E0", linewidth=1.5))
    ax.text(0, 0.08, f"{s.sum():,}", ha="center", va="center", fontsize=16,
            fontweight="bold", color=C_DARK)
    ax.text(0, -0.08, "总订单数", ha="center", va="center", fontsize=10, color="#888")
    labels = [f"{idx}  ({val:,})" for idx, val in s.items()]
    ax.legend(wedges, labels, title="订单状态", loc="center left",
              bbox_to_anchor=(1.0, 0.5), fontsize=10, title_fontsize=11, framealpha=0.9)
    ax.set_title("订单状态占比（圆环图）", color=C_DARK, fontsize=15)
    plt.tight_layout(); save(fig, "fig10_订单状态_圆环图.png")


def fig11_radar_rfm():
    """模板11·雷达图：RFM 四分群特征。"""
    rfm = pd.read_csv(TABLES / "rfm.csv")
    top4 = rfm.groupby("segment").agg(R=("R", "mean"), F=("F", "mean"), M=("M", "mean")).reset_index()
    top4 = top4[top4["segment"].str.startswith("重要")].head(4)
    norm = top4[["R", "F", "M"]].copy()
    for c in ["R", "F", "M"]:
        norm[c] = norm[c] / norm[c].max()
    labels = ["R (近因)", "F (频次)", "M (金额)"]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_facecolor("#FAFAFA")
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8, color="#888")
    ax.grid(color="#CCCCCC", linewidth=0.6, alpha=0.7)
    ax.spines["polar"].set_color("#BBBBBB")
    for i, (_, row) in enumerate(norm.iterrows()):
        vals = row.tolist() + [row.tolist()[0]]
        ax.plot(angles, vals, linewidth=2.5, label=top4.iloc[i]["segment"],
                color=PALETTE[i], marker="o", markersize=7,
                markerfacecolor="white", markeredgecolor=PALETTE[i], markeredgewidth=2)
        ax.fill(angles, vals, alpha=0.18, color=PALETTE[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, fontweight="bold", color=C_DARK)
    ax.set_title("重要客群 RFM 特征（雷达图）", pad=25, color=C_DARK, fontsize=15)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=9,
              framealpha=0.9, edgecolor="#CCCCCC", markerscale=1.2)
    plt.tight_layout(); save(fig, "fig11_RFM特征_雷达图.png")


def fig12_lollipop_new_customers(full):
    """模板12·棒棒糖图：各月新增客户数。"""
    df = full.copy()
    first = df.groupby("customer_unique_id")["order_purchase_timestamp"].min()
    first_m = first.dt.to_period("M").astype(str).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.vlines(first_m.index, 0, first_m.values, color=C_BLUE, linewidth=2, alpha=0.6)
    ax.scatter(first_m.index, first_m.values, color=C_CORAL, s=40, zorder=3, edgecolor="white", linewidth=0.8)
    ax.set_title("各月新增客户数（棒棒糖图）", color=C_DARK)
    ax.set_ylabel("新增客户数", color="#555")
    ax.tick_params(axis="x", rotation=90)
    ax.set_ylim(0, max(first_m.values) * 1.1)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig12_新增客户_棒棒糖图.png")


# ============ 业务模型类 7 张 ============

def fig13_rfm_bubble():
    """业务图1·RFM 八分类气泡散点图。"""
    rfm = pd.read_csv(TABLES / "rfm.csv")
    fig, ax = plt.subplots(figsize=(9, 6))
    segs = rfm["segment"].unique()
    for i, seg in enumerate(segs):
        d = rfm[rfm["segment"] == seg]
        ax.scatter(d["R"], d["F"], s=d["M"] / 8, alpha=0.5,
                   color=PALETTE[i % len(PALETTE)], label=seg, edgecolor="white", linewidth=0.5)
    ax.set_title("RFM 八分类气泡散点图（R×F，气泡=金额）", color=C_DARK)
    ax.set_xlabel("R 最近购买距今天数", color="#555")
    ax.set_ylabel("F 购买频次", color="#555")
    ax.legend(loc="upper right", fontsize=7, ncol=2, framealpha=0.85, markerscale=0.8)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig13_RFM八分类_气泡散点图.png")


def fig14_rfm_segment_value():
    """业务图2·RFM 分群金额占比条形图。"""
    seg = pd.read_csv(TABLES / "rfm_segment_summary.csv")
    seg = seg.sort_values("累计金额", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.viridis(np.linspace(0.2, 0.85, len(seg)))
    bars = ax.barh(seg["segment"], seg["累计金额"], color=colors, height=0.6, edgecolor="white", linewidth=0.5)
    total = seg["累计金额"].sum()
    for b, v in zip(bars, seg["累计金额"]):
        ax.text(v + total * 0.005, b.get_y() + b.get_height() / 2, f"{v/total*100:.1f}%",
                fontsize=8, va="center", color="#444", fontweight="medium")
    ax.set_title("RFM 分群金额贡献占比", color=C_DARK)
    ax.set_xlabel("累计金额 (BRL)", color="#555")
    ax.set_xlim(0, seg["累计金额"].max() * 1.15)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig14_RFM分群金额占比.png")


def fig15_cohort_heatmap():
    """业务图3·同期群留存热力图。"""
    matrix = pd.read_csv(TABLES / "cohort_matrix.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(matrix, annot=True, fmt=".1%", cmap="YlGnBu", ax=ax,
                cbar_kws={"label": "留存率"}, annot_kws={"fontsize": 6},
                vmin=0, vmax=1, linewidths=0.3, linecolor="white")
    ax.set_title("同期群留存热力图", color=C_DARK)
    ax.set_xlabel("距首购月数", color="#555")
    ax.set_ylabel("首次购买月", color="#555")
    plt.tight_layout(); save(fig, "fig15_同期群留存_热力图.png")


def fig16_pareto():
    """业务图4·帕累托图（双轴：柱+累计占比线，ABC 着色）。"""
    p = pd.read_csv(TABLES / "pareto_abc.csv")
    p = p.sort_values("order_value", ascending=False).head(20)
    fig, ax1 = plt.subplots(figsize=(11, 5))
    colors = {"A": C_BLUE, "B": C_GOLD, "C": C_CORAL}
    bars = ax1.bar(p["main_category"], p["order_value"], color=[colors[c] for c in p["ABC"]],
                   width=0.6, edgecolor="white", linewidth=0.5)
    ax1.set_ylabel("销售额 (BRL)", color="#555")
    ax1.tick_params(axis="x", rotation=90)
    ax2 = ax1.twinx()
    ax2.plot(p["main_category"], p["cum_share"] * 100, color=C_DARK, marker="o", markersize=4,
             linewidth=2, markerfacecolor="white", markeredgecolor=C_DARK, markeredgewidth=1.5)
    ax2.set_ylabel("累计占比 (%)", color="#555")
    ax2.set_ylim(0, 108)
    ax2.axhline(70, color=C_CORAL, linestyle="--", linewidth=1, alpha=0.7)
    ax2.axhline(90, color=C_DARK, linestyle="--", linewidth=1, alpha=0.5)
    ax2.text(len(p) - 0.5, 71, "70%", fontsize=8, color=C_CORAL, ha="right")
    ax2.text(len(p) - 0.5, 91, "90%", fontsize=8, color=C_DARK, ha="right")
    ax2.spines["right"].set_visible(True)
    ax1.set_title("帕累托图（Top20 品类，ABC 分类）", color=C_DARK)
    legend = [Patch(facecolor=colors[k], label=f"{k}类") for k in ["A", "B", "C"]]
    ax1.legend(handles=legend, title="ABC", loc="upper right", framealpha=0.9)
    style_ax(ax1)
    plt.tight_layout(); save(fig, "fig16_帕累托图_ABC.png")


def fig17_abc_pie():
    """业务图5·ABC 类别构成饼图。"""
    p = pd.read_csv(TABLES / "pareto_abc.csv")
    g = p.groupby("ABC").agg(类别数=("main_category", "count"), 销售额=("order_value", "sum"))
    fig, ax = plt.subplots(figsize=(7.5, 6))
    explode = [0.06, 0.03, 0.01]
    colors_abc = [C_BLUE, C_GOLD, C_CORAL]
    wedges, texts, autotexts = ax.pie(
        g["销售额"], labels=None, autopct="%1.1f%%", colors=colors_abc, startangle=90,
        explode=explode, textprops={"fontsize": 11, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2.5}, pctdistance=0.72)
    for t in autotexts:
        t.set_fontsize(12); t.set_fontweight("bold"); t.set_color("white")
    labels = [f"{i}类  ({n} 个类目, {v/1e6:.2f}M BRL)" for i, n, v in zip(g.index, g["类别数"], g["销售额"])]
    ax.legend(wedges, labels, title="ABC 分类", loc="center left",
              bbox_to_anchor=(1.0, 0.5), fontsize=10, title_fontsize=11, framealpha=0.9)
    ax.set_title("ABC 分类销售额构成", color=C_DARK, fontsize=15)
    plt.tight_layout(); save(fig, "fig17_ABC构成_饼图.png")


def fig18_trend_ma_yoy():
    """业务图6·月度趋势 + 移动平均 + 同比柱线组合图。"""
    t = pd.read_csv(TABLES / "monthly_trend.csv", parse_dates=["month_dt"])
    t = t.sort_values("month_dt")
    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.bar(t["month"], t["销售额"], color=C_BLUE, width=0.55, alpha=0.6, label="月销售额", edgecolor="white", linewidth=0.3)
    ax1.plot(t["month"], t["3月移动平均"], color=C_CORAL, linewidth=2.2, marker="o", markersize=4,
             markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=1.5, label="3月移动平均")
    ax1.set_ylabel("销售额 (BRL)", color="#555")
    ax1.tick_params(axis="x", rotation=90)
    ax2 = ax1.twinx()
    ax2.bar(t["month"], t["同比增长率"] * 100, color=C_MINT, width=0.3, alpha=0.5, label="同比增长率")
    ax2.set_ylabel("同比增长率 (%)", color="#555")
    ax2.axhline(0, color="#888888", linewidth=0.8)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color("#BBBBBB")
    ax1.set_title("月度销售额趋势、移动平均与同比", color=C_DARK)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8, framealpha=0.9)
    style_ax(ax1)
    plt.tight_layout(); save(fig, "fig18_趋势移动平均同比.png")


def fig19_sarima_forecast():
    """业务图7·SARIMA 预测带 95% 置信区间。"""
    df = pd.read_csv(TABLES / "sarima_forecast.csv", parse_dates=["month"])
    metrics = pd.read_csv(TABLES / "sarima_metrics.csv")
    fig, ax = plt.subplots(figsize=(11, 5))
    hist = df[df["type"] == "历史"]
    fut = df[df["type"] == "预测"]
    ax.fill_between(fut["month"], fut["lower"], fut["upper"], color=C_CORAL, alpha=0.15, label="95% 置信区间")
    ax.plot(hist["month"], hist["actual"], color=C_BLUE, linewidth=2, label="历史销售额")
    ax.plot(fut["month"], fut["forecast"], color=C_CORAL, linewidth=2, marker="o", markersize=5,
            markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=1.5, label="预测")
    ax.axvline(hist["month"].iloc[-1], color="#888888", linestyle="--", linewidth=1, alpha=0.5)
    ax.text(hist["month"].iloc[-1], ax.get_ylim()[1] * 0.95, " 预测起点", fontsize=8, color="#666")
    ax.set_title(f"SARIMA 销售额预测（回测 MAPE={metrics['MAPE'].iloc[0]:.1f}%  RMSE={metrics['RMSE'].iloc[0]:.0f}）", color=C_DARK)
    ax.set_xlabel("月份", color="#555")
    ax.set_ylabel("销售额 (BRL)", color="#555")
    ax.legend(fontsize=9, framealpha=0.9)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig19_SARIMA预测_置信区间.png")


def main():
    print("=" * 60)
    print("04_visuals.py — 数据可视化（19 张图）")
    print("=" * 60)
    full = load_full()
    print(f"载入宽表：{full.shape}")
    print("模板复现类 12 张：")
    fig01_monthly_orders_bar(full)
    fig02_sales_line(full)
    fig03_payment_pie(full)
    fig04_dual_axis(full)
    fig05_stacked_bar_state(full)
    fig06_price_review_scatter(full)
    fig07_boxplot_state(full)
    fig08_heatmap_dow_hour(full)
    fig09_top_category_hbar(full)
    fig10_status_donut(full)
    fig11_radar_rfm()
    fig12_lollipop_new_customers(full)
    print("业务模型类 7 张：")
    fig13_rfm_bubble()
    fig14_rfm_segment_value()
    fig15_cohort_heatmap()
    fig16_pareto()
    fig17_abc_pie()
    fig18_trend_ma_yoy()
    fig19_sarima_forecast()
    print(f"\n全部 19 张图已输出到 {FIG}")


if __name__ == "__main__":
    main()
    print("完成。")

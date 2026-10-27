"""
04_visuals.py — 纽约 Airbnb 民宿数据可视化（全 Python 实现）
============================================================
对照《Excel数据可视化——从图表到数据大屏》12 种模板复现图 + 7 张业务模型图，共 19 张。
统一命名 fig01_*.png … fig19_*.png，输出到 outputs/figures/，分辨率 300dpi。

运行：python scripts/04_visuals.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch, FancyBboxPatch
import matplotlib.colors as mcolors
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ---- 全局样式（升级版）----
for _fp in [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\msyh.ttc"]:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "font.family": "sans-serif", "axes.unicode_minus": False,
    "figure.dpi": 150, "savefig.dpi": 300,
    "axes.titlesize": 15, "axes.titleweight": "bold", "axes.titlepad": 14,
    "axes.labelsize": 11, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "figure.facecolor": "white", "axes.facecolor": "#F8F9FB",
    "axes.edgecolor": "#C0C5CE", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#E2E5EA", "grid.linewidth": 0.6, "grid.alpha": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
})

# 升级配色（Material Design 风格）
C_BLUE = "#1565C0"; C_CORAL = "#E63946"; C_MINT = "#06A77D"; C_GOLD = "#F4A261"
C_PURPLE = "#7B2CBF"; C_CYAN = "#0096C7"; C_ORANGE = "#E76F51"; C_DARK = "#264653"
C_TEAL = "#2A9D8F"; C_PINK = "#EF476F"; C_INDIGO = "#4361EE"; C_LIME = "#80B918"
PALETTE = [C_BLUE, C_CORAL, C_MINT, C_GOLD, C_PURPLE, C_CYAN, C_ORANGE, C_DARK]
PALETTE8 = [C_BLUE, C_CORAL, C_MINT, C_GOLD, C_PURPLE, C_CYAN, C_TEAL, C_PINK]


def save(fig, name):
    fig.savefig(FIG / name, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  saved {name}")


def load_listings():
    df = pd.read_csv(CLEAN / "listings_clean.csv")
    for c in ["last_review", "host_since"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def try_load(name):
    p = TABLES / name
    if p.exists():
        return pd.read_csv(p)
    print(f"  [跳过] 未找到 {name}")
    return None


def style_ax(ax):
    ax.spines["left"].set_color("#9BA3AF")
    ax.spines["bottom"].set_color("#9BA3AF")
    ax.tick_params(colors="#6B7280")


def add_subtitle(fig, text):
    fig.text(0.5, 0.96, text, ha="center", va="top", fontsize=9,
             color="#9CA3AF", style="italic")


def gradient_bar(ax, x, y, color_from, color_to, width=0.6, **kwargs):
    """绘制渐变色柱形图。"""
    n = len(y)
    cmap = mcolors.LinearSegmentedColormap.from_list("g", [color_from, color_to])
    colors = [cmap(i / max(n - 1, 1)) for i in range(n)]
    return ax.bar(x, y, color=colors, width=width, edgecolor="white", linewidth=0.8, **kwargs)


# ============ 模板复现类 12 张 ============

def fig01_room_type_bar(df):
    """模板1·柱形图：房型分布（渐变色 + 数据标签 + 占比）。"""
    s = df["room_type"].value_counts()
    total = s.sum()
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = gradient_bar(ax, s.index, s.values, C_INDIGO, C_CYAN, width=0.55)
    for b, v in zip(bars, s.values):
        pct = v / total * 100
        ax.text(b.get_x() + b.get_width() / 2, v + s.max() * 0.015,
                f"{v:,}\n({pct:.1f}%)", ha="center", va="bottom",
                fontsize=9, color="#374151", fontweight="bold")
    ax.set_title("房型分布", color=C_DARK)
    ax.set_ylabel("房源数", color="#6B7280")
    ax.set_ylim(0, s.max() * 1.18)
    style_ax(ax)
    add_subtitle(fig, f"总房源数 {total:,} ｜ 纽约 Airbnb")
    plt.tight_layout(); save(fig, "fig01_房型分布_柱形图.png")


def fig02_monthly_reviews_line(df):
    """模板2·折线图：月度评论趋势（渐变填充 + 高峰标注）。"""
    d = df.dropna(subset=["last_review", "number_of_reviews"]).copy()
    d["ym"] = d["last_review"].dt.to_period("M").astype(str)
    s = d.groupby("ym")["number_of_reviews"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(s.index, s.values, alpha=0.2, color=C_BLUE, zorder=1)
    ax.plot(s.index, s.values, color=C_BLUE, linewidth=2.5, zorder=2)
    peak_idx = s.idxmax()
    ax.scatter([peak_idx], [s[peak_idx]], color=C_CORAL, s=80, zorder=3,
               edgecolor="white", linewidth=1.5)
    ax.annotate(f"峰值: {s[peak_idx]:,}", xy=(peak_idx, s[peak_idx]),
                xytext=(20, 10), textcoords="offset points",
                fontsize=9, color=C_CORAL, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_CORAL))
    ax.set_title("月度评论数趋势", color=C_DARK)
    ax.set_ylabel("评论数", color="#6B7280")
    ax.tick_params(axis="x", rotation=90)
    style_ax(ax)
    add_subtitle(fig, f"覆盖 {len(s)} 个月份 ｜ 总评论 {s.sum():,}")
    plt.tight_layout(); save(fig, "fig02_月度评论趋势_折线图.png")


def fig03_neighbourhood_pie(df):
    """模板3·饼图：行政区占比（环形 + 图例标注数量）。"""
    s = df["neighbourhood_group_cleansed"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6.5))
    explode = [0.05 if i == 0 else 0.02 for i in range(len(s))]
    wedges, _, autotexts = ax.pie(
        s.values, labels=None, autopct="%1.1f%%", colors=PALETTE[:len(s)], startangle=90,
        explode=explode, textprops={"fontsize": 11, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 3}, pctdistance=0.75)
    for t in autotexts:
        t.set_color("white")
    labels = [f"{idx}  ({val:,})" for idx, val in s.items()]
    ax.legend(wedges, labels, title="行政区", loc="center left",
              bbox_to_anchor=(1.05, 0.5), fontsize=10, title_fontsize=11, framealpha=0.9)
    ax.set_title("行政区房源占比", color=C_DARK, fontsize=16)
    add_subtitle(fig, f"共 {s.sum():,} 条房源 ｜ 5 个行政区")
    plt.tight_layout(); save(fig, "fig03_行政区占比_饼图.png")


def fig04_price_reviews_dual(df):
    """模板4·双轴组合图：价格直方图 + 评论数折线。"""
    d = df.dropna(subset=["price", "number_of_reviews"]).copy()
    d = d[d["price"] < d["price"].quantile(0.98)]
    bins = np.linspace(d["price"].min(), d["price"].max(), 30)
    centers = (bins[:-1] + bins[1:]) / 2
    counts, _ = np.histogram(d["price"], bins=bins)
    reviews = d.groupby(pd.cut(d["price"], bins=bins), observed=True)["number_of_reviews"].sum().values
    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.bar(centers, counts, width=(bins[1] - bins[0]) * 0.85, color=C_BLUE, alpha=0.7,
            edgecolor="white", linewidth=0.5, label="房源数")
    ax1.set_ylabel("房源数", color=C_BLUE, fontweight="bold")
    ax1.tick_params(axis="y", colors=C_BLUE)
    ax2 = ax1.twinx()
    ax2.plot(centers, reviews, color=C_CORAL, linewidth=2.5, marker="o", markersize=4,
             markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=1.5, label="评论数")
    ax2.fill_between(centers, reviews, alpha=0.08, color=C_CORAL)
    ax2.set_ylabel("评论数", color=C_CORAL, fontweight="bold")
    ax2.tick_params(axis="y", colors=C_CORAL)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(C_CORAL)
    ax1.set_title("价格分布与评论数（双轴组合图）", color=C_DARK)
    ax1.set_xlabel("价格 (USD)", color="#6B7280")
    fig.legend(loc="upper right", bbox_to_anchor=(0.92, 0.90), fontsize=9, framealpha=0.9)
    style_ax(ax1)
    add_subtitle(fig, f"房源数 {len(d):,} ｜ 价格区间 ${d['price'].min():.0f}–${d['price'].max():.0f}")
    plt.tight_layout(); save(fig, "fig04_价格评论数_双轴组合图.png")


def fig05_neighbourhood_room_stacked(df):
    """模板5·堆积柱形图：各行政区各房型数量堆积。"""
    pivot = df.pivot_table(index="neighbourhood_group_cleansed", columns="room_type",
                           values="id", aggfunc="count", observed=True).fillna(0)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    pivot.plot.bar(stacked=True, ax=ax, color=[C_BLUE, C_CORAL, C_MINT, C_GOLD],
                   width=0.6, edgecolor="white", linewidth=0.8)
    for i, (idx, row) in enumerate(pivot.iterrows()):
        total = row.sum()
        ax.text(i, total + pivot.sum().max() * 0.01, f"{int(total):,}",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color="#374151")
    ax.set_title("各行政区房型分布（堆积柱形图）", color=C_DARK)
    ax.set_ylabel("房源数", color="#6B7280")
    ax.set_xlabel("行政区", color="#6B7280")
    ax.legend(title="房型", fontsize=9, framealpha=0.9, loc="upper right")
    ax.set_ylim(0, pivot.sum().max() * 1.12)
    style_ax(ax)
    plt.tight_layout(); save(fig, "fig05_行政区房型_堆积柱形图.png")


def fig06_price_rating_scatter(df):
    """模板6·散点图：价格 vs 评分（按评分着色 + 密度轮廓）。"""
    d = df.dropna(subset=["price", "review_scores_rating"]).copy()
    d = d[(d["price"] < d["price"].quantile(0.98)) & (d["review_scores_rating"] > 0)]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sc = ax.scatter(d["price"], d["review_scores_rating"], s=10, alpha=0.4,
                    c=d["review_scores_rating"], cmap="RdYlGn", edgecolors="none")
    ax.axhline(4.5, color=C_CORAL, linestyle="--", linewidth=1, alpha=0.5)
    ax.text(d["price"].max() * 0.95, 4.52, "4.5分线", fontsize=8, color=C_CORAL, ha="right")
    ax.set_title("价格与评分（散点图）", color=C_DARK)
    ax.set_xlabel("价格 (USD)", color="#6B7280")
    ax.set_ylabel("评分", color="#6B7280")
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("评分", fontsize=10)
    style_ax(ax)
    add_subtitle(fig, f"样本 {len(d):,} ｜ 评分均值 {d['review_scores_rating'].mean():.2f}")
    plt.tight_layout(); save(fig, "fig06_价格评分_散点图.png")


def fig07_neighbourhood_price_box(df):
    """模板7·箱线图：各行政区价格分布（均值标记 + 样本数）。"""
    d = df.dropna(subset=["price"]).copy()
    d = d[d["price"] < d["price"].quantile(0.95)]
    order = d.groupby("neighbourhood_group_cleansed")["price"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    sns.boxplot(data=d, x="neighbourhood_group_cleansed", y="price", ax=ax, order=order,
                palette=PALETTE[:len(order)], fliersize=2, linewidth=1.3,
                boxprops=dict(alpha=0.85), medianprops=dict(color=C_DARK, linewidth=2),
                meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor=C_DARK, markersize=6),
                showmeans=True)
    for i, grp in enumerate(order):
        n = len(d[d["neighbourhood_group_cleansed"] == grp])
        med = d[d["neighbourhood_group_cleansed"] == grp]["price"].median()
        ax.text(i, med, f"  ${med:.0f}", fontsize=8, color=C_DARK, fontweight="bold", va="center")
        ax.text(i, -d["price"].max() * 0.04, f"n={n:,}", fontsize=8, color="#9CA3AF", ha="center")
    ax.set_title("各行政区价格分布（箱线图）", color=C_DARK)
    ax.set_xlabel("行政区", color="#6B7280")
    ax.set_ylabel("价格 (USD)", color="#6B7280")
    style_ax(ax)
    add_subtitle(fig, "◆ 为均值 ｜ 已剔除前5%极端值")
    plt.tight_layout(); save(fig, "fig07_行政区价格_箱线图.png")


def fig08_price_availability_heatmap(df):
    """模板8·热力图：价格分箱 × 可住天数分箱（数值标注）。"""
    d = df.dropna(subset=["price", "availability_365"]).copy()
    d = d[(d["price"] > 0) & (d["price"] < d["price"].quantile(0.95))]
    d["price_bin"] = pd.cut(d["price"], bins=10, labels=[f"${int(b)}" for b in pd.cut(d["price"], bins=10).cat.categories.left])
    d["avail_bin"] = pd.cut(d["availability_365"], bins=8,
                            labels=[f"{int(b)}d" for b in pd.cut(d["availability_365"], bins=8).cat.categories.left])
    pivot = d.pivot_table(index="price_bin", columns="avail_bin", values="id", aggfunc="count", observed=True).fillna(0)
    fig, ax = plt.subplots(figsize=(12, 5.5))
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".0f", annot_kws={"fontsize": 7},
                ax=ax, cbar_kws={"label": "房源数"}, linewidths=0.4, linecolor="white")
    ax.set_title("价格 × 可住天数 热力图", color=C_DARK)
    ax.set_xlabel("可住天数", color="#6B7280")
    ax.set_ylabel("价格", color="#6B7280")
    add_subtitle(fig, f"样本 {len(d):,} ｜ 颜色越深房源越密集")
    plt.tight_layout(); save(fig, "fig08_价格可住天数_热力图.png")


def fig09_top10_neighbourhood_hbar(df):
    """模板9·水平条形图：Top10 街区房源数（渐变 + 数据标签）。"""
    s = df["neighbourhood_cleansed"].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    bars = gradient_bar(ax, s.values, s.index, C_TEAL, C_BLUE, width=0.6)
    ax.barh(s.index, s.values, color=plt.cm.viridis(np.linspace(0.2, 0.85, len(s))),
            height=0.6, edgecolor="white", linewidth=0.8)
    for i, v in enumerate(s.values):
        ax.text(v + s.max() * 0.01, i, f"{v:,}", fontsize=9, va="center",
                color="#374151", fontweight="bold")
    ax.set_title("Top10 街区房源数（水平条形图）", color=C_DARK)
    ax.set_xlabel("房源数", color="#6B7280")
    ax.set_xlim(0, s.max() * 1.15)
    style_ax(ax)
    add_subtitle(fig, "按房源数降序排列 ｜ Top10 街区")
    plt.tight_layout(); save(fig, "fig09_Top10街区房源_水平条形图.png")


def fig10_room_type_donut(df):
    """模板10·圆环图：房型占比（中心总房源数 + 外圈标签）。"""
    s = df["room_type"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6.5))
    wedges, _, autotexts = ax.pie(
        s.values, labels=None, autopct="%1.1f%%", colors=[C_BLUE, C_CORAL, C_MINT, C_GOLD],
        startangle=90, pctdistance=0.82, textprops={"fontsize": 11},
        wedgeprops={"edgecolor": "white", "linewidth": 3, "width": 0.45})
    for t in autotexts:
        t.set_fontsize(11); t.set_fontweight("bold"); t.set_color("white")
    ax.add_artist(plt.Circle((0, 0), 0.52, fc="white", ec="#E5E7EB", linewidth=2))
    ax.text(0, 0.1, f"{s.sum():,}", ha="center", va="center", fontsize=18,
            fontweight="bold", color=C_DARK)
    ax.text(0, -0.12, "总房源数", ha="center", va="center", fontsize=10, color="#9CA3AF")
    labels = [f"{idx}  ({val:,})" for idx, val in s.items()]
    ax.legend(wedges, labels, title="房型", loc="center left",
              bbox_to_anchor=(1.05, 0.5), fontsize=10, title_fontsize=11, framealpha=0.9)
    ax.set_title("房型占比（圆环图）", color=C_DARK, fontsize=16)
    plt.tight_layout(); save(fig, "fig10_房型占比_圆环图.png")


def fig11_cluster_radar():
    """模板11·雷达图：4 个 K-Means 聚类的归一化特征。"""
    centers = try_load("kmeans_centers.csv")
    if centers is None:
        return
    feat_cols = [c for c in centers.columns if c != "cluster"]
    centers = centers.head(4)
    norm = centers[feat_cols].copy()
    for c in feat_cols:
        norm[c] = norm[c] / norm[c].max()
    angles = np.linspace(0, 2 * np.pi, len(feat_cols), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
    ax.set_facecolor("#F8F9FB")
    ax.set_ylim(0, 1.15)
    ax.grid(color="#D1D5DB", linewidth=0.8, alpha=0.7)
    for i, (_, row) in enumerate(norm.iterrows()):
        vals = row.tolist() + [row.tolist()[0]]
        ax.plot(angles, vals, linewidth=2.8, label=f"簇 {centers.iloc[i]['cluster']}",
                color=PALETTE8[i], marker="o", markersize=7,
                markerfacecolor="white", markeredgecolor=PALETTE8[i], markeredgewidth=2.2)
        ax.fill(angles, vals, alpha=0.15, color=PALETTE8[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feat_cols, fontsize=9, fontweight="bold", color=C_DARK)
    ax.set_title("K-Means 聚类特征（雷达图）", pad=28, color=C_DARK, fontsize=16)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9, framealpha=0.9)
    add_subtitle(fig, "各特征归一化至 [0, 1] ｜ 4 个聚类中心")
    plt.tight_layout(); save(fig, "fig11_聚类特征_雷达图.png")


def fig12_new_hosts_lollipop(df):
    """模板12·棒棒糖图：各月活跃房源数（渐变茎 + 大头标记）。"""
    d = df.dropna(subset=["last_review"]).copy()
    s = d.groupby(d["last_review"].dt.to_period("M").astype(str))["id"].count().sort_index()
    s = s.iloc[-24:]
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = plt.cm.viridis(np.linspace(0.3, 0.85, len(s)))
    ax.vlines(s.index, 0, s.values, colors=colors, linewidth=2.5, alpha=0.7)
    ax.scatter(s.index, s.values, c=colors, s=50, zorder=3, edgecolor="white", linewidth=1)
    ax.set_title("近24月活跃房源数（棒棒糖图）", color=C_DARK)
    ax.set_ylabel("活跃房源数", color="#6B7280")
    ax.tick_params(axis="x", rotation=90)
    ax.set_ylim(0, s.max() * 1.12)
    style_ax(ax)
    add_subtitle(fig, f"近24月 ｜ 月均 {s.mean():.0f} 套活跃房源")
    plt.tight_layout(); save(fig, "fig12_各月新增房东_棒棒糖图.png")


# ============ 业务模型类 7 张 ============

def fig13_kmeans_scatter():
    """业务图1·KMeans 聚类散点图：经度 × 纬度，按 cluster 着色 + 簇心标注。"""
    c = try_load("kmeans_clusters.csv")
    if c is None:
        return
    df = pd.read_csv(CLEAN / "listings_clean.csv", usecols=["id", "longitude", "latitude"])
    c = c.merge(df, on="id", how="inner")
    fig, ax = plt.subplots(figsize=(10, 8))
    for k, grp in c.groupby("cluster"):
        ax.scatter(grp["longitude"], grp["latitude"], s=6, alpha=0.45,
                   color=PALETTE8[int(k) % len(PALETTE8)], label=f"簇 {k} ({len(grp):,})", edgecolors="none")
        cx, cy = grp["longitude"].mean(), grp["latitude"].mean()
        ax.scatter([cx], [cy], s=120, marker="X", color=PALETTE8[int(k) % len(PALETTE8)],
                   edgecolor="white", linewidth=2, zorder=5)
    ax.set_title("KMeans 聚类散点图（经度 × 纬度）", color=C_DARK)
    ax.set_xlabel("经度", color="#6B7280")
    ax.set_ylabel("纬度", color="#6B7280")
    ax.legend(loc="best", fontsize=9, framealpha=0.9, markerscale=1.5, title="聚类 (样本数)")
    style_ax(ax)
    add_subtitle(fig, "X 为簇中心 ｜ K=4 ｜ 标准化后聚类")
    plt.tight_layout(); save(fig, "fig13_KMeans聚类_散点图.png")


def fig14_feature_importance():
    """业务图2·随机森林特征重要性 Top15 水平条形图（渐变 + 数据标签）。"""
    fi = try_load("rf_feature_importance.csv")
    if fi is None:
        return
    fi = fi.sort_values("importance", ascending=True).tail(15)
    fig, ax = plt.subplots(figsize=(9.5, 6.5))
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(fi)))
    bars = ax.barh(fi["feature"], fi["importance"], color=colors, height=0.65,
                   edgecolor="white", linewidth=0.8)
    for b, v in zip(bars, fi["importance"]):
        ax.text(v + fi["importance"].max() * 0.01, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", fontsize=8, va="center", color="#374151", fontweight="bold")
    ax.set_title("随机森林特征重要性 Top15", color=C_DARK)
    ax.set_xlabel("重要性", color="#6B7280")
    ax.set_xlim(0, fi["importance"].max() * 1.18)
    style_ax(ax)
    add_subtitle(fig, "n_estimators=200 ｜ 随机森林回归")
    plt.tight_layout(); save(fig, "fig14_特征重要性_条形图.png")


def fig15_price_residual():
    """业务图3·定价预测残差图：实际值 vs 预测值散点 + 对角线 + R²标注。"""
    p = try_load("rf_predictions.csv")
    if p is None:
        return
    actual = p["y_true"].values
    pred = p["y_pred"].values
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(actual, pred, s=10, alpha=0.35, c=actual, cmap="coolwarm",
               edgecolors="none")
    lim = [min(actual.min(), pred.min()), max(actual.max(), pred.max())]
    ax.plot(lim, lim, color=C_DARK, linewidth=2.5, linestyle="--", label="理想预测线 y=x", zorder=5)
    from sklearn.metrics import r2_score, mean_squared_error
    r2 = r2_score(actual, pred)
    rmse = np.sqrt(mean_squared_error(actual, pred))
    ax.text(0.05, 0.92, f"R² = {r2:.3f}\nRMSE = {rmse:.1f}", transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=C_DARK,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=C_DARK, alpha=0.9))
    ax.set_title("定价预测：实际值 vs 预测值", color=C_DARK)
    ax.set_xlabel("实际价格 (USD)", color="#6B7280")
    ax.set_ylabel("预测价格 (USD)", color="#6B7280")
    ax.legend(fontsize=10, framealpha=0.9, loc="lower right")
    style_ax(ax)
    add_subtitle(fig, f"样本 {len(p):,} ｜ 随机森林回归模型")
    plt.tight_layout(); save(fig, "fig15_定价预测_残差图.png")


def fig16_host_value_segment():
    """业务图4·房东价值分层图：RFM 各 segment 房东数柱形 + 金额占比折线。"""
    rfm = try_load("host_rfm.csv")
    if rfm is None:
        return
    seg = rfm.groupby("segment").agg(房东数=("host_id", "count"), 金额=("M", "sum")).reset_index()
    seg["金额占比"] = seg["金额"] / seg["金额"].sum()
    seg = seg.sort_values("金额", ascending=False)
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    colors = plt.cm.tab10(np.linspace(0, 0.8, len(seg)))
    bars = ax1.bar(seg["segment"], seg["房东数"], color=colors, width=0.6, alpha=0.85,
                   edgecolor="white", linewidth=0.8, label="房东数")
    for b, v in zip(bars, seg["房东数"]):
        ax1.text(b.get_x() + b.get_width() / 2, v + seg["房东数"].max() * 0.02,
                 f"{int(v):,}", ha="center", va="bottom", fontsize=8, color="#374151", fontweight="bold")
    ax1.set_ylabel("房东数", color=C_BLUE, fontweight="bold")
    ax1.tick_params(axis="y", colors=C_BLUE)
    ax1.tick_params(axis="x", rotation=30)
    ax2 = ax1.twinx()
    ax2.plot(seg["segment"], seg["金额占比"] * 100, color=C_CORAL, linewidth=2.8, marker="o",
             markersize=7, markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=2, label="金额占比(%)")
    ax2.fill_between(seg["segment"], seg["金额占比"] * 100, alpha=0.08, color=C_CORAL)
    ax2.set_ylabel("金额占比 (%)", color=C_CORAL, fontweight="bold")
    ax2.tick_params(axis="y", colors=C_CORAL)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(C_CORAL)
    ax1.set_title("房东价值分层（RFM 分群）", color=C_DARK)
    ax1.set_ylim(0, seg["房东数"].max() * 1.15)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9, framealpha=0.9)
    style_ax(ax1)
    add_subtitle(fig, f"8 个分群 ｜ 总房东 {seg['房东数'].sum():,}")
    plt.tight_layout(); save(fig, "fig16_房东价值_分层图.png")


def fig17_geo_price_scatter(df):
    """业务图5·地理价格散点图：经度 × 纬度，按 price 着色 + 行政区标注。"""
    d = df.dropna(subset=["longitude", "latitude", "price"]).copy()
    d = d[(d["price"] > 0) & (d["price"] < d["price"].quantile(0.98))]
    fig, ax = plt.subplots(figsize=(10, 8))
    sc = ax.scatter(d["longitude"], d["latitude"], s=5, alpha=0.55, c=d["price"],
                    cmap="plasma", edgecolors="none")
    boroughs = {
        "Manhattan": (-73.97, 40.77), "Brooklyn": (-73.95, 40.65),
        "Queens": (-73.80, 40.73), "Bronx": (-73.87, 40.85),
        "Staten Island": (-74.15, 40.58),
    }
    for name, (lon, lat) in boroughs.items():
        ax.annotate(name, xy=(lon, lat), fontsize=9, fontweight="bold",
                    color="white", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=C_DARK, alpha=0.7))
    ax.set_title("地理价格分布（经度 × 纬度）", color=C_DARK)
    ax.set_xlabel("经度", color="#6B7280")
    ax.set_ylabel("纬度", color="#6B7280")
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("价格 (USD)", fontsize=10)
    style_ax(ax)
    add_subtitle(fig, f"样本 {len(d):,} ｜ plasma 色图按价格着色")
    plt.tight_layout(); save(fig, "fig17_地理价格_散点图.png")


def fig18_neighbourhood_pareto(df):
    """业务图6·街区帕累托图：Top20 街区贡献柱形 + 累计占比折线 + ABC 着色。"""
    s = df["neighbourhood_cleansed"].value_counts().head(20)
    cum = s.cumsum() / s.sum()
    abc = np.where(cum <= 0.70, "A", np.where(cum <= 0.90, "B", "C"))
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    colors = {"A": C_BLUE, "B": C_GOLD, "C": C_CORAL}
    bars = ax1.bar(s.index, s.values, color=[colors[c] for c in abc], width=0.65,
                   edgecolor="white", linewidth=0.8)
    for b, v in zip(bars, s.values):
        ax1.text(b.get_x() + b.get_width() / 2, v + s.max() * 0.01, f"{v}",
                 ha="center", va="bottom", fontsize=7, color="#6B7280")
    ax1.set_ylabel("房源数", color="#6B7280")
    ax1.tick_params(axis="x", rotation=90)
    ax2 = ax1.twinx()
    ax2.plot(s.index, cum * 100, color=C_DARK, linewidth=2.5, marker="o", markersize=5,
             markerfacecolor="white", markeredgecolor=C_DARK, markeredgewidth=1.8)
    ax2.set_ylabel("累计占比 (%)", color="#6B7280")
    ax2.set_ylim(0, 108)
    ax2.axhline(70, color=C_CORAL, linestyle="--", linewidth=1.2, alpha=0.7)
    ax2.axhline(90, color=C_DARK, linestyle="--", linewidth=1.2, alpha=0.5)
    ax2.text(len(s) - 0.5, 71, "70%", fontsize=8, color=C_CORAL, ha="right")
    ax2.text(len(s) - 0.5, 91, "90%", fontsize=8, color=C_DARK, ha="right")
    ax2.spines["right"].set_visible(True)
    ax1.set_title("街区帕累托图（Top20，ABC 分类）", color=C_DARK)
    legend = [Patch(facecolor=colors[k], label=f"{k}类 ({sum(abc==k)}个)") for k in ["A", "B", "C"]]
    ax1.legend(handles=legend, title="ABC分类", loc="center right", framealpha=0.9)
    style_ax(ax1)
    add_subtitle(fig, f"A类贡献 {cum[cum<=0.70].iloc[-1]*100:.1f}% ｜ 符合帕累托二八定律")
    plt.tight_layout(); save(fig, "fig18_街区帕累托图.png")


def fig19_reviews_moving_avg(df):
    """业务图7·评论趋势移动平均：月度评论数柱形 + 3 月移动平均折线。"""
    d = df.dropna(subset=["last_review", "number_of_reviews"]).copy()
    d["ym"] = d["last_review"].dt.to_period("M").astype(str)
    s = d.groupby("ym")["number_of_reviews"].sum().sort_index()
    ma = s.rolling(3, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.bar(s.index, s.values, color=C_BLUE, width=0.55, alpha=0.55, label="月度评论数",
           edgecolor="white", linewidth=0.3)
    ax.plot(ma.index, ma.values, color=C_CORAL, linewidth=2.8, marker="o", markersize=4,
            markerfacecolor="white", markeredgecolor=C_CORAL, markeredgewidth=1.5, label="3月移动平均")
    ax.fill_between(ma.index, ma.values, alpha=0.08, color=C_CORAL)
    ax.set_title("月度评论数与 3 月移动平均", color=C_DARK)
    ax.set_ylabel("评论数", color="#6B7280")
    ax.tick_params(axis="x", rotation=90)
    ax.legend(fontsize=10, framealpha=0.9, loc="upper left")
    style_ax(ax)
    add_subtitle(fig, f"覆盖 {len(s)} 个月 ｜ 移分平滑窗口=3")
    plt.tight_layout(); save(fig, "fig19_评论趋势_移动平均.png")


def main():
    print("=" * 60)
    print("04_visuals.py — 纽约 Airbnb 可视化（19 张图·升级版）")
    print("=" * 60)
    df = load_listings()
    print(f"载入 listings_clean.csv：{df.shape}")
    print("\n模板复现类 12 张：")
    fig01_room_type_bar(df)
    fig02_monthly_reviews_line(df)
    fig03_neighbourhood_pie(df)
    fig04_price_reviews_dual(df)
    fig05_neighbourhood_room_stacked(df)
    fig06_price_rating_scatter(df)
    fig07_neighbourhood_price_box(df)
    fig08_price_availability_heatmap(df)
    fig09_top10_neighbourhood_hbar(df)
    fig10_room_type_donut(df)
    fig11_cluster_radar()
    fig12_new_hosts_lollipop(df)
    print("\n业务模型类 7 张：")
    fig13_kmeans_scatter()
    fig14_feature_importance()
    fig15_price_residual()
    fig16_host_value_segment()
    fig17_geo_price_scatter(df)
    fig18_neighbourhood_pareto(df)
    fig19_reviews_moving_avg(df)
    print(f"\n全部完成，图片已输出到 {FIG}")


if __name__ == "__main__":
    main()
    print("完成。")

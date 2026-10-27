"""第10章 效应分解法-信用卡消费额(去除节日)预测 -> Python
原素材: 信用卡消费额_去除节日.xlsx + 信用卡消费额_含节日.xlsx
内涵: 对去除节日效应的日度消费额做 趋势+星期季节+残差 分解,
       残差应无显著正偏差(节日已剔除), 用趋势+季节外推未来7天预测;
       对比含节日版残差, 验证去除节日后预测更平稳.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "CDA 教材资料2025" / "1《CDA 一级认证教材：商业数据分析》" / "第10章 使用效应分解方法做预报"


def decompose(dates, y, window=7):
    n = len(y)
    dow = pd.Series(dates).dt.dayofweek.values
    trend = pd.Series(y).rolling(window, center=True, min_periods=window).mean().values
    detrend = y - trend
    smean = {}
    for d in range(7):
        v = detrend[dow == d]; v = v[~np.isnan(v)]
        smean[d] = v.mean() if v.size else 0
    seasonal = np.array([smean[d] for d in dow])
    seasonal = seasonal - seasonal.mean()
    resid = y - trend - seasonal
    return trend, seasonal, resid, smean, dow


def forecast(dates, y, smean, days=7):
    last_trend = pd.Series(y).rolling(7, center=True, min_periods=7).mean().values
    last_trend = last_trend[~np.isnan(last_trend)][-3:].mean()
    future_dates = pd.date_range(dates[-1] + pd.Timedelta(days=1), periods=days)
    future_dow = future_dates.dayofweek.values
    s_bar = np.mean(list(smean.values()))
    future_seasonal = np.array([smean[d] - s_bar for d in future_dow])
    return future_dates, last_trend + future_seasonal


d_clean = pd.read_excel(B / "信用卡消费额_去除节日.xlsx")
d_clean["日期"] = pd.to_datetime(d_clean["日期"])
d_clean = d_clean.sort_values("日期").reset_index(drop=True)
y_c = d_clean.iloc[:, 1].values.astype(float)

d_raw = pd.read_excel(B / "信用卡消费额_含节日.xlsx", sheet_name="pos")
d_raw["date"] = pd.to_datetime(d_raw["date"])
d_raw = d_raw.sort_values("date").reset_index(drop=True)
y_r = d_raw["amount"].values.astype(float)

tr_c, se_c, re_c, sm_c, dow_c = decompose(d_clean["日期"], y_c)
tr_r, se_r, re_r, sm_r, dow_r = decompose(d_raw["date"], y_r)
thr_c = 1.5 * np.nanstd(re_c)
thr_r = 1.5 * np.nanstd(re_r)
fest_c = re_c > thr_c
fest_r = re_r > thr_r
fc_dates, fc_vals = forecast(d_clean["日期"].values, y_c, sm_c, days=7)

print(f"去除节日: 残差std={np.nanstd(re_c):.2f} 节日效应日={fest_c.sum()}")
print(f"含节日:   残差std={np.nanstd(re_r):.0f} 节日效应日={fest_r.sum()}")
print(f"残差波动比(含/去): {np.nanstd(re_r)/np.nanstd(re_c):.1f}倍")
print("\n== 去除节日 未来7天预测 ==")
for dt, v in zip(fc_dates, fc_vals):
    print(f"  {dt.strftime('%Y-%m-%d')}  预测{v:.1f}")

fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=False)
axes[0].plot(d_clean["日期"], y_c, color="#4C78A8", label="去除节日实际")
axes[0].plot(d_clean["日期"], tr_c + se_c, color="#E45756", ls="--", label="趋势+季节")
axes[0].plot(fc_dates, fc_vals, color="#54A24B", ls="-", marker="o", ms=4, label="预测")
axes[0].axvline(d_clean["日期"].iloc[-1], color="gray", ls=":", lw=0.8)
axes[0].set_title("去除节日: 实际/拟合/未来7天预测", fontsize=10); axes[0].legend(fontsize=7)
axes[1].plot(d_raw["date"], re_r, color="#E45756", alpha=0.7, label="含节日残差")
axes[1].plot(d_clean["日期"], re_c, color="#4C78A8", label="去除节日残差")
axes[1].axhline(thr_r, color="#E45756", ls="--", lw=0.8)
axes[1].axhline(thr_c, color="#4C78A8", ls="--", lw=0.8)
axes[1].set_title("残差对比(虚线=1.5σ阈值)", fontsize=10); axes[1].legend(fontsize=7)
wd = ["一", "二", "三", "四", "五", "六", "日"]
s_bar = np.mean(list(sm_c.values()))
sv = [sm_c[d] - s_bar for d in range(7)]
axes[2].bar(wd, sv, color="#F58518")
axes[2].set_title("去除节日: 星期季节分量", fontsize=10)
plt.tight_layout()
out = Path(__file__).resolve().parent / "第10章_信用卡去除节日预测.png"
plt.savefig(out, dpi=130)
print(f"\n图已保存: {out.name}")

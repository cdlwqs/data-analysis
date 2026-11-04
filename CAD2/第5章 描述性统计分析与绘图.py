# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第5章-数据可视化")
"""
第5章 描述性统计分析与绘图
==========================
项目内涵：用 pandas 对连续变量做描述性统计，量化"集中趋势—离散程度—分布形态"三维度，
         并计算变量间相关系数。
技术方法：mean/median/std、quantile、max-min(极差)、var、skew(偏度)、kurtosis(峰度)、
         corr(pearson/spearman/kendall)。
数据源：sndHsPr.csv（二手房价数据，含面积 AREA 与价格 price）。
关键步骤：1)集中趋势(均值/中位数/标准差/分位数) → 2)离散程度(极差/方差/标准差)
         → 3)分布形态(偏度/峰度) → 4)相关系数(三种)。
"""

# 3.1.3 连续变量的分布与集中趋势


import pandas as pd
data = pd.read_csv('sndHsPr.csv')


data.price.agg(['mean','median','std'])


data. price.quantile([0.25,0.5,0.75])


data.price.hist(bins=20)


# 3.1.4 连续变量的离散程度


data.price.max()-data.price.min()


data.price.var()#求方差


data.price.std()#求标准差


# 3.1.5 数据分布的对称与高矮


import numpy as np


normal = pd.Series(np.random.randn(1000),name='normal')


normal.skew()


normal.kurtosis()


data[['AREA','price']].corr("pearson")


data[['AREA','price']].corr("spearman")


data[['AREA','price']].corr("kendall")



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第5章 描述性统计分析与绘图
# ==========================
# 项目内涵：用 pandas 对连续变量做描述性统计，量化"集中趋势—离散程度—分布形态"三维度，
#          并计算变量间相关系数。
# 技术方法：mean/median/std、quantile、max-min(极差)、var、skew(偏度)、kurtosis(峰度)、
#          corr(pearson/spearman/kendall)。
# 数据源：sndHsPr.csv（二手房价数据，含面积 AREA 与价格 price）。
# 关键步骤：1)集中趋势(均值/中位数/标准差/分位数) → 2)离散程度(极差/方差/标准差)
#          → 3)分布形态(偏度/峰度) → 4)相关系数(三种)。
#
# mean      61151.810919
# median    57473.000000
# std       22293.358147
# Name: price, dtype: float64
# 0.25    42812.25
# 0.50    57473.00
# 0.75    76099.75
# Name: price, dtype: float64
# 131523
# 496993817.485068
# 22293.358147328723
# 0.01696467399394673
# -0.030492329132367324
#            AREA     price
# AREA   1.000000 -0.073955
# price -0.073955  1.000000
#            AREA     price
# AREA   1.000000 -0.114628
# price -0.114628  1.000000
#           AREA    price
# AREA   1.00000 -0.07458
# price -0.07458  1.00000

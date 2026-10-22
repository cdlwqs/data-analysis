# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第7章-特征降维方法")
"""
第7章 特征降维 —— 主成分分析(PCA)
===================================
项目内涵：电信运营商根据客户在主要业务上的使用情况做分群，原始变量较多且相关，
         用 PCA 把多个相关业务指标降为少数主成分，作为后续分群的输入。
技术方法：scale(中心标准化)、PCA(n_components, whiten)、explained_variance_ratio_、
         components_(载荷)、transform(得分)。
数据源：profile_telecom.csv（电信客户业务使用频次）。
关键步骤：1)读入并查看相关矩阵 → 2)中心标准化 → 3)拟合 PCA 取 2 个主成分
         → 4)查看方差解释率/载荷/主成分得分。
"""

# # 在 Python 中实现主成分分析. 
# 一家电信运营商希望根据客户在几个主要业务上的使用情况，对客户进行分群
# 分析。


# ![image.png](attachment:image.png)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


profile = pd.read_csv("profile_telecom.csv")
profile.head()


data = profile.loc[:,"cnt_call":]
data.corr(method = "pearson")


from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
data_scaled = scale(data)
pca = PCA(n_components = 2, whiten = True).fit(data_scaled)
pca.explained_variance_ratio_


pca.components_


pca.transform(data_scaled)



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第7章 特征降维 —— 主成分分析(PCA)
# ===================================
# 项目内涵：电信运营商根据客户在主要业务上的使用情况做分群，原始变量较多且相关，
#          用 PCA 把多个相关业务指标降为少数主成分，作为后续分群的输入。
# 技术方法：scale(中心标准化)、PCA(n_components, whiten)、explained_variance_ratio_、
#          components_(载荷)、transform(得分)。
# 数据源：profile_telecom.csv（电信客户业务使用频次）。
# 关键步骤：1)读入并查看相关矩阵 → 2)中心标准化 → 3)拟合 PCA 取 2 个主成分
#          → 4)查看方差解释率/载荷/主成分得分。
#
#         ID  cnt_call  cnt_msg  cnt_wei  cnt_web
# 0  1964627        46       90       36       31
# 1  3107769        53        2        0        2
# 2  3686296        28       24        5        8
# 3  3961002         9        2        0        4
# 4  4174839       145        2        0        1
#           cnt_call   cnt_msg   cnt_wei   cnt_web
# cnt_call  1.000000  0.052096  0.117832  0.114190
# cnt_msg   0.052096  1.000000  0.510686  0.739506
# cnt_wei   0.117832  0.510686  1.000000  0.950492
# cnt_web   0.114190  0.739506  0.950492  1.000000
# [0.62510442 0.24620209]
# [[ 0.11085805  0.50974123  0.57909319  0.62651852]
#  [ 0.99020127 -0.12736724 -0.01900236 -0.05401806]]
# [[ 2.30183615 -0.89716788]
#  [-0.74694076 -0.04035188]
#  [-0.11502116 -0.59578592]
#  ...
#  [ 2.19333782  0.04953167]
#  [-0.07833419 -0.10944885]
#  [-0.6621524   1.16641367]]

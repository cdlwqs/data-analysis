# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第6章-市场调研与数据预处理\2 数据预处理基础")
"""
第6章 数据预处理基础 —— 脏数据清洗
====================================
项目内涵：对外部获取的电信营销数据做基础质量检查与清洗，重点处理"用 0 表示缺失"的
         伪缺失值，并通过直方图观察分布。
技术方法：read_csv、describe、hist、replace({0:np.NaN})。
数据源：teleco_camp_orig.csv（电信营销客户收入/房价数据）。
关键步骤：1)读入并查看 AvgIncome 分布 → 2)describe 发现 0 值异常
         → 3)将 0 替换为 NaN → 4)指定值域重绘直方图。
"""

import pandas as pd
import os
import numpy as np
# 导入数据
camp = pd.read_csv(r"teleco_camp_orig.csv")
# 脏数据或数据不正确
import matplotlib.pyplot as plt
plt.hist(camp["AvgIncome"],bins=20)#,normed=True)#查看分布情况


camp["AvgIncome"].describe(include="all")


camp["AvgHomeValue"].describe(include="all")


#这里的 0值应该是缺失值，处理 0值。
camp["AvgIncome"]=camp["AvgIncome"].replace({0:np.nan})


#像这种外部获取的数据要比较小心，经常出现意义不清晰或这错误值。AvgHomeValue也有这种情况
plt.hist(camp["AvgIncome"],bins=20,range=(camp.AvgIncome.min(),camp.AvgIncome.max()))
#由于数据中存在缺失值 ,需要指定绘图的值域


camp["AvgHomeValue"].describe(include="all")



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第6章 数据预处理基础 —— 脏数据清洗
# ====================================
# 项目内涵：对外部获取的电信营销数据做基础质量检查与清洗，重点处理"用 0 表示缺失"的
#          伪缺失值，并通过直方图观察分布。
# 技术方法：read_csv、describe、hist、replace({0:np.NaN})。
# 数据源：teleco_camp_orig.csv（电信营销客户收入/房价数据）。
# 关键步骤：1)读入并查看 AvgIncome 分布 → 2)describe 发现 0 值异常
#          → 3)将 0 替换为 NaN → 4)指定值域重绘直方图。
#
# count      9686.000000
# mean      40491.444249
# std       28707.494146
# min           0.000000
# 25%       24464.000000
# 50%       43100.000000
# 75%       56876.000000
# max      200001.000000
# Name: AvgIncome, dtype: float64
# count      9686.000000
# mean     110986.299814
# std       98670.855450
# min           0.000000
# 25%       52300.000000
# 50%       76900.000000
# 75%      128175.000000
# max      600000.000000
# Name: AvgHomeValue, dtype: float64
# count      9686.000000
# mean     110986.299814
# std       98670.855450
# min           0.000000
# 25%       52300.000000
# 50%       76900.000000
# 75%      128175.000000
# max      600000.000000
# Name: AvgHomeValue, dtype: float64

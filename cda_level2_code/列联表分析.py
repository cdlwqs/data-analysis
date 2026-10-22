# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\列联表检验")
"""
第8章 列联表检验 —— 卡方独立性检验
====================================
项目内涵：检验两个分类变量(是否破产 bankruptcy_ind、是否坏账 bad_ind)是否独立，
         若显著相关则说明破产状态对坏账有解释力。
技术方法：pd.crosstab(列联表)、div(行百分比)、scipy.stats.chi2_contingency(卡方检验)。
数据源：accepts.csv（信贷接受记录，含破产标识与坏账标识）。
关键步骤：1)构建列联表(含边际) → 2)计算行百分比 → 3)卡方独立性检验输出卡方值/p值/自由度/期望频数。
"""

import pandas as pd
accepts =pd.read_csv ( 'accepts.csv' )
cross_table=pd.crosstab(accepts.bankruptcy_ind,accepts.bad_ind, margins=True)
cross_table


cross_table_rowpct = cross_table.div(cross_table ["All"] ,axis = 0)
cross_table_rowpct


# 打印结果
from scipy import stats
print(
    "chisq = %6.4f\np-value = %6.4f\ndof = %d\nexpected_freq = %s"
    %stats.chi2_contingency (cross_table))



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第8章 列联表检验 —— 卡方独立性检验
# ====================================
# 项目内涵：检验两个分类变量(是否破产 bankruptcy_ind、是否坏账 bad_ind)是否独立，
#          若显著相关则说明破产状态对坏账有解释力。
# 技术方法：pd.crosstab(列联表)、div(行百分比)、scipy.stats.chi2_contingency(卡方检验)。
# 数据源：accepts.csv（信贷接受记录，含破产标识与坏账标识）。
# 关键步骤：1)构建列联表(含边际) → 2)计算行百分比 → 3)卡方独立性检验输出卡方值/p值/自由度/期望频数。
#
# bad_ind            0     1   All
# bankruptcy_ind                  
# N               4163  1017  5180
# Y                345   103   448
# All             4508  1120  5628
# bad_ind                0         1  All
# bankruptcy_ind                         
# N               0.803668  0.196332  1.0
# Y               0.770089  0.229911  1.0
# All             0.800995  0.199005  1.0
# chisq = 2.9167
# p-value = 0.5719
# dof = 4
# expected_freq = [[4149.15422886 1030.84577114 5180.        ]
#  [ 358.84577114   89.15422886  448.        ]
#  [4508.         1120.         5628.        ]]

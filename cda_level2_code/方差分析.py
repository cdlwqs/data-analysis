# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\假设检验与方差分析")
"""
第8章 假设检验与方差分析（ANOVA）
==================================
项目内涵：检验分类变量(教育程度 edu_class、性别 gender)对连续型因变量(信用卡月均支出
         avg_exp)的影响是否显著，从单因素扩展到多因素含交互项。
技术方法：statsmodels ols + anova_lm，公式中 C() 表示分类变量。
数据源：creditcard_exp.csv（信用卡消费数据）。
关键步骤：1)读入并清洗(转字符串/浮点) → 2)单因素方差分析 avg_exp~C(edu_class)+C(gender)
         → 3)多因素含交互 avg_exp~C(edu_class)+C(gender)+C(edu_class)*C(gender)。
"""

# # 单因素方差分析


from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd


data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')


df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')


formula = f'avg_exp ~ C(edu_class) + C(gender)'
anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)


# # 多因素方差分析


data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')
df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')


formula = f'avg_exp ~ C(edu_class) + C(gender) + C(edu_class)*C(gender)'

anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第8章 假设检验与方差分析（ANOVA）
# ==================================
# 项目内涵：检验分类变量(教育程度 edu_class、性别 gender)对连续型因变量(信用卡月均支出
#          avg_exp)的影响是否显著，从单因素扩展到多因素含交互项。
# 技术方法：statsmodels ols + anova_lm，公式中 C() 表示分类变量。
# 数据源：creditcard_exp.csv（信用卡消费数据）。
# 关键步骤：1)读入并清洗(转字符串/浮点) → 2)单因素方差分析 avg_exp~C(edu_class)+C(gender)
#          → 3)多因素含交互 avg_exp~C(edu_class)+C(gender)+C(edu_class)*C(gender)。
#
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.731
# Model:                            OLS   Adj. R-squared:                  0.720
# Method:                 Least Squares   F-statistic:                     64.69
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           2.69e-26
# Time:                        19:16:56   Log-Likelihood:                -713.08
# No. Observations:                 100   AIC:                             1436.
# Df Residuals:                      95   BIC:                             1449.
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# =====================================================================================
#                         coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------------
# Intercept            28.1190     73.264      0.384      0.702    -117.329     173.567
# C(edu_class)[T.1]   383.2751     89.384      4.288      0.000     205.826     560.724
# C(edu_class)[T.2]   976.9943    100.255      9.745      0.000     777.962    1176.026
# C(edu_class)[T.3]  1435.7083    103.378     13.888      0.000    1230.477    1640.939
# C(gender)[T.1]      -91.4020     77.717     -1.176      0.243    -245.691      62.887
# ==============================================================================
# Omnibus:                        6.407   Durbin-Watson:                   2.370
# Prob(Omnibus):                  0.041   Jarque-Bera (JB):                5.840
# Skew:                           0.512   Prob(JB):                       0.0539
# Kurtosis:                       3.594   Cond. No.                         5.91
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.743
# Model:                            OLS   Adj. R-squared:                  0.724
# Method:                 Least Squares   F-statistic:                     38.06
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           1.56e-24
# Time:                        19:16:56   Log-Likelihood:                -710.82
# No. Observations:                 100   AIC:                             1438.
# Df Residuals:                      92   BIC:                             1458.
# Df Model:                           7                                         
# Covariance Type:            nonrobust                                         
# ====================================================================================================
#                                        coef    std err          t      P>|t|      [0.025      0.975]
# ----------------------------------------------------------------------------------------------------
# Intercept                           24.3965     74.767      0.326      0.745    -124.097     172.890
# C(edu_class)[T.1]                  385.8773     92.520      4.171      0.000     202.125     569.629
# C(edu_class)[T.2]                  915.2349    109.204      8.381      0.000     698.346    1132.124
# C(edu_class)[T.3]                 1529.5444    116.230     13.160      0.000    1298.701    1760.388
# C(gender)[T.1]                     -24.3965    317.210     -0.077      0.939    -654.403     605.610
# C(edu_class)[T.1]:C(gender)[T.1]   -58.7153    350.140     -0.168      0.867    -754.125     636.694
# C(edu_class)[T.2]:C(gender)[T.1]   121.2551    344.727      0.352      0.726    -563.402     805.913
# C(edu_class)[T.3]:C(gender)[T.1]  -265.2554    343.576     -0.772      0.442    -947.628     417.117
# ==============================================================================
# Omnibus:                       16.354   Durbin-Watson:                   2.368
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):               22.080
# Skew:                           0.797   Prob(JB):                     1.60e-05
# Kurtosis:                       4.662   Cond. No.                         24.4
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

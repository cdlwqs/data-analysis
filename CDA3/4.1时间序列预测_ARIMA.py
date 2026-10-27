"""ARIMA
原素材: 4.1时间序列预测\ARIMA.ipynb
"""

import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import warnings
import os

%matplotlib inline
warnings.filterwarnings("ignore")
ts_simu200 = pd.read_csv('ts_simu200.csv',index_col='t')
ts_simu200 .head()
dates = pd.date_range(start='2017/01/01', periods=200)
ts_simu200.set_index(dates, inplace=True)

dta = ts_simu200['AR1_a']
dta.plot(figsize=(8,5))
plt.show()
# 自相关和偏自相关

sm.graphics.tsa.plot_acf(dta,lags=20)#lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()
ar10 = sm.tsa.ARIMA(dta,order=(1, 0, 0)).fit()
#检验下残差序列：
resid = ar10.resid

sm.graphics.tsa.plot_acf(resid, lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()
# 从残差的ACF和PACF图，可以看到序列残差基本为白噪声
print(sm.stats.durbin_watson(ar10.resid.values))
print(stats.normaltest(resid))

fig, ax = plt.subplots(figsize=(5, 5))
qqplot(resid, line='q', fit=True, ax=ax)
plt.show()
# 预测: ar.predict 或者 ar.forcast
forcast= ar10.forecast(steps=5) 
print(pd.DataFrame({'forcast': forcast}))
dta = ts_simu200['MA1_a']

# 自相关和偏自相关
sm.graphics.tsa.plot_acf(dta,lags=20) #  lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()
#  拟合数据
ma01 = sm.tsa.ARIMA(dta,order=(0, 0, 1)).fit()
resid = ma01.resid

#  通过自相关检验残差
sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()
print(sm.stats.durbin_watson(ma01.resid))
print(stats.normaltest(resid).pvalue)
ma01.predict(start=pd.to_datetime('2017-07-20'),
             end=pd.to_datetime('2017-07-25'),
             dynamic=False)
dta=ts_simu200['ARMA_11_b']

sm.graphics.tsa.plot_acf(dta,lags=20)#lags 表示滞后的阶数
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()
# 暴力搜索最佳的自回归与移动平均的阶数

import warnings
import itertools

warnings.filterwarnings("ignore")  # 忽略ARIMA模型无法估计出结果时的报警信息

# 设置自相关(AR)、差分(I)、移动平均(MA)的三个参数的取值范围
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
temp_model = None

for param in pdq:
    try:
        temp_model = sm.tsa.ARIMA(dta,param)
        results = temp_model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
            best_seasonal_pdq = param_seasonal
    except:
        continue
        
print("Best ARIMA{} model - AIC:{}".format(best_pdq, best_aic))
arma11 = sm.tsa.ARIMA(dta,order=(1, 0, 1)).fit()
resid = arma11.resid

sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=20)
sm.graphics.tsa.plot_pacf(resid, lags=20)
plt.show()
print(sm.stats.durbin_watson(arma11.resid))
print(stats.normaltest(resid).pvalue)
arma11.predict(start=200,
               end=205,
               dynamic=False)
from statsmodels.tsa.stattools import adfuller

dta = ts_simu200['ARIMA_110']

#平稳性检验
result = adfuller(dta)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
#原序列的自相关和偏自相关
sm.graphics.tsa.plot_acf(dta,lags=20)
sm.graphics.tsa.plot_pacf(dta,lags=20)
plt.show()
dta.plot()
diff1= dta.diff(1)
diff1.plot(figsize=(8, 5))
plt.show()
print('p-value: %f' % adfuller(diff1[1:])[1])
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None
temp_model = None

for param in pdq:
    try:
        temp_model = sm.tsa.ARIMA(dta,param)
        results = temp_model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
    except:
        continue
        
print("Best ARIMA{} model - AIC:{}".format(best_pdq, best_aic))
arima110 = sm.tsa.ARIMA(dta,order=(1, 1, 0)).fit()


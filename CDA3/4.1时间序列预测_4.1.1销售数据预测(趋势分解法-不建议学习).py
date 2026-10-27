"""4.1.1销售数据预测(趋势分解法-不建议学习)
原素材: 4.1时间序列预测\4.1.1销售数据预测(趋势分解法-不建议学习).ipynb
"""

%matplotlib inline
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings("ignore") 
df = pd.read_csv('air.csv')
df['DATE'] = pd.to_datetime(df['DATE'])
df.head()
df.dtypes
df['DATE'] = pd.DatetimeIndex(df['DATE'])
df.dtypes
# 按照fbprophet的输入限制，传入的DataFrame.columns 必须为['ds', 'y']
df = df.rename(columns={'DATE': 'ds', 'AIR': 'y'})
df.head(2)
ax = df.set_index('ds').plot(figsize=(8, 5))
ax.set_title('Monthly Number of Airline Passengers', fontsize=15)
ax.set_xlabel('Date', fontsize=15)
plt.show()
# 设置趋势的形式和预测值的置信区间为95% 
my_model = Prophet(
    growth='linear',
    yearly_seasonality='auto',
    weekly_seasonality=False, 
    seasonality_mode='additive',
    daily_seasonality=False,
    holidays=None,
    interval_width=0.95, 
)
my_model.fit(df)
future_dates = my_model.make_future_dataframe(periods=36, freq='MS')
forecast = my_model.predict(future_dates)

forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title('Forcast of Airline Passengers', fontsize=15)
my_model.plot(forecast, ax=ax, uncertainty=True)
plt.show()
# 带节日效应的乘法模型建模
my_model = Prophet(
    growth='linear', 
    seasonality_mode='multiplicative',
    holidays=None,
    interval_width=0.95
)

# 增加节假日效应
my_model.add_country_holidays('China')

my_model.fit(df)
from fbprophet.plot import add_changepoints_to_plot

#  预测
future_dates = my_model.make_future_dataframe(periods=36, freq='MS')
forecast = my_model.predict(future_dates)

#  绘图
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title('Forcast of Airline Passengers', fontsize=15)
my_model.plot(forecast,uncertainty=True, ax=ax)   

#  绘制changepoints
add_changepoints_to_plot(ax, my_model, forecast)  
plt.show()
my_model.plot_components(forecast, figsize=(7, 5))
plt.show()
forecast.tail(5)

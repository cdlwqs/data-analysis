"""2.3.3变量聚类
原素材: 2.3用户画像（主成分、因子分析、变量聚类、层次聚类、kmeans聚类）\2.3.3变量聚类.ipynb
"""

import sys
sys.path.append("./myscript")

import pandas as pd
from varSelec import var_select

# 读取数据
model_data = pd.read_csv("cities_10.csv", encoding='gbk')
model_data.head()
data = model_data.loc[ :,'X1':]

# 变量聚类，并选择保留k个变量
selected_data = var_select(data, k=2)
selected_data


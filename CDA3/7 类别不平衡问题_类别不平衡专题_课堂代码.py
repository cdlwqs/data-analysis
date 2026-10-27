"""类别不平衡专题_课堂代码
原素材: 7 类别不平衡问题\类别不平衡专题_课堂代码.ipynb
"""

# pip install imbalanced-learn
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
class_1 = 1000       #类别1有1000个样本
class_2 = 100        #类别2只有100个
centers = [[0,0], [2.0, 2.0]]         #设定两个类别的中心
clusters_std = [1.5, 1]             #设定两个类别的标准差，通常来说，样本量比较大的类别会更加松散
X, y = make_blobs(n_samples= [class_1, class_2],
                  centers= centers,
                  cluster_std= clusters_std,
                  random_state= 42, shuffle= False)
# 画图看数据集，其中红色点是少数类，紫色点是多数类
plt.scatter(X[:, 0], X[:, 1], c = y, cmap = "rainbow",s = 10)
# 查看不平衡的样本数量
pd.DataFrame(y).value_counts()
# SMOTE过采样
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state = 42, sampling_strategy= 0.5)
X_sm, Y_sm = smote.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_sm).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_sm[:, 0], X_sm[:, 1], c = Y_sm, cmap = "rainbow",s = 10)
# Random欠采样
from imblearn.under_sampling import RandomUnderSampler

rus= RandomUnderSampler(sampling_strategy=0.3, random_state= 42)
X_rus, Y_rus = rus.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_rus).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_rus[:, 0], X_rus[:, 1], c = Y_rus, cmap = "rainbow",s = 10)
# TomekLinks欠采样
from imblearn.under_sampling import TomekLinks

tl= TomekLinks()
X_tl, Y_tl= tl.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_tl).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_tl[:, 0], X_tl[:, 1], c = Y_tl, cmap = "rainbow",s = 10)
# ENN欠采样
from imblearn.under_sampling import EditedNearestNeighbours

enn= EditedNearestNeighbours(n_neighbors= 20)  # 改变n_neighbors=3 参数以观察欠采样结果
X_enn, Y_enn= enn.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_enn).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_enn[:, 0], X_enn[:, 1], c = Y_enn, cmap = "rainbow",s = 10)
# SMOTE叠加TomekLink
from imblearn.combine import SMOTETomek

smote_tomek = SMOTETomek(random_state= 42)
X_smote_tomek, Y_smote_tomek= smote_tomek.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_smote_tomek).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_smote_tomek[:, 0], X_smote_tomek[:, 1], c = Y_smote_tomek, cmap = "rainbow",s = 10)
# SMOTE叠加ENN
from imblearn.combine import SMOTEENN

smote_enn = SMOTEENN(random_state= 42)
X_smote_enn, Y_smote_enn= smote_enn.fit_resample(X, y)

# 查看采样后的比例
pd.DataFrame(Y_smote_enn).value_counts()

# 画图看过采样后的数据集
plt.scatter(X_smote_enn[:, 0], X_smote_enn[:, 1], c = Y_smote_enn, cmap = "rainbow",s = 10)
# 读取数据
raw_data= pd.read_csv('train_set.csv')
raw_data.info()
df_features= raw_data.drop(['ID'], axis=1)
df= df_features.dropna().reset_index(drop= True)  # 缺失值
labels= df.pop("y")  # 分割标签
cat_cols= df.select_dtypes(include= ["object"])   # 分类型
num_cols= df.select_dtypes(exclude= ["object"])   # 数值型
# 数据编码
from sklearn.preprocessing import OrdinalEncoder
encoder= OrdinalEncoder()
cat_trans= encoder.fit_transform(cat_cols)
df_cat= pd.DataFrame(cat_trans, columns= cat_cols.columns)
# 数据合并
data= pd.concat([df_cat, num_cols], axis=1)
# 分割测试集
from sklearn.model_selection  import train_test_split
Xtrain, Xtest, Ytrain, Ytest= train_test_split(data, labels, test_size= 0.3, stratify= labels, random_state= 42)
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

train = xgb.DMatrix(data= Xtrain, label= Ytrain)
XGB= xgb.train(params= {}, dtrain= train)

test = xgb.DMatrix(data= Xtest)
print(classification_report(Ytest, XGB.predict(test)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
# SMOTE
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state = 42)
X_sm, Y_sm = smote.fit_resample(Xtrain, Ytrain)

# 查看采样后的比例
pd.DataFrame(Y_sm).value_counts()
train_sm = xgb.DMatrix(data= X_sm, label= Y_sm)
XGB= xgb.train(params= {}, dtrain= train_sm)

test_sm = xgb.DMatrix(data= Xtest)
print(classification_report(Ytest, XGB.predict(test_sm)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test_sm)))
# 思考：上述过采样得到的数据，是否有问题
# SMOTENC
from imblearn.over_sampling import SMOTENC

smote_nc= SMOTENC(categorical_features= list(cat_cols.columns))
X_smnc, Y_smnc = smote_nc.fit_resample(Xtrain, Ytrain)

# 查看采样后的比例
pd.DataFrame(Y_smnc).value_counts()
train_smnc = xgb.DMatrix(data= X_smnc, label= Y_smnc)
XGB= xgb.train(params= {}, dtrain= train_smnc)

print(classification_report(Ytest, XGB.predict(test_sm)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test_sm)))
weight= Ytrain.value_counts()[0] / Ytrain.value_counts()[1]

params= {'scale_pos_weight': weight, 'eval_metric': 'auc'}

XGB= xgb.train(params= params, dtrain= train)

print(classification_report(Ytest, XGB.predict(test)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
params= {'max_delta_step': 0.6, 'eval_metric': 'auc'}

XGB= xgb.train(params= params, dtrain= train)

print(classification_report(Ytest, XGB.predict(test)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))



"""5.2&3 pipeline_保险案例
原素材: 5 预测类算法的参数调优\5.2&3 pipeline_保险案例.ipynb
"""

# 导入所有的库
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")
# 导入数据，拆分标签
df= pd.read_csv('保险数据_第一期.csv')

labels= df.pop('resp_flag')   # 取出y
# 数据类型区分
cat_cols= df.select_dtypes(include=["object"])   # 分类型变量
num_cols= df.select_dtypes(exclude=["object"])   # 数值型变量
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
# 分类型数据
cat_imp= SimpleImputer(strategy='most_frequent')   # 缺失值
cat_encode= OrdinalEncoder()   # 数据编码
cat_pipe= Pipeline(steps= [('cat_imp', cat_imp), ('cat_encode', cat_encode)])

# 数值型数据
num_imp= SimpleImputer(strategy='mean')   # 缺失值

# ColumnTransformer，List of (name, transformer, columns) tuples
col_trans= ColumnTransformer(transformers= [('cat_pipe', cat_pipe, cat_cols.columns),
                                            ('num_imp', num_imp, num_cols.columns)])
# 测试
col_trans.fit_transform(df)
# pipeline，List of (name, transform) tuples
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

lr_pipe= Pipeline(steps= [('col_trans', col_trans), ('lr', lr)])
# 分割测试集
from sklearn.model_selection  import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(df, labels, test_size=0.3, stratify=labels, random_state= 42)
# 测试
lr_pipe.fit(Xtrain, Ytrain)
lr_pipe.score(Xtest, Ytest)
# 网格搜索，使用<estimator>__<parameter>访问每个transform内部的参数
from sklearn.model_selection import GridSearchCV

# 参数字典
param= dict(lr__C= np.arange(1, 2, 0.1),
           lr__class_weight= [None, "balanced"],
           col_trans__num_imp__strategy= ['mean', 'median'])

grid_lr= GridSearchCV(lr_pipe, param, cv= 3, n_jobs= -1)
grid_lr.fit(Xtrain, Ytrain)
grid_lr.best_params_
# 模型评估
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

print(classification_report(Ytest, grid_lr.predict(Xtest)))
print("AUC: ", roc_auc_score(Ytest, grid_lr.predict_proba(Xtest)[:, 1]))
print(classification_report(Ytrain, grid_lr.predict(Xtrain)))
print("AUC: ", roc_auc_score(Ytrain, grid_lr.predict_proba(Xtrain)[:, 1]))
# 保存模型
import joblib
joblib.dump(grid_lr, "model_20241222.joblib")
# 预测新进用户
df_new= pd.read_csv("保险案例_新进用户.csv")
df_new
grid_lr.predict(df_new)
# 作业：继续做特征工程，包括加入数据标准化，模型换成决策树并调参，以实现更好的模型结果


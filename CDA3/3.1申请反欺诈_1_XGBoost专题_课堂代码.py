"""1_XGBoost专题_课堂代码
原素材: 3.1申请反欺诈（决策树系列等）\进阶内容_组合算法最近特性和模型解释\1_XGBoost专题_课堂代码.ipynb
"""

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection  import train_test_split
import xgboost as xgb
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# 读入数据
raw_data= pd.read_csv('保险数据_第一期.csv')
# 缺失值(缺失值占比很少，直接删除)
df= raw_data.dropna().reset_index(drop=True)
# 分割标签
labels= df.pop("resp_flag")
# 数据类型拆分
cat_cols= df.select_dtypes(include= ["object"])   # 分类型
num_cols= df.select_dtypes(exclude= ["object"])   # 数值型
# 数据编码
encoder= OrdinalEncoder()
cat_trans= encoder.fit_transform(cat_cols)
df_cat= pd.DataFrame(cat_trans, columns= cat_cols.columns)
# 数据合并
data= pd.concat([df_cat, num_cols], axis=1)
# 分割测试集
Xtrain, Xtest, Ytrain, Ytest= train_test_split(data, labels, test_size= 0.3, stratify= labels, random_state= 42)
# sklearn接口
from xgboost.sklearn import XGBClassifier
XGB= XGBClassifier()
XGB.fit(Xtrain, Ytrain)

print("AUC: ", roc_auc_score(Ytest, XGB.predict_proba(Xtest)[:, 1]))
# xgb接口，必须传入专属格式的数据
import xgboost as xgb

train= xgb.DMatrix(data= Xtrain, label= Ytrain)
XGB= xgb.train(params= {}, dtrain= train)

test= xgb.DMatrix(data= Xtest)
print(classification_report(Ytest, XGB.predict(test)>0.5))
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
# 参数设置
param= {'max_depth': 5, 'eta': 0.4}
param['eval_metric'] = 'auc'

XGB= xgb.train(params= param, dtrain= train, evals= [(train, 'train')], num_boost_round= 15)
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
evals=None   计算评估指标的数据集
early_stopping_rounds=None   提前停止。int。连续多少次指标没有改进，则返回上次迭代的模型
# 提前停止
Xtrain1, Xtest1, Ytrain1, Ytest1= train_test_split(Xtrain, Ytrain, test_size= 0.3, stratify= Ytrain, random_state= 42)

train_e= xgb.DMatrix(data= Xtrain1, label= Ytrain1)
test_e= xgb.DMatrix(data= Xtest1, label= Ytest1)

# 参数设置
param= {'max_depth': 5, 'eta': 0.4}
param['eval_metric'] = 'auc'

eval_list= [(train_e, 'train_e'), (test_e, 'test_e')]   # 只有最后一个数据集用来计算early stop

XGB= xgb.train(params= param, dtrain= train_e, evals= eval_list, 
               num_boost_round= 15, early_stopping_rounds= 3)
param
# 单调约束
params_monotonic= param.copy()
params_monotonic['tree_method']= 'exact'
params_monotonic['monotone_constraints']= (0, 1, -1)   # 前三个特征分别：不设约束，单调增，单调减

XGB= xgb.train(params= params_monotonic, dtrain= train, evals= [(train, 'train')])
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
# 交互约束
params_interaction= param.copy()
params_interaction['interaction_constraints']= '[[0, 2], [1, 3, 4], [5, 6]]'

XGB= xgb.train(params= params_interaction, dtrain= train, evals= [(train, 'train')])
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))
# 随机森林
params_rf= {
          "colsample_bynode": 0.8,   # colsample类型的参数设置任何一个即可，必须小于1
          "learning_rate": 1,   # 必须设为1
          "num_parallel_tree": 100,   # 森林中树的数量
          "subsample": 0.8,   # 必须小于1
            }

XGB= xgb.train(params= params_rf, dtrain= train, evals= [(train, 'train')], num_boost_round= 1)   # 迭代次数必须设为1，否则会生成多个森林
print("AUC: ", roc_auc_score(Ytest, XGB.predict(test)))

"""3_模型解释性专题_课堂代码
原素材: 3.1申请反欺诈（决策树系列等）\进阶内容_组合算法最近特性和模型解释\3_模型解释性专题_课堂代码.ipynb
"""

# !pip install shap
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection  import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
import statsmodels.api as sm
Xtrain_lr= Xtrain.copy()
Xtrain_lr["const"]= 1

LR= sm.Logit(Ytrain, Xtrain_lr).fit()
LR.summary()
from sklearn.tree import DecisionTreeClassifier
dt= DecisionTreeClassifier()
dt.fit(Xtrain, Ytrain)

dt.feature_importances_
from sklearn.ensemble import RandomForestClassifier
rf= RandomForestClassifier(oob_score= True, n_jobs= -1)
rf.fit(Xtrain, Ytrain)

rf.feature_importances_
import xgboost as xgb

train= xgb.DMatrix(data= Xtrain, label= Ytrain)
XGB= xgb.train(params= {}, dtrain= train)
XGB.get_score(importance_type= 'weight')
import lightgbm

train= lightgbm.Dataset(Xtrain, label= Ytrain)
lgb = lightgbm.train(params={}, train_set= train)
lgb.feature_importance(importance_type= 'split')
# 在SHAP中进行模型解释需要先创建一个explainer，SHAP支持很多类型的explainer(例如deep, gradient, kernel, linear, tree, sampling)
import shap
explainer = shap.Explainer(XGB)
shap_values = explainer(Xtrain)
shap_values
# 查看特征重要性
shap.plots.bar(shap_values, max_display=10)
# 查看某个样本预测值的特征贡献
shap.plots.bar(shap_values[1], max_display=10)
# 查看全体样本的特征贡献（蜂群图）
shap.plots.beeswarm(shap_values)
# 单个特征的偏依赖图
from sklearn.inspection import PartialDependenceDisplay
PartialDependenceDisplay.from_estimator(
    estimator=rf,
    X=Xtrain,
    features=['GEND','BANK','age','meda'],
    subsample=1000    # 样本采样数量
)
# 偏依赖的数值计算（计算复杂度高，建议每次只计算一个特征）
from sklearn.inspection import partial_dependence
partial_dependence(
    estimator=rf,
    X=Xtrain,
    features=['age'],  # 'GEND','BANK','meda',
)
# 简单的决策树可以直接使用sklearn+matplotlib可视化（示例展示）
from sklearn.datasets import load_iris
data = load_iris()
X, y = data.data, data.target
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

from sklearn.tree import plot_tree
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=data.feature_names, class_names=data.target_names, filled=True)
plt.show()
# 对于更加复杂的决策树，可视化树很难判断具体决策路径，因此我们引入一个新的方法
# 需要分析决策路径的预测样本
sample= np.array(Xtest.loc[1])

# 获取决策路径
node_indicator= dt.decision_path(sample.reshape(1, -1))
node_index= node_indicator.indices

# 获取树的分裂特征和阈值（-2表示叶节点）
feature= dt.tree_.feature
threshold= dt.tree_.threshold
# 打印样本的详细决策路径
print("决策路径:")
for node_id in node_index:
    if feature[node_id] != -2:  # 非叶节点
        feature_name = dt.feature_names_in_[feature[node_id]]
        threshold_value = threshold[node_id]
        sample_value = sample[feature[node_id]]
        print(f"节点 {node_id}: 如果 {feature_name} <= {threshold_value:.2f} (样本值: {sample_value:.2f})")
    else:
        print(f"叶节点 {node_id}: 预测结果 = {dt.classes_[dt.tree_.value[node_id].argmax()]}")
# 训练一个只有5棵树的森林，方便演示
rf_clf= RandomForestClassifier(n_estimators=5, n_jobs= -1).fit(Xtrain, Ytrain)

for i, tree in enumerate(rf_clf.estimators_):
    print(f"第 {i+1} 棵树的决策路径:")
    # 获取决策路径
    node_indicator = tree.decision_path(sample.reshape(1, -1))
    node_index = node_indicator.indices

    # 获取树的分裂特征和阈值
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold

    for node_id in node_index:
        if feature[node_id] != -2:  # 非叶节点
            feature_name = rf_clf.feature_names_in_[feature[node_id]]
            threshold_value = threshold[node_id]
            sample_value = sample[feature[node_id]]
            print(f"  节点 {node_id}: 如果 {feature_name} <= {threshold_value:.2f} (样本值: {sample_value:.2f})")
        else:
            leaf_value = tree.tree_.value[node_id]
            print(f"  叶节点 {node_id}: 分类结果 = {np.argmax(leaf_value)}, 节点值 = {leaf_value}\n")
# 取重要性前5的特征，重新训练一棵简单的决策树
feature_importance= pd.DataFrame({'Feature':dt.feature_names_in_, 'Importance':dt.feature_importances_})
feature_sort= feature_importance.sort_values(by='Importance', ascending=False)

Xtrain_rule= Xtrain[feature_sort.head(5)['Feature']]

dt_rule= DecisionTreeClassifier(max_depth=5).fit(Xtrain_rule, Ytrain)
# 提取规则
from sklearn.tree import export_text

rules = export_text(dt_rule, feature_names= dt_rule.feature_names_in_.tolist())
print(rules)
# 若决策树足够简单，也可以通过可视化图来提取规则
plt.figure(figsize=(12, 8))
plot_tree(dt_rule, feature_names=dt_rule.feature_names_in_.tolist(), class_names=['0','1'], filled=True)
plt.show()
# 注意：安装此库会将pandas的版本自动降为1.5，需要手动回退，请谨慎安装
# !pip install dice_ml
import dice_ml
train_dataset= pd.concat([Xtrain, Ytrain], axis=1)

# 生成dice专用格式的数据集
d = dice_ml.Data(dataframe=train_dataset, continuous_features=num_cols.columns.tolist(), outcome_name='resp_flag')

# 将模型导入dice
m = dice_ml.Model(model=dt, backend="sklearn")

# 创建解释器
exp = dice_ml.Dice(d, m, method="random")
# 生成反事实样本
e1 = exp.generate_counterfactuals(Xtest[0:1], total_CFs=4, desired_class="opposite", random_seed=42)
e1.visualize_as_dataframe(show_only_changes=True)


"""2.2逻辑回归
原素材: 2.2用户响应预测（逻辑回归）\2.2逻辑回归.ipynb
"""

%matplotlib inline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

pd.set_option('display.max_columns', 8)
data = pd.read_csv(r'creditcard_exp.csv', skipinitialspace=True)
data.head()
oos_data = pd.read_csv(r'creditcard_exp_out_of_sample.csv', skipinitialspace=True)
oos_data.head()
data = data.drop('avg_exp', axis=1)\
           .drop('avg_exp_ln', axis=1)\
           .drop('age2', axis=1)
oos_data = oos_data.drop('age2', axis=1)
oos_data['edu_class'].replace({0: 1}, inplace=False)
train = data.sample(frac=0.7, random_state=1234).copy()
test = data[~ data.index.isin(train.index)].copy()
print(' 训练集样本量: %i \n 测试集样本量: %i' %(len(train), len(test)))
lr_model = smf.logit(
    formula='Acc ~ Income ', 
    data=train, 
#     family=sm.families.Binomial(sm.families.links.logit)
).fit()
lr_model.summary()
test['Pred_Acc'] = lr_model.predict(test)
print(test['Pred_Acc'].head())
#  不同阈值下的模型评估

for i in np.arange(0.1, 1, 0.2):
    prediction = (test['Pred_Acc'] > i).astype('int')
    confusion_matrix = pd.crosstab(prediction,test['Acc'],
                                   margins=True)
    precision = confusion_matrix.iloc[0, 0] /confusion_matrix.loc['All', 0]
    recall = confusion_matrix.iloc[0, 0] / confusion_matrix.loc[0, 'All']
    Specificity = confusion_matrix.iloc[1, 1] /confusion_matrix.loc[1,'All']
    f1_score = 2 * (precision * recall) / (precision + recall)
    print('Threshold: %.2f' %(i))
    print('Precision: %.2f, Recall:%.2f ,Specificity:%.2f ,f1_score:%.2f \n' \
          %(precision, recall, Specificity,f1_score))
y_col = 'Acc'
x_col_continuous = ['Age', 'Income', 'dist_home_val', 'dist_avg_income', 'high_avg']
x_col_discrete = ['gender', 'Ownrent', 'Selfempl', 'edu_class']
x_col_all = x_col_continuous + x_col_discrete
#  连续变量标准化
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
train[x_col_continuous] = scaler.fit(train[x_col_continuous])\
                                .transform(train[x_col_continuous])

#  对测试集连续变量做同样的标准化
test[x_col_continuous]  = scaler.transform(test[x_col_continuous])
oos_data[x_col_continuous] = scaler.transform(oos_data[x_col_continuous])
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()
lr.fit(train[x_col_all], train[y_col])

# 打印测试集预测结果
print('Prediction of test: ')
print(lr.predict(test[x_col_all]))
# 打印测试集预测概率
print('Probability of test: ')
print(lr.predict_proba(test[x_col_all]))
from sklearn.feature_selection import RFECV

rfecv = RFECV(lr, cv=3, scoring="accuracy",n_jobs=-1)
rfecv.fit(train[x_col_all], train[y_col])

# RFECV.support_返回保留下来的特征的mask
selected_cols = np.array(x_col_all)[rfecv.support_]

print('Ranking of columns: ', rfecv.ranking_)
print('Selected columns: ', selected_cols)
from sklearn.linear_model import LogisticRegressionCV

 # Cs为正则化系数的倒数
lrcv = LogisticRegressionCV(Cs=10, cv=4, n_jobs=-1)  
lrcv.fit(train[selected_cols], train[y_col])
print('Regulation strength: ', lrcv.C_)  # 模型交叉验证分数最高的C值
#  预测标签
train_prediction = lrcv.predict(train[selected_cols])
test_prediction = lrcv.predict(test[selected_cols])

#  预测概率分值
train_proba = lrcv.predict_proba(train[selected_cols])[:,1]
test_proba = lrcv.predict_proba(test[selected_cols])[:,1]
from sklearn.metrics import roc_curve, classification_report, auc

print(classification_report(test['Acc'], test_prediction))  # 计算评估指标
#  生成TPR和FPR
fpr_test, tpr_test, th_test = roc_curve(test['Acc'], test_proba)
fpr_train, tpr_train, th_train = roc_curve(train['Acc'], train_proba)

#  绘制ROC曲线
fig, ax = plt.subplots(figsize=[5, 5])
ax.set_xlabel('FPR',  fontsize=15)
ax.set_ylabel('TPR',  fontsize=15)
ax.plot(fpr_test, tpr_test, 'b-')
ax.plot(fpr_train, tpr_train, 'r-')
plt.title('ROC curve', fontsize=20)
plt.show()

#  打印AUC
print('AUC on test = %6.4f' % auc(fpr_test, tpr_test))
oos_data.head()
output_data_dir = './data_processed'
if not os.path.exists(output_data_dir):
    os.mkdir(output_data_dir)
output_data_path = os.path.join(output_data_dir,
                               'creditcard_exp_logistic_regression.csv')

oos_data['Pred_Acc'] = lrcv.predict_proba(oos_data[selected_cols])[:,1]
oos_data.to_csv(output_data_path, index=False)
import joblib

output_dir = "./model"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    
save_path = os.path.join(output_dir, "creditcard_logisticRegression.model")

# 模型持久化
joblib.dump(lrcv, save_path)
# 读取模型
model_reload = joblib.load(save_path)
model_reload.predict(oos_data[selected_cols])



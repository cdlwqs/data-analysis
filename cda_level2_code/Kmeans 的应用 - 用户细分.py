# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第9章-用户分群\k-means聚类")
"""
第9章 用户分群 —— K-means 用户细分（银行客户）
================================================
项目内涵：银行客户按交易行为(柜台/ATM/POS/信用卡次数)细分。先用 PCA+因子分析降维去相关，
         再 K-means 聚类；因变量偏态严重，用 QuantileTransformer 做正态转换后再次聚类，
         最后用决策树做聚类事后解释。
技术方法：preprocessing.scale、PCA、fa_kit 因子分析(varimax)、KMeans、
         QuantileTransformer(正态转换)、DecisionTreeClassifier 事后解释、export_graphviz。
数据源：profile_bank.csv（银行客户 4 类交易次数 CNT_TBM/CNT_ATM/CNT_POS/CNT_CSC）。
关键步骤：1)标准化+PCA 看主成分数 → 2)fa_kit 因子分析得 3 因子(ATM_POS/TBM/CSC)
         → 3)查偏度 → 4)K-means 聚 3 类 → 5)QuantileTransformer 正态转换后再聚类
         → 6)决策树事后分析(可视化各簇特征)。
依赖：fa_kit、pydotplus。
"""

# 该银行交易行为数据有四个特征，分别表示去柜台服务、使用 Atm、刷 pos 机和信用卡的次数。
# 1、导入数据
import pandas as pd
model_data = pd.read_csv("profile_bank.csv")
data = model_data.loc[ :,'CNT_TBM':'CNT_CSC']
data.head()


# - 2、查看相关系数矩阵，判定做变量降维的必要性（非必须）
corr_matrix = data.corr(method='pearson')
#corr_matrix = corr_matrix.abs()
corr_matrix


# - 3、做主成分之前，进行中心标准化
from sklearn import preprocessing
data = preprocessing.scale(data)


# - 4、使用 sklearn的主成分分析，用于判断保留主成分的数量
from sklearn.decomposition import PCA
pca=PCA(n_components=3)
newData=pca.fit(data)
print(pca.explained_variance_)
print(pca.explained_variance_ratio_)


# - 1、导入包，并对输入的数据进行主成分提取。为保险起见，data需要进行中心标准化
from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting
fa = FactorAnalysis.load_data_samples(data,preproc_demean=True,preproc_scale=True)
fa.extract_components()



# - 2、设定提取主成分的方式。默认为“broken_stick”方法，建议使用“top_n”法
fa.find_comps_to_retain(method='top_n',num_keep=3)


# - 3、通过最大方差法进行因子旋转
fa.rotate_components(method='varimax')
fa_plotting.graph_summary(fa)


# - 4、获取因子得分
pd.DataFrame(fa.comps["rot"])


score=fa.get_component_scores(data)
score=pd.DataFrame(score)



fa_scores=score.rename(columns={0: "ATM_POS", 1: "TBM",2: "CSC"})


fa_scores.head()


# - 识别异常


# - 1、查看变量的偏度
var = ["ATM_POS","TBM","CSC"]
skew_var = {}
for i in var:
    skew_var[i]=abs(fa_scores[i].skew())
skew=pd.Series(skew_var).sort_values(ascending=False)
skew


# - 2、进行 k-means聚类
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3) #MiniBatchKMeans()分批处理
#kmeans = cluster.KMeans(n_clusters=3, init='random', n_init=1)
result=kmeans.fit(fa_scores)
#print(result)


# - 3、对分类结果进行解读
model_data_l=model_data.join(pd.DataFrame(result.
labels_))
model_data_l=model_data_l.rename(columns={0: "clustor"})
model_data_l.head()


import matplotlib
try:
    get_ipython().magic("matplotlib inline")
except Exception:
    matplotlib.use("Agg")
model_data_l.clustor.value_counts().plot(kind = "pie")


# - 用户细分


# - 1、进行变量分布的正态转换
import numpy as np
from sklearn import preprocessing


quantile_transformer = preprocessing.QuantileTransformer(output_distribution='normal', random_state=0)
fa_scores_trans=quantile_transformer.fit_transform(fa_scores)
fa_scores_trans=pd.DataFrame(fa_scores_trans)


fa_scores_trans=fa_scores_trans.rename(columns={0: "ATM_POS", 1: "TBM", 2: "CSC"})


# 查看变量的偏度
var = ["ATM_POS","TBM","CSC"]
skew_var = {}
for i in var:
    skew_var[i]=abs(fa_scores_trans[i].skew())
skew=pd.Series(skew_var).sort_values(ascending=False)
skew


# - 2、进行 k-means聚类
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3) #MiniBatchKMeans()分批处理
#kmeans = cluster.KMeans(n_clusters=3, init='random', n_init=1)
result=kmeans.fit(fa_scores_trans)
#print(result)


# - 3、对分类结果进行解读
model_data_l=model_data.join(pd.DataFrame(result.
labels_))
model_data_l=model_data_l.rename(columns={0: "clustor"})
model_data_l.head()


model_data_l.clustor.value_counts()


#聚类事后分析
from sklearn import tree
clf=tree.DecisionTreeClassifier(criterion='gini',max_depth=3, min_samples_split=100, min_samples_leaf=100,random_state=12345)
# 当前支持计算信息增益和 GINI
clf.fit(model_data, result.labels_)


import pydotplus
try:
    from IPython.display import Image
except Exception:
    Image = None
import sklearn.tree as tree
dot_data = tree.export_graphviz(clf,out_file=None,feature_names=model_data.columns,class_names=["0","1","2"],filled=True)
try:
    graph = pydotplus.graph_from_dot_data(dot_data)
    if Image is not None:
        Image(graph.create_png())
    else:
        graph.write_png("kmeans_decision_tree.png")
        print("决策树图已保存为 kmeans_decision_tree.png")
except Exception as _e:
    print("决策树图形渲染跳过(需安装 GraphViz):", _e)
    with open("kmeans_decision_tree.dot", "w") as _f:
        _f.write(dot_data)
    print("决策树 dot 文本已保存为 kmeans_decision_tree.dot")



# ============================================================
# 【运行结果】成功
# ============================================================
#
# 第9章 用户分群 —— K-means 用户细分（银行客户）
# ================================================
# 项目内涵：银行客户按交易行为(柜台/ATM/POS/信用卡次数)细分。先用 PCA+因子分析降维去相关，
#          再 K-means 聚类；因变量偏态严重，用 QuantileTransformer 做正态转换后再次聚类，
#          最后用决策树做聚类事后解释。
# 技术方法：preprocessing.scale、PCA、fa_kit 因子分析(varimax)、KMeans、
#          QuantileTransformer(正态转换)、DecisionTreeClassifier 事后解释、export_graphviz。
# 数据源：profile_bank.csv（银行客户 4 类交易次数 CNT_TBM/CNT_ATM/CNT_POS/CNT_CSC）。
# 关键步骤：1)标准化+PCA 看主成分数 → 2)fa_kit 因子分析得 3 因子(ATM_POS/TBM/CSC)
#          → 3)查偏度 → 4)K-means 聚 3 类 → 5)QuantileTransformer 正态转换后再聚类
#          → 6)决策树事后分析(可视化各簇特征)。
# 依赖：fa_kit、pydotplus。
#
#    CNT_TBM  CNT_ATM  CNT_POS  CNT_CSC
# 0       34        3        3        9
# 1       44       17        5       18
# 2      122       26       32       36
# 3       42        3        6        1
# 4       20       15        2        2
#           CNT_TBM   CNT_ATM   CNT_POS   CNT_CSC
# CNT_TBM  1.000000  0.055648  0.083624  0.198835
# CNT_ATM  0.055648  1.000000  0.341161  0.242106
# CNT_POS  0.083624  0.341161  1.000000  0.234055
# CNT_CSC  0.198835  0.242106  0.234055  1.000000
# [1.60786876 1.00252275 0.7339482 ]
# [0.40196317 0.25062818 0.18348521]
# None
# [0 1 2]
# None
# Figure(800x1200)
#           0         1         2
# 0  0.004039  0.992900  0.007811
# 1  0.671476 -0.090569  0.100081
# 2  0.741002  0.076706 -0.084707
# 3 -0.004504  0.007874  0.991336
#     ATM_POS       TBM       CSC
# 0 -0.852354 -0.294938  0.143935
# 1 -0.333078 -0.244334  0.939343
# 2  0.918067  0.593787  2.349496
# 3 -0.741847 -0.210507 -0.521592
# 4 -0.499703 -0.492714 -0.367629
# TBM        51.881233
# CSC         6.093417
# ATM_POS     2.097633
# dtype: float64
#       ID  CNT_TBM  CNT_ATM  CNT_POS  CNT_CSC  CNT_TOT  clustor
# 0  41360       34        3        3        9       49        0
# 1  52094       44       17        5       18       84        0
# 2  57340      122       26       32       36      216        1
# 3  76885       42        3        6        1       52        0
# 4  89150       20       15        2        2       39        0
# TBM        0.012075
# ATM_POS    0.011758
# CSC        0.007694
# dtype: float64
#       ID  CNT_TBM  CNT_ATM  CNT_POS  CNT_CSC  CNT_TOT  clustor
# 0  41360       34        3        3        9       49        1
# 1  52094       44       17        5       18       84        1
# 2  57340      122       26       32       36      216        1
# 3  76885       42        3        6        1       52        2
# 4  89150       20       15        2        2       39        2
# clustor
# 2    35592
# 1    34448
# 0    29960
# Name: count, dtype: int64
# DecisionTreeClassifier(max_depth=3, min_samples_leaf=100, min_samples_split=100,
#                        random_state=12345)
# 决策树图形渲染跳过(需安装 GraphViz): GraphViz's executables not found
# 决策树 dot 文本已保存为 kmeans_decision_tree.dot

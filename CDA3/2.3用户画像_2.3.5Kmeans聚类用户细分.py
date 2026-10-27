"""2.3.5Kmeans聚类用户细分
原素材: 2.3用户画像（主成分、因子分析、变量聚类、层次聚类、kmeans聚类）\2.3.5Kmeans聚类用户细分.ipynb
"""

%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option("display.max_columns",7)  # 为方便截图设置最大显示列数为7

customer = pd.read_csv('data_clust.csv',skipinitialspace=True)
customer.describe(include='all')
customer.head()
for col in customer.columns:
    if customer[col].hasnans:
        print(col)
fill_cols = ['interested_travel', 'computer_owner', 'HH_adults_num']
fill_values = {col: customer[col].mode()[0] for col in fill_cols}

customer = customer.fillna(fill_values)
customer['interested_reading'].value_counts(dropna=False)
customer['HH_has_children'] = customer['HH_has_children']\
    .replace({'N':0, 'Y':1, np.NaN:0})
    
customer['interested_reading'] = customer['interested_reading']\
    .replace({'.':'0'}).astype('int')
from itertools import combinations
from scipy import stats

_cols = [
    'interested_travel',
    'computer_owner',
    'marital',
    'interested_golf', 
    'interested_gambling', 
    'HH_has_children',
    'interested_reading'
]

sample = customer[_cols].sample(3000, random_state=12345)

for colA, colB in combinations(_cols, 2):
    crosstab = pd.crosstab(sample[colA], sample[colB])
    pval = stats.chi2_contingency(crosstab)[1]
    if pval > 0.05:
        print('p-value = %0.3f between "%s" and "%s"' %(pval, colA, colB))
from sklearn.preprocessing import Binarizer

# 二值化
binarizer = Binarizer(threshold=1.5)
customer['interested_reading'] = binarizer.fit_transform(
    customer[['interested_reading']])
# 生成偏好填充率
interest =[
    'interested_travel',
    'computer_owner',
    'interested_golf', 
    'interested_gambling',
    'interested_reading'
]
n_ = len(interest)

customer = customer.drop(interest, axis=1)\
               .assign(interest=customer[interest].sum(axis=1) / n_)

customer.head()
# 所有变量划分为连续、有序分类和离散，以便后续处理
continuous_cols = ['age', 'home_value', 'risk_score', 'interested_sport', 
                   'HH_dieting', 'auto_member', 'HH_grandparent',
                   'HH_head_age', 'loan_ratio']

categorical_cols = ['marital', 'interest', 'HH_adults_num']

discreate_cols = ['HH_has_children']
customer[continuous_cols].hist(bins=25, figsize=[8, 8])
plt.show()
from sklearn.preprocessing import QuantileTransformer

qt = QuantileTransformer(n_quantiles=100, output_distribution='normal')
qt_data = qt.fit_transform(customer[continuous_cols])

pd.DataFrame(qt_data, columns=continuous_cols).hist(bins=25, figsize=[8, 8])
plt.show()
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scale_data = scaler.fit_transform(customer[categorical_cols])
data = np.hstack([qt_data, scale_data, customer[discreate_cols]])
data = pd.DataFrame(
    data, columns=continuous_cols + categorical_cols + discreate_cols)
data.head()
household = ['age', 'marital', 'HH_adults_num', 'home_value', 
             'risk_score', 'HH_grandparent', 'HH_head_age', 'loan_ratio']
hobby = ['HH_dieting', 'auto_member','interest', 'interested_sport']
#  'HH_has_children' 暂不进入模型 
data[hobby].corr()
data[household].to_numpy()
from sklearn.decomposition import PCA

pca_hh = PCA().fit(data[household])
pca_hh.explained_variance_ratio_.cumsum()
from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting
fa_hh = FactorAnalysis.load_data_samples(
    data[household].to_numpy(),
    preproc_demean=True,
    preproc_scale=True
)
fa_hh.extract_components()
fa_hh.find_comps_to_retain(method='top_n',num_keep=4)
fa_hh.rotate_components(method='varimax')
fa_plotting.graph_summary(fa_hh)
print(pd.DataFrame(fa_hh.comps['rot'], index=household))
data_hh = pd.DataFrame(
    np.dot(data[household], fa_hh.comps['rot']), 
    columns=['life_circle','finance', 'HH_size', 'risk']
)
fa_hb = FactorAnalysis.load_data_samples(
    data[hobby].to_numpy(), 
    preproc_demean=True,
    preproc_scale=True
)

fa_hb.extract_components()

fa_hb.find_comps_to_retain(method='top_n', num_keep=3)
fa_hb.rotate_components(method='varimax')
print(pd.DataFrame(fa_hb.comps['rot'], index=hobby))
data_hb = pd.DataFrame(
    np.dot(data[hobby], fa_hb.comps['rot']), 
    columns=['sports', 'health', 'leisure']
)
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_plot(data, k_range=range(2, 12), n_init=5, sample_size=2000, 
                 figsize=[9, 2]):
    scores = []  #  用来保存模型效果的评分
    models = {}  #  用字典来保存模型
    
    #  遍历选择的所有k
    for k in k_range:
        kmeans = KMeans(n_clusters=k, n_init=n_init)
        kmeans.fit(data)  # 训练
        models[k] = kmeans  
        sil = silhouette_score(data, kmeans.labels_, 
                               sample_size=sample_size)  # 轮廓系数
        scores.append([k, kmeans.inertia_, sil])  # inertia_即SSD

    scores_df = pd.DataFrame(scores, columns=['k','sum_square_dist', 'sil'])
    #  绘制簇内离差平方和
    plt.figure(figsize=figsize)
    plt.subplot(121, ylabel='SSD')
    plt.plot(scores_df.k, scores_df.sum_square_dist)
    #  绘制轮廓系数
    plt.subplot(122, ylabel='silhouette_score')
    plt.plot(scores_df.k, scores_df.sil)
    plt.show()
    
    return models  # 返回不同k值对应的模型
# 对因子得分进行标准化
hh_scaler = StandardScaler()
scale_data_hh = hh_scaler.fit_transform(data_hh)
hb_scaler = StandardScaler()
scale_data_hb = hb_scaler.fit_transform(data_hb)

# 绘制ssd、轮廓系数
models_hh = cluster_plot(scale_data_hh)
print("-" * 80)
models_hb = cluster_plot(scale_data_hb)
hh_labels = pd.DataFrame(models_hh[3].labels_, columns=['hh'])
hb_labels = pd.DataFrame(models_hb[2].labels_, columns=['hb'])
clusters = customer.join(hh_labels).join(hb_labels)
clusters.head()
from sklearn.tree import DecisionTreeClassifier
import pydotplus
from IPython.display import Image
import sklearn.tree as tree

# 建立决策树
tree_hh = DecisionTreeClassifier()
tree_hb = DecisionTreeClassifier()
tree_hh.fit(clusters[household], clusters['hh'])
tree_hb.fit(clusters[hobby], clusters['hb'])


# 对household的聚类标签绘制决策树
dot_hh = tree.export_graphviz(
    tree_hh,
    out_file=None, 
    feature_names=household, 
    class_names=True,
    max_depth=2, 
    filled=True
) 

graph_hh = pydotplus.graph_from_dot_data(dot_hh)  
Image(graph_hh.create_png()) 
dot_hb = tree.export_graphviz(
    tree_hb,
    out_file=None, 
    feature_names=hobby, 
    class_names=True,
    max_depth=2, 
    filled=True
) 

graph_hb = pydotplus.graph_from_dot_data(dot_hb)  
Image(graph_hb.create_png()) 
clusters
cluster_pt = pd.pivot_table(clusters, index='hh', columns='hb',
                            aggfunc='mean').T
cluster_pt.swaplevel('hb', 0).sort_index(level=0)


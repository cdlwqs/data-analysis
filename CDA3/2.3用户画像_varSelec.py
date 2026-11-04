
'''
基于SparsePCA的算法还不是很稳定,尤其是当数据本身保留几个变量都处于模棱两可的时候,
该算法并不能达到人为调整的效果。而且并不能保证每次保留的变量是一致的（原因1、SparsePCA：本身就具有随机性；2、脚本中也随机抽样的），
只能保证保留的变量是不相关的
其特点只是比较省人力，可以自动化运行
'''


from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.decomposition import SparsePCA


def var_select(orgdata, k, max_alpha=10, alpha_step=0.2):
    """
    orgdata-需要信息压缩的数据框
    k-预期最大需要保留的最大变量个数，实际保留数量不能多于这个数值
    max_alpha-SparsePCA算法惩罚项的最大值,一般要到5才会取得比较理想的结果
    alpha_step-SparsePCA算法惩罚项递增的步长
    """
    # 当数据量过大时，抽样计算
    if len(orgdata) > 5000:
        data = orgdata.sample(5000)
    else:
        data = orgdata

    data = preprocessing.scale(data)
    n_components = k

    # 进行SparsePCA，选择合适的惩罚项alpha，使得每个原始变量只在一个主成分上有权重
    for i in np.arange(0.1, max_alpha, alpha_step):
        pca_model = SparsePCA(n_components=n_components, alpha=i)
        pca_model.fit(data)
        pca = pd.DataFrame(pca_model.components_).T
        n = data.shape[1] - sum(sum(np.array(pca != 0)))  # 计算系数不为0的数量
        if n == 0:
            global best_alpha
            best_alpha = i
            break        
            
    # 计算稀疏主成分得分
    pca_model = SparsePCA(n_components=n_components, alpha=best_alpha)
    pca_model.fit(data)
    pca = pd.DataFrame(pca_model.components_).T
    data = pd.DataFrame(data)
    score = pd.DataFrame(pca_model.fit_transform(data))
    # 计算原始变量与主成分之间的1-R方值
    r = []
    R_square = []
    for xk in range(data.shape[1]):  # xk输入变量个数
        for paj in range(n_components):  # paj主成分个数
            r.append(abs(np.corrcoef(data.iloc[:, xk], score.iloc[:, paj])[0, 1]))
            r_max1 = max(r)
            r.remove(r_max1)
            r.append(-2)
            r_max2 = max(r)
            R_square.append((1 - r_max1 ** 2) / (1 - r_max2 ** 2))

    R_square = abs(pd.DataFrame(np.array(R_square).reshape((data.shape[1], n_components))))
    var_list = []

    # 每个主成分中，选出原始变量的1-R方值最小的。
    for i in range(n_components):
        vmin = R_square[i].min()
        var_list.append(R_square[R_square[i] == vmin][i].index)
    
    news_ids =[]
    for id in var_list:
        if id not in news_ids:
            news_ids.append(id)
    print(news_ids)
    data_vc = orgdata.iloc[:, np.array(news_ids).reshape(len(news_ids))]
    return data_vc
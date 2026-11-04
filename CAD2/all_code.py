# -*- coding: utf-8 -*-
"""
CDA 二级认证教材《量化策略分析》—— 全部代码与运行结果汇总
============================================================
本文件按章节顺序收录 13 个 .py 的原始代码，每章含：
  1) 章节标题与源文件路径
  2) 原始代码（原样保留，未做任何包裹/改动）
  3) 运行结果（以注释形式附在代码后）
注意：各章代码的相对数据路径基于其所在子目录，独立运行时请先 cd 到该目录。
运行环境: Python 3.10 + pandas/numpy/matplotlib/seaborn/
         sklearn/scipy/statsmodels/fa_kit/pydotplus
"""

# ================================================================
# 1. 第4章 数据整合与数据清洗（pandas）
# 源文件: 第4章- 数据处理(pandas)\第4章  数据整合和数据清洗.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第4章- 数据处理(pandas)
# ================================================================

# -*- coding: utf-8 -*-
"""
第4章 数据整合与数据清洗（pandas）
====================================
项目内涵：使用 pandas 完成数据从"读入"到"清洗"的完整预处理流程，是量化分析的
         数据底座。涵盖读取、行列操作、连接合并、分组汇总、重复/缺失/噪声值处理。
技术方法：read_csv/to_csv、iloc/loc、merge/join/concat、groupby/agg、pivot_table、
         盖帽法(cap)、pd.cut 分箱。
数据源：sample.csv、data/big.csv（分块读取演示）。
关键步骤：1)按列/按行/分块读取并写出 → 2)行列选择与条件查询 → 3)横向merge与纵向concat
         → 4)排序、分组汇总、透视表 → 5)重复值drop_duplicates、缺失值fillna、
         盖帽法去噪、等频/等距分箱。
"""

# 1.1.1读取数据


import pandas as pd
csv = pd.read_csv('sample.csv')
csv


csv = pd.read_csv('sample.csv',\
                   usecols=['id','name'],\
                   nrows=2) #读取'id'和'name'两列，仅读取前两行
csv


csvs = pd.read_csv('data/big.csv',chunksize=900)
for i in csvs:
    print (i.shape)


csvs = pd.read_csv('data/big.csv',chunksize=900)
dat = pd.concat(csvs,ignore_index=True)
dat.shape


csv = pd.read_csv('sample.csv',
                  na_values='99999')
csv


csv = pd.read_csv('sample.csv',
                  encoding='utf-8')
csv


csv.to_csv('write.csv',encoding='utf-8',index=False)


# 1.2.1 行列操作


import numpy as np
import pandas as pd
np.random.seed(0) #为保证代码每次运行都能得到相同的一组数据，设置随机数种子
sample = pd.DataFrame(np.random.randn(4,5)
                     ,columns=list("abcde")
                     )
sample


sample['a']


sample.iloc[:,0]


sample.loc[:,"a"]


sample[['a']]


sample.loc[:1,:"b"]


sample.iloc[0:2,0:2]


sample['new_col'] = sample['a'] - sample['b']
sample


sample.assign(new_col2 = sample['a'] - sample['b'],
                  new_col3 = sample['a'] + sample['b'])


sample.drop(columns='a')


sample.drop(columns=['a','b'])


# 1.2.2 条件查询


sample =pd.DataFrame({'group':[1,1,1,2,1,2]
                      ,'name':['Bob','Lindy','Mark','Miki','Sully','Rose']
                      ,'score':[98,78,87,77,65,67]
                      ,})
sample


sample.score > 70


sample[sample.score > 70]


sample[(sample.score > 70) & (sample.group ==1)] #且


sample[~(sample.group ==1)] #非


sample[(sample.group ==2) | (sample.group ==1)]


sample.query('score > 90')


sample.query('(group ==2) |(group == 1)')


# sample[sample['score'].between(70,80),inclusive=True]
sample[sample['score'].between(70, 80, inclusive='both')]#Pandas 1.3.0 版本开始，inclusive 参数被修改为 inclusive='both'（或’neither’/‘left’/‘right’） 的字符串形式


sample[sample['name'].isin(['Bob','Lindy'])]


sample[sample['name'].str.contains('[M]+')]


# 1.2.3 横向连接


df1 = pd.DataFrame({ 'col1':['a','b','c'],
                     'id':[1,2,3],
                   })
df2 = pd.DataFrame({ 'col2':['d','e'],
                    'id':[4,3],
                   })


df1


df2


df1.merge(df2,how='inner',on='id')


df1.merge(df2,how='inner',left_on='id',right_on='id')


df1.merge(df2,how='left',on='id')


df1.merge(df2,how='right',on='id')


df1.merge(df2,how='outer',on='id')


df1 = pd.DataFrame({'id1':[1,2,3],
                    'col1':['a','b','c']},
                  index = [1,2,3])
df2 = pd.DataFrame({'id2':[1,2,3],
                    'col2':['aa','bb','cc']},
                  index = [1,3,2])


df1


df2


pd.concat([df1,df2],axis=1)


df1.join(df2)


# 1.2.4 纵向合并


df1 = pd.DataFrame({'id':[1,1,1,2,3,4,6],
                    'col':['a','a','b','c','v','e','q']})
df2 = pd.DataFrame({'id':[1,2,3,3,5],
                    'col':['x','y','z','v','w']})


df1


df2


pd.concat([df1,df2],ignore_index=True,axis=0)


pd.concat([df1,df2],ignore_index=True).drop_duplicates()


df3 = df1.rename(columns = {'col':'new_col'})
df3


pd.concat([df1,df3],ignore_index=True).drop_duplicates()


# 1.2.5 排序


sample=pd.DataFrame({'group':[1,1,1,2,1,2],
                    'name':['Bob','Lindy','Mark','Miki','Sully','Rose'],
                    'score':[98,78,87,77,77,np.nan],
                    })
sample


sample.sort_values('score',ascending=False,na_position='last')


sample.sort_values(['group','score'])


# 1.2.6 分组汇总


sample = pd.DataFrame({"name":['Bob','Lindy','Mark','Miki','Sully','Rose']
                        ,"class":[1,1,1,2,1,2]
                        ,"grade":[1,1,1,2,2,2]
                        ,"chinese":[88,78,86,56,77,54]
                        ,"math":[98,78,87,77,77,np.nan]
                        })
sample


sample.groupby('grade')[['math']].max()


sample.groupby(['grade','class'])[['math']].mean()


sample.groupby(['grade']) [['math','chinese']].mean()


sample.groupby('class')['math'].agg(['mean','min','max'])


df = sample.groupby(['grade','class']) [['math','chinese']].agg(['min','max'])
df


df['math']['min']


df.loc[:,('math','min')]


df.loc[(2,2),('math','min')]


# 1.2.7 拆分列


table = pd.DataFrame({ 'Monetary':[3608,420,1894,3503,4567],
                        'cust_id':[10001,10001,10002,10002,10003],
                        'type':['Normal','Special_offer',\
                        'Normal','Special_offer','Special_offer']
                     })
table


pd.pivot_table(table,index='cust_id',columns='type',values='Monetary')


pd.pivot_table(table,index='cust_id',columns='type',values='Monetary',
        fill_value=0,aggfunc='sum')


# 1.2.8 赋值与条件赋值


sample = pd.DataFrame({'name':['Bob','Lindy','Mark',
        'Miki','Sully','Rose'],
        'score':[99,78,999,77,77,np.nan],
        'group':[1,1,1,2,1,2],})
sample


sample.score.replace(999,np.nan)


sample.replace({'score':{999:np.nan},
                'name':{'Bob':np.nan}})


sample


def transform(row):
    if row['group'] == 1:
        return ('class1')
    elif row['group'] == 2:
        return ('class2')  

sample.apply(transform,axis=1)


sample.assign(class_n = sample.apply(transform,axis=1))


sample = sample.copy()
sample.loc[sample.group==1,'class_n']='class1'
sample.loc[sample.group==2,'class_n']='class2'
sample


# 1.3.1 重复值处理


sample = pd.DataFrame({'group':[1,1,1,2,1,2],
                        'id':[1,1,1,3,4,5],
                       'name':['Bob','Bob','Mark','Miki','Sully','Rose'],
                       'score':[99,99,87,77,77,np.nan],
                       })
sample


sample[sample.duplicated()]


sample.drop_duplicates()


sample.drop_duplicates('id')


# 1.3.2 缺失值处理


sample = pd.DataFrame({'group':[1,1,np.nan,2,1,np.nan],
                        'id':[1,1,1,3,4,np.nan],
                       'name':['Bob','Bob','Mark','Miki','Sully',np.nan],
                       'score':[99,np.nan,87,77,77,np.nan],
                       })
sample


sample.apply(lambda col:sum(col.isnull())/col.size)


sample.score.fillna(sample.score.mean())


sample.score.fillna(sample.score.median())


sample.score.isnull()


sample.score.isnull().apply(int)


# 1.3.3 噪声值处理


def cap(x,quantile=[0.01,0.99]):
    """盖帽法处理异常值
    Args：
        x：pd.Series列，连续变量
        quantile：指定盖帽法的上下分位数范围
    """

# 生成分位数
    Q01,Q99=x.quantile(quantile).values.tolist()

# 替换异常值为指定的分位数
    if Q01 > x.min():
        x = x.copy()
        x.loc[x<Q01] = Q01

    if Q99 < x.max():
        x = x.copy()
        x.loc[x>Q99] = Q99

    return(x)


sample = pd.DataFrame({'normal':np.random.randn(1000)})
sample.hist(bins=50)


new = sample.apply(cap,quantile=[0.01,0.99])
new.hist(bins=50)


np.random.seed(0)
sample =pd.DataFrame({'normal':np.random.randn(10)})
sample


pd.cut(sample.normal,5)


pd.cut(sample.normal,bins=5,labels=[1,2,3,4,5])


pd.cut(sample.normal,bins=2,labels=['bad','good'])


sample.normal.quantile([0,0.5,1])


pd.cut(sample.normal,bins=sample.normal.quantile([0,0.5,1]),
 include_lowest=True)


pd.cut(sample.normal,bins=sample.normal.quantile([0,0.5,1]),labels=['bad','good'],include_lowest=True)

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第4章 数据整合与数据清洗（pandas）
# ====================================
# 项目内涵：使用 pandas 完成数据从"读入"到"清洗"的完整预处理流程，是量化分析的
#          数据底座。涵盖读取、行列操作、连接合并、分组汇总、重复/缺失/噪声值处理。
# 技术方法：read_csv/to_csv、iloc/loc、merge/join/concat、groupby/agg、pivot_table、
#          盖帽法(cap)、pd.cut 分箱。
# 数据源：sample.csv、data/big.csv（分块读取演示）。
# 关键步骤：1)按列/按行/分块读取并写出 → 2)行列选择与条件查询 → 3)横向merge与纵向concat
#          → 4)排序、分组汇总、透视表 → 5)重复值drop_duplicates、缺失值fillna、
#          盖帽法去噪、等频/等距分箱。
#
#    id name  scores
# 0   0   小明    78.0
# 1   1   小红    87.0
# 2   2   小白    99.0
# 3   3   小青  9999.0
# 4   4   小兰     NaN
#    id name
# 0   0   小明
# 1   1   小红
# (900, 4)
# (900, 4)
# (900, 4)
# (900, 4)
# (900, 4)
# (4500, 4)
#    id name  scores
# 0   0   小明    78.0
# 1   1   小红    87.0
# 2   2   小白    99.0
# 3   3   小青  9999.0
# 4   4   小兰     NaN
#    id name  scores
# 0   0   小明    78.0
# 1   1   小红    87.0
# 2   2   小白    99.0
# 3   3   小青  9999.0
# 4   4   小兰     NaN
# None
# None
#           a         b         c         d         e
# 0  1.764052  0.400157  0.978738  2.240893  1.867558
# 1 -0.977278  0.950088 -0.151357 -0.103219  0.410599
# 2  0.144044  1.454274  0.761038  0.121675  0.443863
# 3  0.333674  1.494079 -0.205158  0.313068 -0.854096
# 0    1.764052
# 1   -0.977278
# 2    0.144044
# 3    0.333674
# Name: a, dtype: float64
# 0    1.764052
# 1   -0.977278
# 2    0.144044
# 3    0.333674
# Name: a, dtype: float64
# 0    1.764052
# 1   -0.977278
# 2    0.144044
# 3    0.333674
# Name: a, dtype: float64
#           a
# 0  1.764052
# 1 -0.977278
# 2  0.144044
# 3  0.333674
#           a         b
# 0  1.764052  0.400157
# 1 -0.977278  0.950088
#           a         b
# 0  1.764052  0.400157
# 1 -0.977278  0.950088
#           a         b         c         d         e   new_col
# 0  1.764052  0.400157  0.978738  2.240893  1.867558  1.363895
# 1 -0.977278  0.950088 -0.151357 -0.103219  0.410599 -1.927366
# 2  0.144044  1.454274  0.761038  0.121675  0.443863 -1.310230
# 3  0.333674  1.494079 -0.205158  0.313068 -0.854096 -1.160405
#           a         b         c  ...   new_col  new_col2  new_col3
# 0  1.764052  0.400157  0.978738  ...  1.363895  1.363895  2.164210
# 1 -0.977278  0.950088 -0.151357  ... -1.927366 -1.927366 -0.027189
# 2  0.144044  1.454274  0.761038  ... -1.310230 -1.310230  1.598317
# 3  0.333674  1.494079 -0.205158  ... -1.160405 -1.160405  1.827753
#
# [4 rows x 8 columns]
#           b         c         d         e   new_col
# 0  0.400157  0.978738  2.240893  1.867558  1.363895
# 1  0.950088 -0.151357 -0.103219  0.410599 -1.927366
# 2  1.454274  0.761038  0.121675  0.443863 -1.310230
# 3  1.494079 -0.205158  0.313068 -0.854096 -1.160405
#           c         d         e   new_col
# 0  0.978738  2.240893  1.867558  1.363895
# 1 -0.151357 -0.103219  0.410599 -1.927366
# 2  0.761038  0.121675  0.443863 -1.310230
# 3 -0.205158  0.313068 -0.854096 -1.160405
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
# 2      1   Mark     87
# 3      2   Miki     77
# 4      1  Sully     65
# 5      2   Rose     67
# 0     True
# 1     True
# 2     True
# 3     True
# 4    False
# 5    False
# Name: score, dtype: bool
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
# 2      1   Mark     87
# 3      2   Miki     77
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
# 2      1   Mark     87
#    group  name  score
# 3      2  Miki     77
# 5      2  Rose     67
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
# 2      1   Mark     87
# 3      2   Miki     77
# 4      1  Sully     65
# 5      2   Rose     67
#    group name  score
# 0      1  Bob     98
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
# 2      1   Mark     87
# 3      2   Miki     77
# 4      1  Sully     65
# 5      2   Rose     67
#    group   name  score
# 1      1  Lindy     78
# 3      2   Miki     77
#    group   name  score
# 0      1    Bob     98
# 1      1  Lindy     78
#    group  name  score
# 2      1  Mark     87
# 3      2  Miki     77
#   col1  id
# 0    a   1
# 1    b   2
# 2    c   3
#   col2  id
# 0    d   4
# 1    e   3
#   col1  id col2
# 0    c   3    e
#   col1  id col2
# 0    c   3    e
#   col1  id col2
# 0    a   1  NaN
# 1    b   2  NaN
# 2    c   3    e
#   col1  id col2
# 0  NaN   4    d
# 1    c   3    e
#   col1  id col2
# 0    a   1  NaN
# 1    b   2  NaN
# 2    c   3    e
# 3  NaN   4    d
#    id1 col1
# 1    1    a
# 2    2    b
# 3    3    c
#    id2 col2
# 1    1   aa
# 3    2   bb
# 2    3   cc
#    id1 col1  id2 col2
# 1    1    a    1   aa
# 2    2    b    3   cc
# 3    3    c    2   bb
#    id1 col1  id2 col2
# 1    1    a    1   aa
# 2    2    b    3   cc
# 3    3    c    2   bb
#    id col
# 0   1   a
# 1   1   a
# 2   1   b
# 3   2   c
# 4   3   v
# 5   4   e
# 6   6   q
#    id col
# 0   1   x
# 1   2   y
# 2   3   z
# 3   3   v
# 4   5   w
#     id col
# 0    1   a
# 1    1   a
# 2    1   b
# 3    2   c
# 4    3   v
# 5    4   e
# 6    6   q
# 7    1   x
# 8    2   y
# 9    3   z
# 10   3   v
# 11   5   w
#     id col
# 0    1   a
# 2    1   b
# 3    2   c
# 4    3   v
# 5    4   e
# 6    6   q
# 7    1   x
# 8    2   y
# 9    3   z
# 11   5   w
#    id new_col
# 0   1       a
# 1   1       a
# 2   1       b
# 3   2       c
# 4   3       v
# 5   4       e
# 6   6       q
#     id  col new_col
# 0    1    a     NaN
# 2    1    b     NaN
# 3    2    c     NaN
# 4    3    v     NaN
# 5    4    e     NaN
# 6    6    q     NaN
# 7    1  NaN       a
# 9    1  NaN       b
# 10   2  NaN       c
# 11   3  NaN       v
# 12   4  NaN       e
# 13   6  NaN       q
#    group   name  score
# 0      1    Bob   98.0
# 1      1  Lindy   78.0
# 2      1   Mark   87.0
# 3      2   Miki   77.0
# 4      1  Sully   77.0
# 5      2   Rose    NaN
#    group   name  score
# 0      1    Bob   98.0
# 2      1   Mark   87.0
# 1      1  Lindy   78.0
# 3      2   Miki   77.0
# 4      1  Sully   77.0
# 5      2   Rose    NaN
#    group   name  score
# 4      1  Sully   77.0
# 1      1  Lindy   78.0
# 2      1   Mark   87.0
# 0      1    Bob   98.0
# 3      2   Miki   77.0
# 5      2   Rose    NaN
#     name  class  grade  chinese  math
# 0    Bob      1      1       88  98.0
# 1  Lindy      1      1       78  78.0
# 2   Mark      1      1       86  87.0
# 3   Miki      2      2       56  77.0
# 4  Sully      1      2       77  77.0
# 5   Rose      2      2       54   NaN
#        math
# grade      
# 1      98.0
# 2      77.0
#                   math
# grade class           
# 1     1      87.666667
# 2     1      77.000000
#       2      77.000000
#             math    chinese
# grade                      
# 1      87.666667  84.000000
# 2      77.000000  62.333333
#        mean   min   max
# class                  
# 1      85.0  77.0  98.0
# 2      77.0  77.0  77.0
#              math       chinese    
#               min   max     min max
# grade class                        
# 1     1      78.0  98.0      78  88
# 2     1      77.0  77.0      77  77
#       2      77.0  77.0      54  56
# grade  class
# 1      1        78.0
# 2      1        77.0
#        2        77.0
# Name: min, dtype: float64
# grade  class
# 1      1        78.0
# 2      1        77.0
#        2        77.0
# Name: (math, min), dtype: float64
# 77.0
#    Monetary  cust_id           type
# 0      3608    10001         Normal
# 1       420    10001  Special_offer
# 2      1894    10002         Normal
# 3      3503    10002  Special_offer
# 4      4567    10003  Special_offer
# type     Normal  Special_offer
# cust_id                       
# 10001    3608.0          420.0
# 10002    1894.0         3503.0
# 10003       NaN         4567.0
# type     Normal  Special_offer
# cust_id                       
# 10001      3608            420
# 10002      1894           3503
# 10003         0           4567
#     name  score  group
# 0    Bob   99.0      1
# 1  Lindy   78.0      1
# 2   Mark  999.0      1
# 3   Miki   77.0      2
# 4  Sully   77.0      1
# 5   Rose    NaN      2
# 0    99.0
# 1    78.0
# 2     NaN
# 3    77.0
# 4    77.0
# 5     NaN
# Name: score, dtype: float64
#     name  score  group
# 0    NaN   99.0      1
# 1  Lindy   78.0      1
# 2   Mark    NaN      1
# 3   Miki   77.0      2
# 4  Sully   77.0      1
# 5   Rose    NaN      2
#     name  score  group
# 0    Bob   99.0      1
# 1  Lindy   78.0      1
# 2   Mark  999.0      1
# 3   Miki   77.0      2
# 4  Sully   77.0      1
# 5   Rose    NaN      2
# 0    class1
# 1    class1
# 2    class1
# 3    class2
# 4    class1
# 5    class2
# dtype: object
#     name  score  group class_n
# 0    Bob   99.0      1  class1
# 1  Lindy   78.0      1  class1
# 2   Mark  999.0      1  class1
# 3   Miki   77.0      2  class2
# 4  Sully   77.0      1  class1
# 5   Rose    NaN      2  class2
#     name  score  group class_n
# 0    Bob   99.0      1  class1
# 1  Lindy   78.0      1  class1
# 2   Mark  999.0      1  class1
# 3   Miki   77.0      2  class2
# 4  Sully   77.0      1  class1
# 5   Rose    NaN      2  class2
#    group  id   name  score
# 0      1   1    Bob   99.0
# 1      1   1    Bob   99.0
# 2      1   1   Mark   87.0
# 3      2   3   Miki   77.0
# 4      1   4  Sully   77.0
# 5      2   5   Rose    NaN
#    group  id name  score
# 1      1   1  Bob   99.0
#    group  id   name  score
# 0      1   1    Bob   99.0
# 2      1   1   Mark   87.0
# 3      2   3   Miki   77.0
# 4      1   4  Sully   77.0
# 5      2   5   Rose    NaN
#    group  id   name  score
# 0      1   1    Bob   99.0
# 3      2   3   Miki   77.0
# 4      1   4  Sully   77.0
# 5      2   5   Rose    NaN
#    group   id   name  score
# 0    1.0  1.0    Bob   99.0
# 1    1.0  1.0    Bob    NaN
# 2    NaN  1.0   Mark   87.0
# 3    2.0  3.0   Miki   77.0
# 4    1.0  4.0  Sully   77.0
# 5    NaN  NaN    NaN    NaN
# group    0.333333
# id       0.166667
# name     0.166667
# score    0.333333
# dtype: float64
# 0    99.0
# 1    85.0
# 2    87.0
# 3    77.0
# 4    77.0
# 5    85.0
# Name: score, dtype: float64
# 0    99.0
# 1    82.0
# 2    87.0
# 3    77.0
# 4    77.0
# 5    82.0
# Name: score, dtype: float64
# 0    False
# 1     True
# 2    False
# 3    False
# 4    False
# 5     True
# Name: score, dtype: bool
# 0    0
# 1    1
# 2    0
# 3    0
# 4    0
# 5    1
# Name: score, dtype: int64
# None
#      normal
# 0  1.764052
# 1  0.400157
# 2  0.978738
# 3  2.240893
# 4  1.867558
# 5 -0.977278
# 6  0.950088
# 7 -0.151357
# 8 -0.103219
# 9  0.410599
# 0     (1.597, 2.241]
# 1      (0.31, 0.954]
# 2     (0.954, 1.597]
# 3     (1.597, 2.241]
# 4     (1.597, 2.241]
# 5    (-0.98, -0.334]
# 6      (0.31, 0.954]
# 7     (-0.334, 0.31]
# 8     (-0.334, 0.31]
# 9      (0.31, 0.954]
# Name: normal, dtype: category
# Categories (5, interval[float64, right]): [(-0.98, -0.334] < (-0.334, 0.31] < (0.31, 0.954] <
#                                            (0.954, 1.597] < (1.597, 2.241]]
# 0    5
# 1    3
# 2    4
# 3    5
# 4    5
# 5    1
# 6    3
# 7    2
# 8    2
# 9    3
# Name: normal, dtype: category
# Categories (5, int64): [1 < 2 < 3 < 4 < 5]
# 0    good
# 1     bad
# 2    good
# 3    good
# 4    good
# 5     bad
# 6    good
# 7     bad
# 8     bad
# 9     bad
# Name: normal, dtype: category
# Categories (2, object): ['bad' < 'good']
# 0.0   -0.977278
# 0.5    0.680343
# 1.0    2.240893
# Name: normal, dtype: float64
# 0     (0.68, 2.241]
# 1    (-0.978, 0.68]
# 2     (0.68, 2.241]
# 3     (0.68, 2.241]
# 4     (0.68, 2.241]
# 5    (-0.978, 0.68]
# 6     (0.68, 2.241]
# 7    (-0.978, 0.68]
# 8    (-0.978, 0.68]
# 9    (-0.978, 0.68]
# Name: normal, dtype: category
# Categories (2, interval[float64, right]): [(-0.978, 0.68] < (0.68, 2.241]]
# 0    good
# 1     bad
# 2    good
# 3    good
# 4    good
# 5     bad
# 6    good
# 7     bad
# 8     bad
# 9     bad
# Name: normal, dtype: category
# Categories (2, object): ['bad' < 'good']


# ================================================================
# 2. 第5章 Python 数据可视化（matplotlib + seaborn）
# 源文件: 第5章-数据可视化\第5章 python数据可视化.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第5章-数据可视化
# ================================================================

# -*- coding: utf-8 -*-
"""
第5章 Python 数据可视化（matplotlib + seaborn）
=================================================
项目内涵：用 matplotlib 与 seaborn 绘制常见统计图形，掌握"选图—绘图—美化"全流程，
         为量化策略的结果呈现打基础。
技术方法：plot线图、pie饼图、bar/barh条形图、hist直方图、scatter散点图、boxplot箱线图；
         seaborn 的 displot(核密度)、jointplot(二元分布)、heatmap(热图)。
数据源：2017股价.xlsx（股价走势）、随机生成的投票/成绩/产量数据。
关键步骤：1)线图看股价走势 → 2)饼图/条形图看占比 → 3)直方图/散点图/箱线图看分布
         → 4)seaborn 加核密度与二元分布 → 5)热图看矩阵相关性。
注意：中文显示需设置 SimHei 字体并关闭 unicode_minus。
"""

# 2.1.1 线图


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r"2017股价.xlsx")
df


import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['axes.unicode_minus']=False#解决保存图像时负号'-'显示为方块的问题
plt.rcParams['font.sans-serif'] = ['SimHei']#指定默认字体


plt.figure(figsize=(10,4)) #生成画布并设置画布尺寸
plt.plot(range(15),df.loc[:,"收盘价"],'-*') #共15个数据点，x轴需要15个刻度点
plt.plot(range(15),df.loc[:,"开盘价"],'-o') 
plt.plot(range(15),df.loc[:,"最高价"],'-v') 
plt.plot(range(15),df.loc[:,"最低价"],'-^')
plt.title('股价走势图') #设置标题
plt.xlabel('时间') #设置x轴标签
plt.ylabel('股价') #设置y轴标签
plt.xticks(range(15),df.日期,rotation=30) #设置刻度的标签，倾斜度
plt.legend(['收盘价','开盘价','最高价','最低价']) #设置图例
plt.show()#展示图形


# 2.1.2 饼图


np.random.seed(1)
df=pd.DataFrame(data={"方案":["plan A","plan B","plan C","plan D","plan E"]
                            ,"投票人数":np.random.randint(10,100,5)})
df




plt.figure(figsize=(6,6))
plt.pie(df.投票人数 #饼图数据源
        ,labels=df.方案 #设置每个扇形对应的标签
        ,autopct='%.2f%%' #设置百分比经度
        ,textprops={'fontsize':13} #设置饼图中字体的大小
    )
plt.title('方案投票占比饼图',fontsize=14);
plt.show()


# 2.1.3 条形图


plt.figure(figsize=(8,4))
plt.bar(df.方案,df.投票人数,width=0.6)
plt.title("各方案投票人数柱形图",fontsize = 14)
plt.ylabel("投票人数",fontsize = 13)
plt.xlabel("方案",fontsize = 13)
plt.show()




plt.figure(figsize=(8,4))
plt.barh(df.sort_values("投票人数").方案,df.sort_values("投票人数").投票人数,height=0.6)
plt.xlabel("投票人数",fontsize = 13)
plt.ylabel("方案",fontsize = 13)
plt.title("各方案投票人数条形图",fontsize = 14)
plt.show()


# 2.1.4 直方图


np.random.seed(1)
np.random.seed(1)
data = np.random.normal(loc=80, scale=20,size=200).astype(int)
data


plt.hist(data,[30,40,50,60,70,80,90,100,110,120,130])
plt.xticks([30,40,50,60,70,80,90,100,110,120,130])
plt.show()


# 2.1.5 散点图


df = pd.DataFrame({"产量":[2200,3300,4400,5500,5700,7300,8000]
              ,"降水量":[22,39,55,66,105,100,122]})
df


plt.scatter(df.降水量,df.产量)
plt.show()


# 2.1.6 箱线图


np.random.seed(1)
df=pd.DataFrame({"语文":np.random.randint(60,150,10)
                ,"英语":np.random.randint(40,150,10)
                ,"数学":np.random.randint(20,150,10)})
df


plt.figure(figsize=(8,6))
plt.boxplot([df.语文,df.英语,df.数学]
            ,labels=['语文','英语','数学']);


# 2.2.1 带核密度估计的直方图


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
np.random.seed(1)
np.random.seed(1)
data = np.random.normal(loc=80, scale=20,size=200).astype(int)
data


sns.displot(data,bins=[30,40,50,60,70,80,90,100,110,120,130],kde=True)# kde=True 显示核密度估计曲线
plt.show()


# 2.2.2 二元分布图


np.random.seed(0)
mean, cov = [0, 1], [(1, .5), (.5, 1)]
data = np.random.multivariate_normal(mean, cov, 200)
df = pd.DataFrame(data, columns=["x", "y"])
df.head()


sns.jointplot(x="x", y="y", data=df)
plt.show()


sns.relplot(x="x", y="y", data=df)
plt.show()


sns.jointplot(x="x", y="y", data=df, kind="kde")
plt.show()


sns.displot(data=df, x="x", y="y", kind="kde")
plt.show()


# 2.2.3 热图


np.random.seed(0)
df0=pd.DataFrame(np.random.uniform(
                -1,1,(7,7)),index=list("abcdefg"),columns=list("ABCDEFG"))
df0


plt.figure(figsize=(8,6))
sns.set(font_scale=1.5)#设置字体大小
sns.heatmap(df0)

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第5章 Python 数据可视化（matplotlib + seaborn）
# =================================================
# 项目内涵：用 matplotlib 与 seaborn 绘制常见统计图形，掌握"选图—绘图—美化"全流程，
#          为量化策略的结果呈现打基础。
# 技术方法：plot线图、pie饼图、bar/barh条形图、hist直方图、scatter散点图、boxplot箱线图；
#          seaborn 的 displot(核密度)、jointplot(二元分布)、heatmap(热图)。
# 数据源：2017股价.xlsx（股价走势）、随机生成的投票/成绩/产量数据。
# 关键步骤：1)线图看股价走势 → 2)饼图/条形图看占比 → 3)直方图/散点图/箱线图看分布
#          → 4)seaborn 加核密度与二元分布 → 5)热图看矩阵相关性。
# 注意：中文显示需设置 SimHei 字体并关闭 unicode_minus。
#
#            日期        收盘价        最高价  ...      涨跌额     涨跌幅        成交量
# 0  2017-09-14  3371.4256  3391.6435  ... -12.7214 -0.3759  221306487
# 1  2017-09-13  3384.1470  3387.1397  ...   4.6590  0.1379  194550715
# 2  2017-09-12  3379.4880  3391.0694  ...   3.0692  0.0909  272910319
# 3  2017-09-11  3376.4188  3384.8100  ...  11.1762  0.3321  219011019
# 4  2017-09-08  3365.2426  3380.8898  ...  -0.2548 -0.0076  198405184
# 5  2017-09-07  3365.4974  3387.7956  ... -19.8914 -0.5876  221118685
# 6  2017-09-06  3385.3888  3391.0105  ...   1.0718  0.0317  229090785
# 7  2017-09-05  3384.3170  3390.8233  ...   4.7340  0.1401  216552946
# 8  2017-09-04  3379.5830  3381.4027  ...  12.4636  0.3702  267427849
# 9  2017-09-01  3367.1194  3381.9252  ...   6.3091  0.1877  282497584
# 10 2017-08-31  3360.8103  3367.3581  ...  -2.8163 -0.0837  234419781
# 11 2017-08-30  3363.6266  3376.6481  ...  -1.5995 -0.0475  246863312
# 12 2017-08-29  3365.2261  3374.5947  ...   2.5747  0.0766  219504535
# 13 2017-08-28  3362.6514  3375.0339  ...  31.1293  0.9344  257461438
# 14 2017-08-25  3331.5221  3331.9146  ...  60.0104  1.8343  205839482
#
# [15 rows x 8 columns]
# None
#        方案  投票人数
# 0  plan A    47
# 1  plan B    22
# 2  plan C    82
# 3  plan D    19
# 4  plan E    85
# None
# None
# [112  67  69  58  97  33 114  64  86  75 109  38  73  72 102  58  76  62
#   80  91  57 102  98  90  98  66  77  61  74  90  66  72  66  63  66  79
#   57  84 113  94  76  62  65 113  81  67  83 122  82  92  86  72  57  73
#   75  91  96  98  85  97  64 105  90  74  89  78 102 110 123  52  51  69
#   83  97  86  39  73  96  84  95  75  75  83  88  83  82  66  87  82 102
#  103  83  72  67  88  81  73  80  67  93  71 104  88  91  58  83  94  60
#   74  80  52  86  96  62  87  53  79  47 102  88  79  64 105 119  42 104
#  112  86  56  97  76  67  55  91  95  67  90  57  96  80  76  77  97  95
#   90  82  81  92  84  93  73  31 100 123  88  77  77  77  80  57  69  60
#   84  74  89  76  99  84 123  42  67  98 130  75  80  75 106  74  93  73
#   54  86  90 105  77  67  91  84  85  78 103  87 118 102  93  47  92  88
#   96 100]
#      产量  降水量
# 0  2200   22
# 1  3300   39
# 2  4400   55
# 3  5500   66
# 4  5700  105
# 5  7300  100
# 6  8000  122
# None
#     语文   英语   数学
# 0   97  116   70
# 1   72  111   88
# 2  132  149  116
# 3   69   46  106
# 4  135   65   27
# 5   65   90   83
# 6  139   60   81
# 7  124  141   42
# 8   76   58   77
# 9   61  124   21
# None
# None
# [112  67  69  58  97  33 114  64  86  75 109  38  73  72 102  58  76  62
#   80  91  57 102  98  90  98  66  77  61  74  90  66  72  66  63  66  79
#   57  84 113  94  76  62  65 113  81  67  83 122  82  92  86  72  57  73
#   75  91  96  98  85  97  64 105  90  74  89  78 102 110 123  52  51  69
#   83  97  86  39  73  96  84  95  75  75  83  88  83  82  66  87  82 102
#  103  83  72  67  88  81  73  80  67  93  71 104  88  91  58  83  94  60
#   74  80  52  86  96  62  87  53  79  47 102  88  79  64 105 119  42 104
#  112  86  56  97  76  67  55  91  95  67  90  57  96  80  76  77  97  95
#   90  82  81  92  84  93  73  31 100 123  88  77  77  77  80  57  69  60
#   84  74  89  76  99  84 123  42  67  98 130  75  80  75 106  74  93  73
#   54  86  90 105  77  67  91  84  85  78 103  87 118 102  93  47  92  88
#   96 100]
# <seaborn.axisgrid.FacetGrid object at 0x00000266A8895AB0>
# None
#           x         y
# 0 -1.727793 -0.327636
# 1 -1.968059  1.272835
# 2 -1.128714 -1.105992
# 3 -0.747122  0.101521
# 4 -0.115909  1.294689
# <seaborn.axisgrid.JointGrid object at 0x00000266A88956F0>
# <seaborn.axisgrid.FacetGrid object at 0x00000266CCEC9180>
# <seaborn.axisgrid.JointGrid object at 0x00000266CCEC9180>
# <seaborn.axisgrid.FacetGrid object at 0x00000266CCEC9180>
# None
#           A         B         C         D         E         F         G
# a  0.097627  0.430379  0.205527  0.089766 -0.152690  0.291788 -0.124826
# b  0.783546  0.927326 -0.233117  0.583450  0.057790  0.136089  0.851193
# c -0.857928 -0.825741 -0.959563  0.665240  0.556314  0.740024  0.957237
# d  0.598317 -0.077041  0.561058 -0.763451  0.279842 -0.713293  0.889338
# e  0.043697 -0.170676 -0.470889  0.548467 -0.087699  0.136868 -0.962420
# f  0.235271  0.224191  0.233868  0.887496  0.363641 -0.280984 -0.125936
# g  0.395262 -0.879549  0.333533  0.341276 -0.579235 -0.742147 -0.369143
# None
# Axes(0.125,0.11;0.62x0.77)
# [stderr] <string>:21: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:28: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:34: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:40: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:47: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:51: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:56: MatplotlibDeprecationWarning: The 'labels' parameter of boxplot() has been renamed 'tick_labels' since Matplotlib 3.9; support for the old name will be dropped in 3.11.
# [stderr] <string>:66: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:73: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:75: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:77: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:79: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown


# ================================================================
# 3. 第5章 描述性统计分析与绘图
# 源文件: 第5章-数据可视化\第5章 描述性统计分析与绘图.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第5章-数据可视化
# ================================================================

# -*- coding: utf-8 -*-
"""
第5章 描述性统计分析与绘图
==========================
项目内涵：用 pandas 对连续变量做描述性统计，量化"集中趋势—离散程度—分布形态"三维度，
         并计算变量间相关系数。
技术方法：mean/median/std、quantile、max-min(极差)、var、skew(偏度)、kurtosis(峰度)、
         corr(pearson/spearman/kendall)。
数据源：sndHsPr.csv（二手房价数据，含面积 AREA 与价格 price）。
关键步骤：1)集中趋势(均值/中位数/标准差/分位数) → 2)离散程度(极差/方差/标准差)
         → 3)分布形态(偏度/峰度) → 4)相关系数(三种)。
"""

# 3.1.3 连续变量的分布与集中趋势


import pandas as pd
data = pd.read_csv('sndHsPr.csv')


data.price.agg(['mean','median','std'])


data. price.quantile([0.25,0.5,0.75])


data.price.hist(bins=20)


# 3.1.4 连续变量的离散程度


data.price.max()-data.price.min()


data.price.var()#求方差


data.price.std()#求标准差


# 3.1.5 数据分布的对称与高矮


import numpy as np


normal = pd.Series(np.random.randn(1000),name='normal')


normal.skew()


normal.kurtosis()


data[['AREA','price']].corr("pearson")


data[['AREA','price']].corr("spearman")


data[['AREA','price']].corr("kendall")

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第5章 描述性统计分析与绘图
# ==========================
# 项目内涵：用 pandas 对连续变量做描述性统计，量化"集中趋势—离散程度—分布形态"三维度，
#          并计算变量间相关系数。
# 技术方法：mean/median/std、quantile、max-min(极差)、var、skew(偏度)、kurtosis(峰度)、
#          corr(pearson/spearman/kendall)。
# 数据源：sndHsPr.csv（二手房价数据，含面积 AREA 与价格 price）。
# 关键步骤：1)集中趋势(均值/中位数/标准差/分位数) → 2)离散程度(极差/方差/标准差)
#          → 3)分布形态(偏度/峰度) → 4)相关系数(三种)。
#
# mean      61151.810919
# median    57473.000000
# std       22293.358147
# Name: price, dtype: float64
# 0.25    42812.25
# 0.50    57473.00
# 0.75    76099.75
# Name: price, dtype: float64
# 131523
# 496993817.485068
# 22293.358147328723
# -0.050589110305626905
# -0.07903186703701381
#            AREA     price
# AREA   1.000000 -0.073955
# price -0.073955  1.000000
#            AREA     price
# AREA   1.000000 -0.114628
# price -0.114628  1.000000
#           AREA    price
# AREA   1.00000 -0.07458
# price -0.07458  1.00000


# ================================================================
# 4. 第6章 数据采集方法 —— 抽样
# 源文件: 第6章-市场调研与数据预处理\1数据采集与处理 1 数据采集方法\抽样.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第6章-市场调研与数据预处理\1数据采集与处理 1 数据采集方法
# ================================================================

# -*- coding: utf-8 -*-
"""
第6章 数据采集方法 —— 抽样
==========================
项目内涵：市场调研中从总体抽取代表性样本的三种基本抽样方法，自定义统一接口 get_sample，
         支持按数量或按比例抽样。
技术方法：random.sample(简单随机)、等距 step(系统抽样)、groupby 分层(分层抽样)。
数据源：clients.csv（客户地区信息，按 Dist 分层）。
关键步骤：1)定义 get_sample 统一接口 → 2)简单随机抽样(按个数/按比例)
         → 3)分层抽样(按 Dist 列) → 4)系统抽样(等距)。
注意：原码用 `is` 比较字符串(python3 已弃用)，保留以忠于教材。
"""

# coding: utf-8

# In[147]:
#定义抽样函数

def get_sample(df, sampling="simple_random", k=1, stratified_col=None):
    """
    对输入的 dataframe 进行抽样的函数

    参数:
        - df: 输入的数据框 pandas.dataframe 对象

        - sampling:抽样方法 str
            可选值有 ["simple_random", "stratified", "systematic"]
            按顺序分别为: 简单随机抽样、分层抽样、系统抽样

        - k: 抽样个数或抽样比例 int or float
            (int, 则必须大于0; float, 则必须在区间(0,1)中)
            如果 0 < k < 1 , 则 k 表示抽样对于总体的比例
            如果 k >= 1 , 则 k 表示抽样的个数；当为分层抽样时，代表每层的样本量

        - stratified_col: 需要分层的列名的列表 list
            只有在分层抽样时才生效

    返回值:
        pandas.dataframe 对象, 抽样结果
    """
    import random
    import pandas as pd
    from functools import reduce
    import numpy as np
    import math
    
    len_df = len(df)
    if k <= 0:
        raise AssertionError("k不能为负数")
    elif k >= 1:
        assert isinstance(k, int), "选择抽样个数时, k必须为正整数"
        sample_by_n=True
        if sampling is "stratified":
            alln=k*df.groupby(by=stratified_col)[stratified_col[0]].count().count() # 有问题的
            #alln=k*df[stratified_col].value_counts().count() 
            if alln >= len_df:
                raise AssertionError("请确认k乘以层数不能超过总样本量")
    else:
        sample_by_n=False
        if sampling in ("simple_random", "systematic"):
            k = math.ceil(len_df * k)
        
    #print(k)

    if sampling is "simple_random":
        print("使用简单随机抽样")
        idx = random.sample(range(len_df), k)
        res_df = df.iloc[idx,:].copy()
        return res_df

    elif sampling is "systematic":
        print("使用系统抽样")
        step = len_df // k+1          #step=len_df//k-1
        start = 0                  #start=0
        idx = range(len_df)[start::step]  #idx=range(len_df+1)[start::step]
        res_df = df.iloc[idx,:].copy()
        #print("k=%d,step=%d,idx=%d"%(k,step,len(idx)))
        return res_df

    elif sampling is "stratified":
        assert stratified_col is not None, "请传入包含需要分层的列名的列表"
        assert all(np.in1d(stratified_col, df.columns)), "请检查输入的列名"
        
        grouped = df.groupby(by=stratified_col)[stratified_col[0]].count()
        if sample_by_n==True:
            group_k = grouped.map(lambda x:k)
        else:
            group_k = grouped.map(lambda x: math.ceil(x * k))
        
        res_df = pd.DataFrame(columns=df.columns)
        for df_idx in group_k.index:
            df1=df
            if len(stratified_col)==1:
                df1=df1[df1[stratified_col[0]]==df_idx]
            else:
                for i in range(len(df_idx)):
                    df1=df1[df1[stratified_col[i]]==df_idx[i]]
            idx = random.sample(range(len(df1)), group_k[df_idx])
            group_df = df1.iloc[idx,:].copy()
            res_df = pd.concat([res_df,group_df])
        return res_df

    else:
        raise AssertionError("sampling is illegal")





#%%
import pandas as pd
clients = pd.read_csv(r'clients.csv',encoding = 'gbk')
#clients["district_id_c"]=clients["district_id"].map(lambda x:"id"+str(x))
#%%
# 在每个地区分别用简单随机抽样、分层抽样、系统抽样，三种方式抽取样本

clients.count()



#%%1简单随机抽样
#%%简单随机抽样-按数量取
srn=get_sample(clients, sampling="simple_random", k=22, stratified_col=None)
#%%简单随机抽样-按百分比取
srp=get_sample(clients, sampling="simple_random", k=0.1, stratified_col=None)
srp.count()


#%%2分层抽样
#%%分层抽样-按每层数量取
strn=get_sample(clients, sampling="stratified", k=2, stratified_col=['Dist'])
#%%分层抽样-按每层百分比取
strp=get_sample(clients, sampling="stratified", k=0.1, stratified_col=['Dist'])

strp.count()


#%%3系统抽样
#%%系统抽样-按数量取
sysn=get_sample(clients, sampling="systematic", k=4, stratified_col=None)
#%%系统抽样-按百分比取
sysp=get_sample(clients, sampling="systematic", k=0.1, stratified_col=None)
#%%
sysp.count()

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第6章 数据采集方法 —— 抽样
# ==========================
# 项目内涵：市场调研中从总体抽取代表性样本的三种基本抽样方法，自定义统一接口 get_sample，
#          支持按数量或按比例抽样。
# 技术方法：random.sample(简单随机)、等距 step(系统抽样)、groupby 分层(分层抽样)。
# 数据源：clients.csv（客户地区信息，按 Dist 分层）。
# 关键步骤：1)定义 get_sample 统一接口 → 2)简单随机抽样(按个数/按比例)
#          → 3)分层抽样(按 Dist 列) → 4)系统抽样(等距)。
# 注意：原码用 `is` 比较字符串(python3 已弃用)，保留以忠于教材。
#
# Client_id    5369
# Gender       5369
# BirthDay     5369
# Dist         5369
# dtype: int64
# 使用简单随机抽样
# 使用简单随机抽样
# Client_id    537
# Gender       537
# BirthDay     537
# Dist         537
# dtype: int64
# Client_id    573
# Gender       573
# BirthDay     573
# Dist         573
# dtype: int64
# 使用系统抽样
# 使用系统抽样
# Client_id    537
# Gender       537
# BirthDay     537
# Dist         537
# dtype: int64
# [stderr] <string>:36: SyntaxWarning: "is" with a literal. Did you mean "=="?
# [stderr] <string>:44: SyntaxWarning: "is" with a literal. Did you mean "=="?
# [stderr] <string>:49: SyntaxWarning: "is" with a literal. Did you mean "=="?
# [stderr] <string>:56: SyntaxWarning: "is" with a literal. Did you mean "=="?
# [stderr] <string>:58: DeprecationWarning: `in1d` is deprecated. Use `np.isin` instead.
# [stderr] <string>:58: DeprecationWarning: `in1d` is deprecated. Use `np.isin` instead.


# ================================================================
# 5. 第6章 数据预处理基础 —— 脏数据清洗
# 源文件: 第6章-市场调研与数据预处理\2 数据预处理基础\数据预处理.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第6章-市场调研与数据预处理\2 数据预处理基础
# ================================================================

# -*- coding: utf-8 -*-
"""
第6章 数据预处理基础 —— 脏数据清洗
====================================
项目内涵：对外部获取的电信营销数据做基础质量检查与清洗，重点处理"用 0 表示缺失"的
         伪缺失值，并通过直方图观察分布。
技术方法：read_csv、describe、hist、replace({0:np.NaN})。
数据源：teleco_camp_orig.csv（电信营销客户收入/房价数据）。
关键步骤：1)读入并查看 AvgIncome 分布 → 2)describe 发现 0 值异常
         → 3)将 0 替换为 NaN → 4)指定值域重绘直方图。
"""

import pandas as pd
import os
import numpy as np
# 导入数据
camp = pd.read_csv(r"teleco_camp_orig.csv")
# 脏数据或数据不正确
import matplotlib.pyplot as plt
plt.hist(camp["AvgIncome"],bins=20)#,normed=True)#查看分布情况


camp["AvgIncome"].describe(include="all")


camp["AvgHomeValue"].describe(include="all")


#这里的 0值应该是缺失值，处理 0值。
camp["AvgIncome"]=camp["AvgIncome"].replace({0:np.nan})


#像这种外部获取的数据要比较小心，经常出现意义不清晰或这错误值。AvgHomeValue也有这种情况
plt.hist(camp["AvgIncome"],bins=20,range=(camp.AvgIncome.min(),camp.AvgIncome.max()))
#由于数据中存在缺失值 ,需要指定绘图的值域


camp["AvgHomeValue"].describe(include="all")

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第6章 数据预处理基础 —— 脏数据清洗
# ====================================
# 项目内涵：对外部获取的电信营销数据做基础质量检查与清洗，重点处理"用 0 表示缺失"的
#          伪缺失值，并通过直方图观察分布。
# 技术方法：read_csv、describe、hist、replace({0:np.NaN})。
# 数据源：teleco_camp_orig.csv（电信营销客户收入/房价数据）。
# 关键步骤：1)读入并查看 AvgIncome 分布 → 2)describe 发现 0 值异常
#          → 3)将 0 替换为 NaN → 4)指定值域重绘直方图。
#
# count      9686.000000
# mean      40491.444249
# std       28707.494146
# min           0.000000
# 25%       24464.000000
# 50%       43100.000000
# 75%       56876.000000
# max      200001.000000
# Name: AvgIncome, dtype: float64
# count      9686.000000
# mean     110986.299814
# std       98670.855450
# min           0.000000
# 25%       52300.000000
# 50%       76900.000000
# 75%      128175.000000
# max      600000.000000
# Name: AvgHomeValue, dtype: float64
# count      9686.000000
# mean     110986.299814
# std       98670.855450
# min           0.000000
# 25%       52300.000000
# 50%       76900.000000
# 75%      128175.000000
# max      600000.000000
# Name: AvgHomeValue, dtype: float64


# ================================================================
# 6. 第7章 特征降维 —— 主成分分析(PCA)
# 源文件: 第7章-特征降维方法\在 Python 中实现主成分分析.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第7章-特征降维方法
# ================================================================

# -*- coding: utf-8 -*-
"""
第7章 特征降维 —— 主成分分析(PCA)
===================================
项目内涵：电信运营商根据客户在主要业务上的使用情况做分群，原始变量较多且相关，
         用 PCA 把多个相关业务指标降为少数主成分，作为后续分群的输入。
技术方法：scale(中心标准化)、PCA(n_components, whiten)、explained_variance_ratio_、
         components_(载荷)、transform(得分)。
数据源：profile_telecom.csv（电信客户业务使用频次）。
关键步骤：1)读入并查看相关矩阵 → 2)中心标准化 → 3)拟合 PCA 取 2 个主成分
         → 4)查看方差解释率/载荷/主成分得分。
"""

# # 在 Python 中实现主成分分析. 
# 一家电信运营商希望根据客户在几个主要业务上的使用情况，对客户进行分群
# 分析。


# ![image.png](attachment:image.png)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


profile = pd.read_csv("profile_telecom.csv")
profile.head()


data = profile.loc[:,"cnt_call":]
data.corr(method = "pearson")


from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
data_scaled = scale(data)
pca = PCA(n_components = 2, whiten = True).fit(data_scaled)
pca.explained_variance_ratio_


pca.components_


pca.transform(data_scaled)

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第7章 特征降维 —— 主成分分析(PCA)
# ===================================
# 项目内涵：电信运营商根据客户在主要业务上的使用情况做分群，原始变量较多且相关，
#          用 PCA 把多个相关业务指标降为少数主成分，作为后续分群的输入。
# 技术方法：scale(中心标准化)、PCA(n_components, whiten)、explained_variance_ratio_、
#          components_(载荷)、transform(得分)。
# 数据源：profile_telecom.csv（电信客户业务使用频次）。
# 关键步骤：1)读入并查看相关矩阵 → 2)中心标准化 → 3)拟合 PCA 取 2 个主成分
#          → 4)查看方差解释率/载荷/主成分得分。
#
#         ID  cnt_call  cnt_msg  cnt_wei  cnt_web
# 0  1964627        46       90       36       31
# 1  3107769        53        2        0        2
# 2  3686296        28       24        5        8
# 3  3961002         9        2        0        4
# 4  4174839       145        2        0        1
#           cnt_call   cnt_msg   cnt_wei   cnt_web
# cnt_call  1.000000  0.052096  0.117832  0.114190
# cnt_msg   0.052096  1.000000  0.510686  0.739506
# cnt_wei   0.117832  0.510686  1.000000  0.950492
# cnt_web   0.114190  0.739506  0.950492  1.000000
# [0.62510442 0.24620209]
# [[ 0.11085805  0.50974123  0.57909319  0.62651852]
#  [ 0.99020127 -0.12736724 -0.01900236 -0.05401806]]
# [[ 2.30183615 -0.89716788]
#  [-0.74694076 -0.04035188]
#  [-0.11502116 -0.59578592]
#  ...
#  [ 2.19333782  0.04953167]
#  [-0.07833419 -0.10944885]
#  [-0.6621524   1.16641367]]


# ================================================================
# 7. 第7章 特征降维 —— 因子分析(PCA + fa_kit)
# 源文件: 第7章-特征降维方法\在 Python 中实现因子分析.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第7章-特征降维方法
# ================================================================

# -*- coding: utf-8 -*-
"""
第7章 特征降维 —— 因子分析(PCA + fa_kit)
==========================================
项目内涵：对 10 个城市的 9 项经济指标先做 PCA 确定主成分个数，再用 fa_kit 做因子分析，
         经最大方差旋转得到可解释的公共因子(Gross 总量因子 / Avg 人均因子)，并计算因子
         得分用于城市定位散点图。
技术方法：preprocessing.scale、PCA(看解释方差)、fa_kit.FactorAnalysis、
         find_comps_to_retain(top_n)、rotate_components(varimax)、因子得分=数据×载荷。
数据源：cities_10.csv（10 城市 9 项经济指标 X1~X9）。
关键步骤：1)标准化 → 2)PCA 看解释方差定 2 个主成分 → 3)fa_kit 提取并 varimax 旋转
         → 4)因子得分=数据×权重 → 5)命名(Gross/Avg)并画城市散点图。
依赖：fa_kit（第三方包，pip install fa_kit）。
"""

# # 主成分分析


# ```
# X1	GDP
# X2	人均GDP
# X3	工业增加值
# X4	第三产业增加值
# X5	固定资产投资
# X6	基本建设投资
# X7	社会消费品零售总额
# X8	海关出口总额
# X9	地方财政收入
# ```


# ## 导入数据


import pandas as pd


#1.导入数据
model_data = pd.read_csv("cities_10.csv",encoding='gbk')
model_data.head()


data = model_data.loc[ :,'X1':]
data.head()


# ## 中心标准化


# 3.做主成分之前，进行中心标准化
from sklearn import preprocessing
data = preprocessing.scale(data)


data


# ## 计算各主成分解释的变异


# 4.使用sklearn的主成分分析，用于判断保留主成分的数量
from sklearn.decomposition import PCA


# ``` 
# 说明：1、第一次的n_components参数应该设的大一点
# 说明：2、观察explained_variance_ratio_和explained_variance_的取值变化，建议explained_variance_ratio_累积大于0.85,explained_variance_需要保留的最后一个主成分大于0.8，
# ```


pca = PCA(n_components=9)
pca.fit(data)


print(pca.explained_variance_)#解释的方差（对于标准化数据来说，单个主成分解释的方差应该大于1）
print(pca.explained_variance_ratio_)


# ## 选取主成分保留个数


pca = PCA(n_components=2).fit(data)


#特征值
pca.explained_variance_


# ## 计算主成分得分


# # 因子分析


# 安装fa_kit


# ## 导入数据


# 1.因子分析的概念很多，作为刚入门的人，我们可以认为因子分析是主成分分析的延续
from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting


fa = FactorAnalysis.load_data_samples(
        data,     #标准化以后的数据
        preproc_demean=True,
        preproc_scale=True
        ) 
fa.extract_components()


# ## 主成分法


# 2.设定提取主成分的方式。默认为“broken_stick”方法，建议使用“top_n”法
fa.find_comps_to_retain(method='top_n',num_keep=2)


# ## 最大方差旋转法


# 3.通过最大方差法进行因子旋转
fa.rotate_components(method='varimax')
pd.DataFrame(fa.comps["rot"])#查看因子权重


# ## 计算因子得分


# 4.获取因子得分
#以下是矩阵相乘的方式计算因子：因子=原始数据（n*k）*权重矩阵(k*num_keep)


import numpy as np


fas = pd.DataFrame(fa.comps["rot"])   #因子权重
data = pd.DataFrame(data)#注意data数据需要标准化
fa_score = pd.DataFrame(np.dot(data, fas))


data


fas


#因子得分
fa_score


#因子命名
a=fa_score.rename(columns={0: "Gross", 1: "Avg"})
citi10_fa=model_data.join(a)


citi10_fa


from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


import matplotlib.pyplot as plt
x=citi10_fa['Gross']
y=citi10_fa['Avg']
label=citi10_fa['AREA']
plt.scatter(x, y)
for a,b,l in zip(x,y,label):
    plt.text(a, b+0.1, '%s.' % l, ha='center', va= 'bottom',fontsize=14)

plt.show()

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第7章 特征降维 —— 因子分析(PCA + fa_kit)
# ==========================================
# 项目内涵：对 10 个城市的 9 项经济指标先做 PCA 确定主成分个数，再用 fa_kit 做因子分析，
#          经最大方差旋转得到可解释的公共因子(Gross 总量因子 / Avg 人均因子)，并计算因子
#          得分用于城市定位散点图。
# 技术方法：preprocessing.scale、PCA(看解释方差)、fa_kit.FactorAnalysis、
#          find_comps_to_retain(top_n)、rotate_components(varimax)、因子得分=数据×载荷。
# 数据源：cities_10.csv（10 城市 9 项经济指标 X1~X9）。
# 关键步骤：1)标准化 → 2)PCA 看解释方差定 2 个主成分 → 3)fa_kit 提取并 varimax 旋转
#          → 4)因子得分=数据×权重 → 5)命名(Gross/Avg)并画城市散点图。
# 依赖：fa_kit（第三方包，pip install fa_kit）。
#
#   AREA       X1     X2      X3      X4      X5      X6      X7     X8     X9
# 0   辽宁   5458.2  13000  1376.2  2258.4  1315.9   529.0  2258.4  123.7  399.7
# 1   山东  10550.0  11643  3502.5  3851.0  2288.7  1070.7  3181.9  211.1  610.2
# 2   河北   6076.6   9047  1406.7  2092.6  1161.6   597.1  1968.3   45.9  302.3
# 3   天津   2022.6  22068   822.8   960.0   703.7   361.9   941.4  115.7  171.8
# 4   江苏  10636.3  14397  3536.3  3967.2  2320.0  1141.3  3215.8  384.7  643.7
#         X1     X2      X3      X4      X5      X6      X7     X8     X9
# 0   5458.2  13000  1376.2  2258.4  1315.9   529.0  2258.4  123.7  399.7
# 1  10550.0  11643  3502.5  3851.0  2288.7  1070.7  3181.9  211.1  610.2
# 2   6076.6   9047  1406.7  2092.6  1161.6   597.1  1968.3   45.9  302.3
# 3   2022.6  22068   822.8   960.0   703.7   361.9   941.4  115.7  171.8
# 4  10636.3  14397  3536.3  3967.2  2320.0  1141.3  3215.8  384.7  643.7
# [[-0.37574772 -0.33589708 -0.57070001 -0.33180084 -0.4351153  -0.68608742
#   -0.13882664 -0.44958874 -0.36008526]
#  [ 1.19924012 -0.48315182  1.14473196  0.98455823  0.79990984  0.8650543
#    0.66401891 -0.27809633  0.34976628]
#  [-0.18446517 -0.76485655 -0.54609356 -0.46884237 -0.63100796 -0.49108511
#   -0.39102534 -0.60224445 -0.68853914]
#  [-1.43844228  0.6481162  -1.01716572 -1.40498973 -1.21233816 -1.16457327
#   -1.28376177 -0.46528598 -1.12861338]
#  [ 1.2259343  -0.18430174  1.17200074  1.08060301  0.83964698  1.06721529
#    0.6934899   0.0625339   0.46273553]
#  [-0.39102805  2.66204455  0.09085021  0.07932373  0.3955559   0.03063913
#   -0.33286576 -0.06343649  0.68294126]
#  [ 0.3084029   0.05150118  0.22017521  0.33489213  0.80993934  1.17974966
#    0.39938849 -0.11504119  0.20374931]
#  [-0.61584072 -0.28055447 -0.83620754 -0.66192379 -0.88123767 -1.06148835
#   -0.65617736 -0.35148095 -0.7876823 ]
#  [ 1.57651587 -0.11561179  1.72729954  1.76366162  1.73201866  1.45149297
#    2.25640894  2.92531908  2.34409505]
#  [-1.30456925 -1.19728849 -1.38489083 -1.37548199 -1.41737163 -1.19091719
#   -1.21064936 -0.66267885 -1.07836735]]
# PCA(n_components=9)
# [8.01129553e+00 1.22149318e+00 6.07923991e-01 9.88894782e-02
#  3.86004507e-02 1.51746715e-02 4.88067443e-03 1.33610801e-03
#  4.05920593e-04]
# [8.01129553e-01 1.22149318e-01 6.07923991e-02 9.88894782e-03
#  3.86004507e-03 1.51746715e-03 4.88067443e-04 1.33610801e-04
#  4.05920593e-05]
# [8.01129553 1.22149318]
# None
# [0 1]
# None
#           0         1
# 0  0.362880 -0.196047
# 1 -0.001947  0.943648
# 2  0.364222  0.006565
# 3  0.369255 -0.028775
# 4  0.361258  0.111596
# 5  0.352799 -0.007144
# 6  0.370140 -0.118691
# 7  0.295099  0.061400
# 8  0.346765  0.199650
#           0         1         2  ...         6         7         8
# 0 -0.375748 -0.335897 -0.570700  ... -0.138827 -0.449589 -0.360085
# 1  1.199240 -0.483152  1.144732  ...  0.664019 -0.278096  0.349766
# 2 -0.184465 -0.764857 -0.546094  ... -0.391025 -0.602244 -0.688539
# 3 -1.438442  0.648116 -1.017166  ... -1.283762 -0.465286 -1.128613
# 4  1.225934 -0.184302  1.172001  ...  0.693490  0.062534  0.462736
# 5 -0.391028  2.662045  0.090850  ... -0.332866 -0.063436  0.682941
# 6  0.308403  0.051501  0.220175  ...  0.399388 -0.115041  0.203749
# 7 -0.615841 -0.280554 -0.836208  ... -0.656177 -0.351481 -0.787682
# 8  1.576516 -0.115612  1.727300  ...  2.256409  2.925319  2.344095
# 9 -1.304569 -1.197288 -1.384891  ... -1.210649 -0.662679 -1.078367
#
# [10 rows x 9 columns]
#           0         1
# 0  0.362880 -0.196047
# 1 -0.001947  0.943648
# 2  0.364222  0.006565
# 3  0.369255 -0.028775
# 4  0.361258  0.111596
# 5  0.352799 -0.007144
# 6  0.370140 -0.118691
# 7  0.295099  0.061400
# 8  0.346765  0.199650
#           0         1
# 0 -1.174241 -0.364178
# 1  2.095775 -0.654819
# 2 -1.399899 -0.870629
# 3 -3.265185  0.698849
# 4  2.386557 -0.337666
# 5  0.163901  2.802894
# 6  1.209012  0.048116
# 7 -2.084500 -0.322173
# 8  5.501759  0.105138
# 9 -3.433179 -1.105531
#   AREA       X1     X2      X3  ...      X8      X9     Gross       Avg
# 0   辽宁   5458.2  13000  1376.2  ...   123.7   399.7 -1.174241 -0.364178
# 1   山东  10550.0  11643  3502.5  ...   211.1   610.2  2.095775 -0.654819
# 2   河北   6076.6   9047  1406.7  ...    45.9   302.3 -1.399899 -0.870629
# 3   天津   2022.6  22068   822.8  ...   115.7   171.8 -3.265185  0.698849
# 4   江苏  10636.3  14397  3536.3  ...   384.7   643.7  2.386557 -0.337666
# 5   上海   5408.8  40627  2196.2  ...   320.5   709.0  0.163901  2.802894
# 6   浙江   7670.0  16570  2356.5  ...   294.2   566.9  1.209012  0.048116
# 7   福建   4682.0  13510  1047.1  ...   173.7   272.9 -2.084500 -0.322173
# 8   广东  11769.7  15030  4224.6  ...  1843.7  1201.6  5.501759  0.105138
# 9   广西   2455.4   5062   367.0  ...    15.1   186.7 -3.433179 -1.105531
#
# [10 rows x 12 columns]
# [stderr] <string>:44: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown


# ================================================================
# 8. 第8章 假设检验与方差分析（ANOVA）
# 源文件: 第8章-使用统计学方法进行检验和预测\假设检验与方差分析\方差分析.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\假设检验与方差分析
# ================================================================

# -*- coding: utf-8 -*-
"""
第8章 假设检验与方差分析（ANOVA）
==================================
项目内涵：检验分类变量(教育程度 edu_class、性别 gender)对连续型因变量(信用卡月均支出
         avg_exp)的影响是否显著，从单因素扩展到多因素含交互项。
技术方法：statsmodels ols + anova_lm，公式中 C() 表示分类变量。
数据源：creditcard_exp.csv（信用卡消费数据）。
关键步骤：1)读入并清洗(转字符串/浮点) → 2)单因素方差分析 avg_exp~C(edu_class)+C(gender)
         → 3)多因素含交互 avg_exp~C(edu_class)+C(gender)+C(edu_class)*C(gender)。
"""

# # 单因素方差分析


from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pandas as pd


data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')


df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')


formula = f'avg_exp ~ C(edu_class) + C(gender)'
anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)


# # 多因素方差分析


data = pd.read_csv('creditcard_exp.csv')
df = data[['avg_exp','edu_class','gender']].dropna(how='any',axis=0)
df['edu_class'] = df['edu_class'].astype('str')
df['gender'] = df['gender'].astype('str')
df['avg_exp'] = df['avg_exp'].apply(lambda x: 0 if x==' ' else x)
df['avg_exp'] = df['avg_exp'].astype('float')


formula = f'avg_exp ~ C(edu_class) + C(gender) + C(edu_class)*C(gender)'

anova = ols(formula=formula, data=df).fit()
anova_results = anova.summary()
print(anova_results)

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第8章 假设检验与方差分析（ANOVA）
# ==================================
# 项目内涵：检验分类变量(教育程度 edu_class、性别 gender)对连续型因变量(信用卡月均支出
#          avg_exp)的影响是否显著，从单因素扩展到多因素含交互项。
# 技术方法：statsmodels ols + anova_lm，公式中 C() 表示分类变量。
# 数据源：creditcard_exp.csv（信用卡消费数据）。
# 关键步骤：1)读入并清洗(转字符串/浮点) → 2)单因素方差分析 avg_exp~C(edu_class)+C(gender)
#          → 3)多因素含交互 avg_exp~C(edu_class)+C(gender)+C(edu_class)*C(gender)。
#
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.731
# Model:                            OLS   Adj. R-squared:                  0.720
# Method:                 Least Squares   F-statistic:                     64.69
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           2.69e-26
# Time:                        19:12:23   Log-Likelihood:                -713.08
# No. Observations:                 100   AIC:                             1436.
# Df Residuals:                      95   BIC:                             1449.
# Df Model:                           4                                         
# Covariance Type:            nonrobust                                         
# =====================================================================================
#                         coef    std err          t      P>|t|      [0.025      0.975]
# -------------------------------------------------------------------------------------
# Intercept            28.1190     73.264      0.384      0.702    -117.329     173.567
# C(edu_class)[T.1]   383.2751     89.384      4.288      0.000     205.826     560.724
# C(edu_class)[T.2]   976.9943    100.255      9.745      0.000     777.962    1176.026
# C(edu_class)[T.3]  1435.7083    103.378     13.888      0.000    1230.477    1640.939
# C(gender)[T.1]      -91.4020     77.717     -1.176      0.243    -245.691      62.887
# ==============================================================================
# Omnibus:                        6.407   Durbin-Watson:                   2.370
# Prob(Omnibus):                  0.041   Jarque-Bera (JB):                5.840
# Skew:                           0.512   Prob(JB):                       0.0539
# Kurtosis:                       3.594   Cond. No.                         5.91
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.743
# Model:                            OLS   Adj. R-squared:                  0.724
# Method:                 Least Squares   F-statistic:                     38.06
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           1.56e-24
# Time:                        19:12:23   Log-Likelihood:                -710.82
# No. Observations:                 100   AIC:                             1438.
# Df Residuals:                      92   BIC:                             1458.
# Df Model:                           7                                         
# Covariance Type:            nonrobust                                         
# ====================================================================================================
#                                        coef    std err          t      P>|t|      [0.025      0.975]
# ----------------------------------------------------------------------------------------------------
# Intercept                           24.3965     74.767      0.326      0.745    -124.097     172.890
# C(edu_class)[T.1]                  385.8773     92.520      4.171      0.000     202.125     569.629
# C(edu_class)[T.2]                  915.2349    109.204      8.381      0.000     698.346    1132.124
# C(edu_class)[T.3]                 1529.5444    116.230     13.160      0.000    1298.701    1760.388
# C(gender)[T.1]                     -24.3965    317.210     -0.077      0.939    -654.403     605.610
# C(edu_class)[T.1]:C(gender)[T.1]   -58.7153    350.140     -0.168      0.867    -754.125     636.694
# C(edu_class)[T.2]:C(gender)[T.1]   121.2551    344.727      0.352      0.726    -563.402     805.913
# C(edu_class)[T.3]:C(gender)[T.1]  -265.2554    343.576     -0.772      0.442    -947.628     417.117
# ==============================================================================
# Omnibus:                       16.354   Durbin-Watson:                   2.368
# Prob(Omnibus):                  0.000   Jarque-Bera (JB):               22.080
# Skew:                           0.797   Prob(JB):                     1.60e-05
# Kurtosis:                       4.662   Cond. No.                         24.4
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.


# ================================================================
# 9. 第8章 列联表检验 —— 卡方独立性检验
# 源文件: 第8章-使用统计学方法进行检验和预测\列联表检验\列联表分析.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\列联表检验
# ================================================================

# -*- coding: utf-8 -*-
"""
第8章 列联表检验 —— 卡方独立性检验
====================================
项目内涵：检验两个分类变量(是否破产 bankruptcy_ind、是否坏账 bad_ind)是否独立，
         若显著相关则说明破产状态对坏账有解释力。
技术方法：pd.crosstab(列联表)、div(行百分比)、scipy.stats.chi2_contingency(卡方检验)。
数据源：accepts.csv（信贷接受记录，含破产标识与坏账标识）。
关键步骤：1)构建列联表(含边际) → 2)计算行百分比 → 3)卡方独立性检验输出卡方值/p值/自由度/期望频数。
"""

import pandas as pd
accepts =pd.read_csv ( 'accepts.csv' )
cross_table=pd.crosstab(accepts.bankruptcy_ind,accepts.bad_ind, margins=True)
cross_table


cross_table_rowpct = cross_table.div(cross_table ["All"] ,axis = 0)
cross_table_rowpct


# 打印结果
from scipy import stats
print(
    "chisq = %6.4f\np-value = %6.4f\ndof = %d\nexpected_freq = %s"
    %stats.chi2_contingency (cross_table))

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第8章 列联表检验 —— 卡方独立性检验
# ====================================
# 项目内涵：检验两个分类变量(是否破产 bankruptcy_ind、是否坏账 bad_ind)是否独立，
#          若显著相关则说明破产状态对坏账有解释力。
# 技术方法：pd.crosstab(列联表)、div(行百分比)、scipy.stats.chi2_contingency(卡方检验)。
# 数据源：accepts.csv（信贷接受记录，含破产标识与坏账标识）。
# 关键步骤：1)构建列联表(含边际) → 2)计算行百分比 → 3)卡方独立性检验输出卡方值/p值/自由度/期望频数。
#
# bad_ind            0     1   All
# bankruptcy_ind                  
# N               4163  1017  5180
# Y                345   103   448
# All             4508  1120  5628
# bad_ind                0         1  All
# bankruptcy_ind                         
# N               0.803668  0.196332  1.0
# Y               0.770089  0.229911  1.0
# All             0.800995  0.199005  1.0
# chisq = 2.9167
# p-value = 0.5719
# dof = 4
# expected_freq = [[4149.15422886 1030.84577114 5180.        ]
#  [ 358.84577114   89.15422886  448.        ]
#  [4508.         1120.         5628.        ]]


# ================================================================
# 10. 第8章 线性回归（statsmodels OLS）
# 源文件: 第8章-使用统计学方法进行检验和预测\线性回归\线性回归.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\线性回归
# ================================================================

# -*- coding: utf-8 -*-
"""
第8章 线性回归（statsmodels OLS）
=================================
项目内涵：以信用卡月均支出 avg_exp 为因变量，完整走一遍线性回归建模流程：数据清洗 →
         相关分析 → 建模 → 模型调优(共线性/同方差/正态性/高次项/交互项)，体现"诊断-改进"
         的迭代思想。
技术方法：read_excel、drop_duplicates、fillna、map 编码、get_dummies 哑变量、
         zscore 异常检测、ols、VIF 方差膨胀因子、残差图、probplot 正态性、log 变换。
数据源：LR_practice.xlsx（信用卡客户支出及人口学变量）。
关键步骤：1)清洗(删无用列/重复/缺失/编码/异常值/哑变量) → 2)相关分析与散点图
         → 3)model_1 初始回归 → 4)VIF 去共线性 model_2 → 5)残差图查同方差
         → 6)probplot 查正态性 → 7)log 变换 model_3 → 8)加高次项 model_4
         → 9)加交互项 model_5。
"""

try:
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"
except Exception:
    pass


# ## 读取变量


import numpy as np
import pandas as pd


#读取数据
data_raw = pd.read_excel('LR_practice.xlsx')
data_raw.head()


data_raw.tail()


data_raw.head(2)


#数据基本信息
data_raw.info()


# ## 数据清洗


# ### 删除无用变量


#变量'id','Acc','edad2'
data_raw.drop(['id','Acc','edad2'], axis=1, inplace=True)


data_raw.head(2)


# ### 重复值


#删除重复值
data_raw.drop_duplicates(inplace=True)


# ### 缺失值


#查看缺失情况
data_raw.isnull().mean()


data_raw.isnull().sum()


# #### 填补缺失值


data_raw['avg_exp'].mean()


#avg_exp
data_raw['avg_exp'] = data_raw['avg_exp'].fillna(data_raw['avg_exp'].mean())


data_raw.isnull().mean()


# #### 数据编码和缺失值


#方法1：gender
data_raw['gender'] = data_raw['gender'].map({'Male':1, 'Female':0})


data_raw.head(2)


#方法2：edu_class
data_raw['edu_class'].unique()


label = data_raw['edu_class'].unique().tolist()
label


label.index('中学')


#对原数据进行编码
data_raw['edu_class'] = data_raw['edu_class'].apply(lambda x: label.index(x))


data_raw.head()


data_raw['edu_class'].value_counts()


# ### 异常值


# #### 箱线图


import seaborn as sns


# dist_avg_income
sns.boxplot(data=data_raw['dist_avg_income'])


# #### 3倍标准差


from scipy import stats


#标准化数据(Age)
z = stats.zscore(data_raw['Age'])
z


(z>3)|(z<-3)


#寻找异常数据的索引
z[(z>3)|(z<-3)]


#查看异常数据的值
data_raw['Age'].iloc[40]


# 如何填补999这个异常的年龄数据呢？


data_raw['Age'].mean()


data_raw['Age'].drop(index=40).mean()


#将异常值使用除异常值之外的数据的均值进行填补
data_raw['Age'].iloc[40] = data_raw['Age'].drop(index=40).mean()


# ### 哑变量转换


data_raw.head()


#edu_class
dummy = pd.get_dummies(data=data_raw['edu_class'], prefix='edu', drop_first=True)
dummy


#合并到原数据
data = pd.concat([data_raw, dummy], axis=1)
data.head()


# ## 相关分析


# ### 相关系数


data.corr()


#分类变量
data.corr(method='kendall')


# ### 散点图


import matplotlib.pyplot as plt


# avg_exp和Income
plt.scatter(data['Income'], data['avg_exp'])


# ## 回归分析


# ### 回归模型


from statsmodels.formula.api import ols


data.columns


data.head()


# model_1 = ols(LR1, data)
# model_1 = model_1.fit()


LR1 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+ dist_avg_income+edu_1+ edu_2+edu_3+ edu_4'
model_1 = ols(LR1, data).fit()


model_1.summary()


#常用接口
dir(model_1)


model_1.resid


# ### 模型调优


# #### 共线性


data.head()


def vif(df, y_col):
    x_cols = list(df.columns)
    x_cols.remove(y_col)
    formula = y_col + '~' + '+'.join(x_cols)
    rsquared = ols(formula, df).fit().rsquared
    return 1. / (1. - rsquared)

exog = data[['gender','Age','Income','Ownrent','Selfempl','dist_home_val','dist_avg_income','edu_class']]

for y_col in exog.columns:
    print(y_col, '\t', vif(df=exog, y_col=y_col))


#重新拟合模型
LR2 = 'avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_2 = ols(LR2, data).fit()
model_2.summary()


# #### 同方差


# 残差图：   
# - 一元回归：横坐标是X，纵坐标是残差
# - 多元回归：横坐标是Y的拟合值，纵坐标是残差


#残差图
plt.scatter(model_2.predict(data), model_2.resid)


# #### 正态性


res = stats.probplot(model_2.resid, plot=plt)


data['ln_avg_exp'] = np.log(data['avg_exp'])
data.head()


#重新拟合模型
LR3 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4'
model_3 = ols(LR3, data).fit()
model_3.summary()


# ![image.png](attachment:image.png)


res = stats.probplot(model_3.resid, plot=plt)


# #### 高次项


data['Age_sq'] = data['Age']**2
data.head()


#年龄
LR4 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq'
model_4 = ols(LR4, data).fit()
model_4.summary()


# #### 交互项


data['Age_gender'] = data['Age']*data['gender']
data.head()


LR5 = 'ln_avg_exp~gender+Age+ Income+ Ownrent+ Selfempl+dist_home_val+edu_1+ edu_2+edu_3+ edu_4 + Age_sq+Age_gender'
model_5 = ols(LR5, data).fit()
model_5.summary()

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第8章 线性回归（statsmodels OLS）
# =================================
# 项目内涵：以信用卡月均支出 avg_exp 为因变量，完整走一遍线性回归建模流程：数据清洗 →
#          相关分析 → 建模 → 模型调优(共线性/同方差/正态性/高次项/交互项)，体现"诊断-改进"
#          的迭代思想。
# 技术方法：read_excel、drop_duplicates、fillna、map 编码、get_dummies 哑变量、
#          zscore 异常检测、ols、VIF 方差膨胀因子、残差图、probplot 正态性、log 变换。
# 数据源：LR_practice.xlsx（信用卡客户支出及人口学变量）。
# 关键步骤：1)清洗(删无用列/重复/缺失/编码/异常值/哑变量) → 2)相关分析与散点图
#          → 3)model_1 初始回归 → 4)VIF 去共线性 model_2 → 5)残差图查同方差
#          → 6)probplot 查正态性 → 7)log 变换 model_3 → 8)加高次项 model_4
#          → 9)加交互项 model_5。
#
#    id  Acc  avg_exp gender  ...  dist_home_val  dist_avg_income  edad2  edu_class
# 0  19    1  1217.03   Male  ...          99.93        15.932789   1600        研究生
# 1   5    1  1251.50   Male  ...          49.88        15.796316   1024         大学
# 2  86    1   856.57   Male  ...          16.10        11.275632   1681        研究生
# 3  50    1  1321.83   Male  ...         100.39        13.346474    784         大学
# 4  67    1   816.03   Male  ...         119.76        10.332263   1681        研究生
#
# [5 rows x 12 columns]
#     id  Acc  avg_exp  gender  ...  dist_home_val  dist_avg_income  edad2  edu_class
# 71  53    1   491.04  Female  ...          36.81         4.349158    441         中学
# 72  83    1   468.61  Female  ...          66.75         4.551105    400         中学
# 73  43    1   593.92  Female  ...         124.23         5.040632    900         中学
# 74  60    1   418.78  Female  ...          34.46         3.828842    441         中学
# 75  28    1   163.18  Female  ...          63.27         3.997789    484      小学及以下
#
# [5 rows x 12 columns]
#    id  Acc  avg_exp gender  ...  dist_home_val  dist_avg_income  edad2  edu_class
# 0  19    1  1217.03   Male  ...          99.93        15.932789   1600        研究生
# 1   5    1  1251.50   Male  ...          49.88        15.796316   1024         大学
#
# [2 rows x 12 columns]
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 76 entries, 0 to 75
# Data columns (total 12 columns):
#  #   Column           Non-Null Count  Dtype  
# ---  ------           --------------  -----  
#  0   id               76 non-null     int64  
#  1   Acc              76 non-null     int64  
#  2   avg_exp          70 non-null     float64
#  3   gender           76 non-null     object 
#  4   Age              76 non-null     int64  
#  5   Income           76 non-null     float64
#  6   Ownrent          76 non-null     int64  
#  7   Selfempl         76 non-null     int64  
#  8   dist_home_val    76 non-null     float64
#  9   dist_avg_income  76 non-null     float64
#  10  edad2            76 non-null     int64  
#  11  edu_class        75 non-null     object 
# dtypes: float64(4), int64(6), object(2)
# memory usage: 7.2+ KB
# None
# None
#    avg_exp gender  Age  ...  dist_home_val  dist_avg_income  edu_class
# 0  1217.03   Male   40  ...          99.93        15.932789        研究生
# 1  1251.50   Male   32  ...          49.88        15.796316         大学
#
# [2 rows x 9 columns]
# None
# avg_exp            0.078947
# gender             0.000000
# Age                0.000000
# Income             0.000000
# Ownrent            0.000000
# Selfempl           0.000000
# dist_home_val      0.000000
# dist_avg_income    0.000000
# edu_class          0.013158
# dtype: float64
# avg_exp            6
# gender             0
# Age                0
# Income             0
# Ownrent            0
# Selfempl           0
# dist_home_val      0
# dist_avg_income    0
# edu_class          1
# dtype: int64
# 983.6554285714284
# avg_exp            0.000000
# gender             0.000000
# Age                0.000000
# Income             0.000000
# Ownrent            0.000000
# Selfempl           0.000000
# dist_home_val      0.000000
# dist_avg_income    0.000000
# edu_class          0.013158
# dtype: float64
#    avg_exp  gender  Age  ...  dist_home_val  dist_avg_income  edu_class
# 0  1217.03       1   40  ...          99.93        15.932789        研究生
# 1  1251.50       1   32  ...          49.88        15.796316         大学
#
# [2 rows x 9 columns]
# ['研究生' '大学' '中学' '小学及以下' nan]
# ['研究生', '大学', '中学', '小学及以下', nan]
# 2
#    avg_exp  gender  Age  ...  dist_home_val  dist_avg_income  edu_class
# 0  1217.03       1   40  ...          99.93        15.932789          0
# 1  1251.50       1   32  ...          49.88        15.796316          1
# 2   856.57       1   41  ...          16.10        11.275632          0
# 3  1321.83       1   28  ...         100.39        13.346474          1
# 4   816.03       1   41  ...         119.76        10.332263          0
#
# [5 rows x 9 columns]
# edu_class
# 2    25
# 1    23
# 0    22
# 3     5
# 4     1
# Name: count, dtype: int64
# [-3.57230069e-02 -1.08121634e-01 -2.66731785e-02 -1.44320948e-01
#  -2.66731785e-02 -9.90718059e-02 -6.28724922e-02  1.85759636e-02
#  -3.57230069e-02 -8.57352166e-03 -1.62420605e-01 -9.00219774e-02
#  -1.44320948e-01 -5.38226638e-02 -1.26221291e-01 -9.00219774e-02
#  -3.57230069e-02 -7.19223206e-02 -1.44320948e-01 -1.17171463e-01
#  -1.76233501e-02 -6.28724922e-02 -1.80520262e-01 -1.71470433e-01
#  -8.57352166e-03 -1.53370776e-01 -9.90718059e-02 -1.44320948e-01
#  -2.66731785e-02 -1.35271120e-01 -9.90718059e-02 -1.71470433e-01
#  -1.71470433e-01 -7.19223206e-02 -1.71470433e-01 -1.62420605e-01
#  -9.90718059e-02 -1.26221291e-01 -1.80520262e-01 -1.71470433e-01
#   8.64306245e+00 -1.62420605e-01 -1.80520262e-01 -6.28724922e-02
#  -1.98619918e-01  1.00024419e-01 -5.38226638e-02 -1.89570090e-01
#  -9.90718059e-02 -1.17171463e-01 -9.00219774e-02 -1.89570090e-01
#  -2.07669747e-01 -1.17171463e-01 -1.35271120e-01 -9.90718059e-02
#  -1.62420605e-01 -8.57352166e-03 -1.35271120e-01 -1.35271120e-01
#  -1.62420605e-01 -8.09721490e-02 -1.53370776e-01 -1.53370776e-01
#  -1.98619918e-01 -1.80520262e-01 -9.00219774e-02 -7.19223206e-02
#  -1.53370776e-01 -8.09721490e-02 -1.26221291e-01 -2.07669747e-01
#  -2.16719575e-01 -1.26221291e-01 -2.07669747e-01 -1.98619918e-01]
# [False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False  True False False False False False False False
#  False False False False False False False False False False False False
#  False False False False False False False False False False False False
#  False False False False]
# [8.64306245]
# 999
# 43.94736842105263
# 31.213333333333335
#    avg_exp  gender   Age  ...  dist_home_val  dist_avg_income  edu_class
# 0  1217.03       1  40.0  ...          99.93        15.932789          0
# 1  1251.50       1  32.0  ...          49.88        15.796316          1
# 2   856.57       1  41.0  ...          16.10        11.275632          0
# 3  1321.83       1  28.0  ...         100.39        13.346474          1
# 4   816.03       1  41.0  ...         119.76        10.332263          0
#
# [5 rows x 9 columns]
#     edu_1  edu_2  edu_3  edu_4
# 0   False  False  False  False
# 1    True  False  False  False
# 2   False  False  False  False
# 3    True  False  False  False
# 4   False  False  False  False
# ..    ...    ...    ...    ...
# 71  False   True  False  False
# 72  False   True  False  False
# 73  False   True  False  False
# 74  False   True  False  False
# 75  False  False   True  False
#
# [76 rows x 4 columns]
#    avg_exp  gender   Age    Income  ...  edu_1  edu_2  edu_3  edu_4
# 0  1217.03       1  40.0  16.03515  ...  False  False  False  False
# 1  1251.50       1  32.0  15.84750  ...   True  False  False  False
# 2   856.57       1  41.0  11.47285  ...  False  False  False  False
# 3  1321.83       1  28.0  13.40915  ...   True  False  False  False
# 4   816.03       1  41.0  10.03015  ...  False  False  False  False
#
# [5 rows x 13 columns]
#                       avg_exp    gender  ...     edu_3         edu_4
# avg_exp          1.000000e+00  0.203600  ... -0.193775 -8.151683e-17
# gender           2.035997e-01  1.000000  ... -0.158590 -6.900656e-02
# Age              2.550378e-01  0.333769  ... -0.061522 -4.190919e-17
# Income           6.189981e-01  0.719685  ... -0.300040 -1.535058e-01
# Ownrent          2.964665e-01  0.430469  ... -0.196988 -8.571429e-02
# Selfempl         7.544430e-03  0.046657  ...  0.315952  3.944053e-01
# dist_home_val    2.993244e-01  0.190720  ... -0.249559  1.443979e-01
# dist_avg_income  6.398076e-01  0.705310  ... -0.332764 -1.809021e-01
# edu_class       -6.524726e-01 -0.373224  ...  0.485764  3.294850e-01
# edu_1           -1.600887e-02  0.126663  ... -0.174816 -7.606684e-02
# edu_2           -5.176081e-01 -0.291216  ... -0.185798 -8.084521e-02
# edu_3           -1.937752e-01 -0.158590  ...  1.000000 -3.064257e-02
# edu_4           -8.151683e-17 -0.069007  ... -0.030643  1.000000e+00
#
# [13 rows x 13 columns]
#                   avg_exp    gender       Age  ...     edu_2     edu_3     edu_4
# avg_exp          1.000000  0.167236  0.230203  ... -0.510726 -0.111642  0.026024
# gender           0.167236  1.000000  0.302455  ... -0.291216 -0.158590 -0.069007
# Age              0.230203  0.302455  1.000000  ... -0.208202 -0.042492  0.019810
# Income           0.421110  0.558598  0.289227  ... -0.302690 -0.297259 -0.149244
# Ownrent          0.290705  0.430469  0.355849  ... -0.168620 -0.196988 -0.085714
# Selfempl         0.064150  0.046657  0.098595  ... -0.101123  0.315952  0.394405
# dist_home_val    0.160775  0.127615  0.029280  ... -0.260723 -0.193864  0.118962
# dist_avg_income  0.439403  0.556359  0.278515  ... -0.315280 -0.315154 -0.157896
# edu_class       -0.561243 -0.351901 -0.245094  ...  0.602196  0.403825  0.190994
# edu_1            0.072620  0.126663 -0.062241  ... -0.461223 -0.174816 -0.076067
# edu_2           -0.510726 -0.291216 -0.208202  ...  1.000000 -0.185798 -0.080845
# edu_3           -0.111642 -0.158590 -0.042492  ... -0.185798  1.000000 -0.030643
# edu_4            0.026024 -0.069007  0.019810  ... -0.080845 -0.030643  1.000000
#
# [13 rows x 13 columns]
# Index(['avg_exp', 'gender', 'Age', 'Income', 'Ownrent', 'Selfempl',
#        'dist_home_val', 'dist_avg_income', 'edu_class', 'edu_1', 'edu_2',
#        'edu_3', 'edu_4'],
#       dtype='object')
#    avg_exp  gender   Age    Income  ...  edu_1  edu_2  edu_3  edu_4
# 0  1217.03       1  40.0  16.03515  ...  False  False  False  False
# 1  1251.50       1  32.0  15.84750  ...   True  False  False  False
# 2   856.57       1  41.0  11.47285  ...  False  False  False  False
# 3  1321.83       1  28.0  13.40915  ...   True  False  False  False
# 4   816.03       1  41.0  10.03015  ...  False  False  False  False
#
# [5 rows x 13 columns]
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.720
# Model:                            OLS   Adj. R-squared:                  0.671
# Method:                 Least Squares   F-statistic:                     14.93
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           8.36e-14
# Time:                        19:12:33   Log-Likelihood:                -519.52
# No. Observations:                  76   AIC:                             1063.
# Df Residuals:                      64   BIC:                             1091.
# Df Model:                          11                                         
# Covariance Type:            nonrobust                                         
# ===================================================================================
#                       coef    std err          t      P>|t|      [0.025      0.975]
# -----------------------------------------------------------------------------------
# Intercept         535.9565    223.038      2.403      0.019      90.387     981.526
# edu_1[T.True]    -262.5083     82.890     -3.167      0.002    -428.100     -96.916
# edu_2[T.True]    -495.1400     92.266     -5.366      0.000    -679.462    -310.818
# edu_3[T.True]    -292.5211    156.617     -1.868      0.066    -605.400      20.358
# edu_4[T.True]      49.3783    294.618      0.168      0.867    -539.188     637.945
# gender           -447.4828     97.100     -4.608      0.000    -641.463    -253.503
# Age                 0.6121      4.779      0.128      0.898      -8.936      10.160
# Income           -119.1929     72.411     -1.646      0.105    -263.850      25.464
# Ownrent            41.3184     76.416      0.541      0.591    -111.341     193.977
# Selfempl          153.7000    129.424      1.188      0.239    -104.853     412.253
# dist_home_val       0.1579      0.859      0.184      0.855      -1.557       1.873
# dist_avg_income   211.5250     71.122      2.974      0.004      69.442     353.608
# ==============================================================================
# Omnibus:                        0.894   Durbin-Watson:                   2.112
# Prob(Omnibus):                  0.640   Jarque-Bera (JB):                0.613
# Skew:                          -0.219   Prob(JB):                        0.736
# Kurtosis:                       3.044   Cond. No.                     1.00e+03
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# [2] The condition number is large,  1e+03. This might indicate that there are
# strong multicollinearity or other numerical problems.
# ['HC0_se', 'HC1_se', 'HC2_se', 'HC3_se', '_HCCM', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abat_diagonal', '_cache', '_data_attr', '_data_in_cache', '_get_robustcov_results', '_get_wald_nonlinear', '_is_nested', '_nobs_int', '_summary_cache', '_transform_predict_exog', '_use_t', '_wexog_singular_values', 'aic', 'bic', 'bse', 'centered_tss', 'compare_f_test', 'compare_lm_test', 'compare_lr_test', 'condition_number', 'conf_int', 'conf_int_el', 'cov_HC0', 'cov_HC1', 'cov_HC2', 'cov_HC3', 'cov_kwds', 'cov_params', 'cov_type', 'df_model', 'df_resid', 'diagn', 'eigenvals', 'el_test', 'ess', 'f_pvalue', 'f_test', 'fittedvalues', 'fvalue', 'get_influence', 'get_prediction', 'get_robustcov_results', 'info_criteria', 'initialize', 'k_constant', 'llf', 'load', 'model', 'mse_model', 'mse_resid', 'mse_total', 'nobs', 'normalized_cov_params', 'outlier_test', 'params', 'predict', 'pvalues', 'remove_data', 'resid', 'resid_pearson', 'rsquared', 'rsquared_adj', 'save', 'scale', 'ssr', 'summary', 'summary2', 't_test', 't_test_pairwise', 'tvalues', 'uncentered_tss', 'use_t', 'wald_test', 'wald_test_terms', 'wresid']
# 0    -565.630770
# 1     -95.652529
# 2    -318.456003
# 3     196.720056
# 4    -460.157387
#          ...    
# 71     -5.047028
# 72    -93.635981
# 73    -29.075904
# 74    -33.779180
# 75   -494.515263
# Length: 76, dtype: float64
#    avg_exp  gender   Age    Income  ...  edu_1  edu_2  edu_3  edu_4
# 0  1217.03       1  40.0  16.03515  ...  False  False  False  False
# 1  1251.50       1  32.0  15.84750  ...   True  False  False  False
# 2   856.57       1  41.0  11.47285  ...  False  False  False  False
# 3  1321.83       1  28.0  13.40915  ...   True  False  False  False
# 4   816.03       1  41.0  10.03015  ...  False  False  False  False
#
# [5 rows x 13 columns]
# gender 	 2.2091919746839945
# Age 	 1.3708810657506336
# Income 	 64.76239230667088
# Ownrent 	 1.6682817716496414
# Selfempl 	 1.288764018740877
# dist_home_val 	 1.165431243043153
# dist_avg_income 	 64.13992249399934
# edu_class 	 1.9945867708908815
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:                avg_exp   R-squared:                       0.681
# Model:                            OLS   Adj. R-squared:                  0.632
# Method:                 Least Squares   F-statistic:                     13.87
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           1.07e-12
# Time:                        19:12:34   Log-Likelihood:                -524.44
# No. Observations:                  76   AIC:                             1071.
# Df Residuals:                      65   BIC:                             1097.
# Df Model:                          10                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------
# Intercept       659.2949    231.997      2.842      0.006     195.965    1122.625
# edu_1[T.True]  -258.0157     87.735     -2.941      0.005    -433.235     -82.796
# edu_2[T.True]  -507.3032     97.579     -5.199      0.000    -702.182    -312.424
# edu_3[T.True]  -377.0725    163.045     -2.313      0.024    -702.696     -51.449
# edu_4[T.True]   -89.4791    307.950     -0.291      0.772    -704.497     525.539
# gender         -451.7062    102.782     -4.395      0.000    -656.976    -246.436
# Age               1.1647      5.056      0.230      0.819      -8.932      11.262
# Income           90.5062     17.456      5.185      0.000      55.644     125.369
# Ownrent           3.8211     79.788      0.048      0.962    -155.526     163.168
# Selfempl         69.9220    133.727      0.523      0.603    -197.149     336.993
# dist_home_val     0.4438      0.903      0.491      0.625      -1.360       2.248
# ==============================================================================
# Omnibus:                        1.477   Durbin-Watson:                   1.892
# Prob(Omnibus):                  0.478   Jarque-Bera (JB):                0.850
# Skew:                           0.153   Prob(JB):                        0.654
# Kurtosis:                       3.418   Cond. No.                         979.
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
#    avg_exp  gender   Age    Income  ...  edu_2  edu_3  edu_4  ln_avg_exp
# 0  1217.03       1  40.0  16.03515  ...  False  False  False    7.104169
# 1  1251.50       1  32.0  15.84750  ...  False  False  False    7.132098
# 2   856.57       1  41.0  11.47285  ...  False  False  False    6.752936
# 3  1321.83       1  28.0  13.40915  ...  False  False  False    7.186772
# 4   816.03       1  41.0  10.03015  ...  False  False  False    6.704451
#
# [5 rows x 14 columns]
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:             ln_avg_exp   R-squared:                       0.614
# Model:                            OLS   Adj. R-squared:                  0.554
# Method:                 Least Squares   F-statistic:                     10.33
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           3.57e-10
# Time:                        19:12:34   Log-Likelihood:                -11.749
# No. Observations:                  76   AIC:                             45.50
# Df Residuals:                      65   BIC:                             71.14
# Df Model:                          10                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------
# Intercept         6.6463      0.273     24.368      0.000       6.102       7.191
# edu_1[T.True]    -0.1870      0.103     -1.813      0.074      -0.393       0.019
# edu_2[T.True]    -0.5625      0.115     -4.903      0.000      -0.792      -0.333
# edu_3[T.True]    -0.7905      0.192     -4.124      0.000      -1.173      -0.408
# edu_4[T.True]    -0.2752      0.362     -0.760      0.450      -0.998       0.448
# gender           -0.3841      0.121     -3.179      0.002      -0.625      -0.143
# Age               0.0023      0.006      0.392      0.696      -0.010       0.014
# Income            0.0649      0.021      3.162      0.002       0.024       0.106
# Ownrent           0.0743      0.094      0.792      0.431      -0.113       0.262
# Selfempl          0.3216      0.157      2.046      0.045       0.008       0.636
# dist_home_val    -0.0005      0.001     -0.444      0.658      -0.003       0.002
# ==============================================================================
# Omnibus:                       10.941   Durbin-Watson:                   1.800
# Prob(Omnibus):                  0.004   Jarque-Bera (JB):               18.504
# Skew:                          -0.485   Prob(JB):                     9.59e-05
# Kurtosis:                       5.214   Cond. No.                         979.
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
#    avg_exp  gender   Age    Income  ...  edu_3  edu_4  ln_avg_exp  Age_sq
# 0  1217.03       1  40.0  16.03515  ...  False  False    7.104169  1600.0
# 1  1251.50       1  32.0  15.84750  ...  False  False    7.132098  1024.0
# 2   856.57       1  41.0  11.47285  ...  False  False    6.752936  1681.0
# 3  1321.83       1  28.0  13.40915  ...  False  False    7.186772   784.0
# 4   816.03       1  41.0  10.03015  ...  False  False    6.704451  1681.0
#
# [5 rows x 15 columns]
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:             ln_avg_exp   R-squared:                       0.689
# Model:                            OLS   Adj. R-squared:                  0.636
# Method:                 Least Squares   F-statistic:                     12.89
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           1.90e-12
# Time:                        19:12:34   Log-Likelihood:                -3.5070
# No. Observations:                  76   AIC:                             31.01
# Df Residuals:                      64   BIC:                             58.98
# Df Model:                          11                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------
# Intercept         4.4947      0.600      7.496      0.000       3.297       5.692
# edu_1[T.True]    -0.1415      0.094     -1.505      0.137      -0.329       0.046
# edu_2[T.True]    -0.5674      0.104     -5.469      0.000      -0.775      -0.360
# edu_3[T.True]    -0.8177      0.173     -4.714      0.000      -1.164      -0.471
# edu_4[T.True]    -0.4300      0.330     -1.304      0.197      -1.089       0.229
# gender           -0.3972      0.109     -3.634      0.001      -0.616      -0.179
# Age               0.1400      0.035      3.957      0.000       0.069       0.211
# Income            0.0485      0.019      2.551      0.013       0.011       0.087
# Ownrent           0.1197      0.086      1.398      0.167      -0.051       0.291
# Selfempl          0.3098      0.142      2.179      0.033       0.026       0.594
# dist_home_val -7.356e-05      0.001     -0.076      0.940      -0.002       0.002
# Age_sq           -0.0020      0.001     -3.937      0.000      -0.003      -0.001
# ==============================================================================
# Omnibus:                        8.638   Durbin-Watson:                   1.582
# Prob(Omnibus):                  0.013   Jarque-Bera (JB):               14.313
# Skew:                          -0.339   Prob(JB):                     0.000780
# Kurtosis:                       5.015   Cond. No.                     2.15e+04
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# [2] The condition number is large, 2.15e+04. This might indicate that there are
# strong multicollinearity or other numerical problems.
#    avg_exp  gender   Age    Income  ...  edu_4  ln_avg_exp  Age_sq  Age_gender
# 0  1217.03       1  40.0  16.03515  ...  False    7.104169  1600.0        40.0
# 1  1251.50       1  32.0  15.84750  ...  False    7.132098  1024.0        32.0
# 2   856.57       1  41.0  11.47285  ...  False    6.752936  1681.0        41.0
# 3  1321.83       1  28.0  13.40915  ...  False    7.186772   784.0        28.0
# 4   816.03       1  41.0  10.03015  ...  False    6.704451  1681.0        41.0
#
# [5 rows x 16 columns]
#                             OLS Regression Results                            
# ==============================================================================
# Dep. Variable:             ln_avg_exp   R-squared:                       0.713
# Model:                            OLS   Adj. R-squared:                  0.658
# Method:                 Least Squares   F-statistic:                     13.03
# Date:                Mon, 12 Oct 2026   Prob (F-statistic):           6.86e-13
# Time:                        19:12:34   Log-Likelihood:               -0.50019
# No. Observations:                  76   AIC:                             27.00
# Df Residuals:                      63   BIC:                             57.30
# Df Model:                          12                                         
# Covariance Type:            nonrobust                                         
# =================================================================================
#                     coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------
# Intercept         4.5002      0.581      7.747      0.000       3.339       5.661
# edu_1[T.True]    -0.1374      0.091     -1.509      0.136      -0.319       0.045
# edu_2[T.True]    -0.5555      0.101     -5.520      0.000      -0.757      -0.354
# edu_3[T.True]    -0.8230      0.168     -4.897      0.000      -1.159      -0.487
# edu_4[T.True]    -0.4744      0.320     -1.482      0.143      -1.114       0.165
# gender            0.5339      0.422      1.264      0.211      -0.310       1.378
# Age               0.1331      0.034      3.867      0.000       0.064       0.202
# Income            0.0518      0.018      2.802      0.007       0.015       0.089
# Ownrent           0.1088      0.083      1.309      0.195      -0.057       0.275
# Selfempl          0.3698      0.140      2.637      0.011       0.090       0.650
# dist_home_val -1.754e-05      0.001     -0.019      0.985      -0.002       0.002
# Age_sq           -0.0018      0.001     -3.647      0.001      -0.003      -0.001
# Age_gender       -0.0276      0.012     -2.278      0.026      -0.052      -0.003
# ==============================================================================
# Omnibus:                        7.398   Durbin-Watson:                   1.573
# Prob(Omnibus):                  0.025   Jarque-Bera (JB):               12.777
# Skew:                          -0.194   Prob(JB):                      0.00168
# Kurtosis:                       4.971   Cond. No.                     2.15e+04
# ==============================================================================
#
# Notes:
# [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
# [2] The condition number is large, 2.15e+04. This might indicate that there are
# strong multicollinearity or other numerical problems.
# [stderr] <string>:41: FutureWarning: ChainedAssignmentError: behaviour will change in pandas 3.0!
# [stderr] You are setting values through chained assignment. Currently this works in certain cases, but when using Copy-on-Write (which will become the default behaviour in pandas 3.0) this will never work to update the original DataFrame or Series, because the intermediate object on which we are setting values will behave as a copy.
# [stderr] A typical example is when you are setting values in a column of a DataFrame, like:
# [stderr] 
# [stderr] df["col"][row_indexer] = value
# [stderr] 
# [stderr] Use `df.loc[row_indexer, "col"] = values` instead, to perform the assignment in a single step and ensure this keeps updating the original `df`.
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] 
# [stderr] <string>:41: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] <string>:41: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '31.213333333333335' has dtype incompatible with int64, please explicitly cast to a compatible dtype first.


# ================================================================
# 11. 第8章 逻辑回归（电信客户流失预测）
# 源文件: 第8章-使用统计学方法进行检验和预测\逻辑回归\逻辑回归.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第8章-使用统计学方法进行检验和预测\逻辑回归
# ================================================================

# -*- coding: utf-8 -*-
"""
第8章 逻辑回归（电信客户流失预测）
===================================
项目内涵：预测电信客户是否流失(churn, 0/1)，从一元逻辑回归到多元逻辑回归，含特征筛选、
         模型评估(ROC/AUC/约登指数最优阈值)与共线性诊断，是典型的二分类评分卡场景。
技术方法：pd.crosstab 卡方检验、smf.logit、train/test 划分、predict 概率、
         metrics.roc_curve/auc、约登指数(tpr-fpr)选阈值、前向选择 forward_select、VIF。
数据源：telecom_churn.csv（电信客户流失及行为变量）。
关键步骤：1)交叉表+卡方看 posTrend 与 churn 相关 → 2)一元 logit(churn~duration)
         → 3)ROC/AUC/最优阈值 → 4)前向选择筛连续变量 → 5)卡方筛分类变量
         → 6)多元 logit 建模 → 7)评估 → 8)VIF 共线性诊断。
"""

# 变量说明：
# - subscriberID="个人客户的ID"
# - churn="是否流失：1=流失";
# - gender="性别"
# - Age="年龄"
# - edu_class="教育水平"
# - incomeCode="用户居住区域平均收入的代码"
# - duration="在网时长"
# - feton="是否注册飞信"
# - peakMinAv="统计期间内最高单月通话时长"
# - peakMinDiff="统计期间结束月份与开始月份相比通话时长增加数量"
# - posTrend="该用户通话时长是否呈现出上升态势：是=1"
# - negTrend="该用户通话时长是否呈现出下降态势：是=1"
# - nrProm="电话公司营销的数量"
# - prom="最近一个月是否被营销过：是=1"
# - curPlan="统计时间开始时套餐类型：1=最高通过200分钟；2=300分钟；3=350分钟；4=500分钟"
# - avgplan="统计期间内平均套餐类型"
# - planChange="统计期间是否更换过套餐：1=是"
# - posPlanChange="统计期间是否提高套餐：1=是"
# - negPlanChange="统计期间是否降低套餐：1=是"
# - call_10086="拨打10086的次数"


import os
import numpy as np
from scipy import stats
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


# # 导入数据


churn = pd.read_csv('telecom_churn.csv')   
churn.head()


churn.info()


# # 分类变量的相关关系


# ## 交叉表


# normalize=False默认计算频数
cross_table = pd.crosstab(churn.posTrend, churn.churn, margins=True)
cross_table


def percConvert(ser):
    return ser/float(ser[-1])

cross_table.apply(percConvert, axis = 1)


544/1644


# ## 卡方检验


#列联表的卡方独立性检验：显著，说明二者存在相关关系
print('''chisq = %6.4f 
p-value = %6.4f
dof = %i 
expected_freq = %s'''  %stats.chi2_contingency(cross_table.iloc[:2, :2]))


# # 一元逻辑回归


# ## 划分训练集与测试集


#在网时长与是否流失
churn.plot(x='duration', y='churn', kind='scatter');


# 随机抽样，建立训练集与测试集
train = churn.sample(frac=0.7, random_state=666)
test = churn[~ churn.index.isin(train.index)]
print(' 训练集样本量: %i \n 测试集样本量: %i' %(len(train), len(test)))


# ## 建立模型


#建模
lg = smf.logit('churn ~ duration', train).fit()
lg.summary()


# ## 模型预测


#预测（概率）
train['proba'] = lg.predict(train)
test['proba'] = lg.predict(test)


test[['churn','proba']].head()


# ## 模型评估


import sklearn.metrics as metrics


#设置阈值
test['prediction'] = (test['proba'] > 0.3).astype('int')


test[['churn','prediction']].head(10)


#混淆矩阵
pd.crosstab(test.churn, test.prediction, margins=True)


#计算准确率
acc = sum(test['prediction'] == test['churn']) /len(test)
print('The accurancy is %.2f' %acc)


#ROC曲线
for i in np.arange(0.1, 0.9, 0.1):
    prediction = (test['proba'] > i).astype('int')
    confusion_matrix = pd.crosstab(prediction,test.churn,
                                   margins = True)
    precision = confusion_matrix.loc[0, 0] /confusion_matrix.loc['All', 0]
    recall = confusion_matrix.loc[0, 0] / confusion_matrix.loc[0, 'All']
    Specificity = confusion_matrix.loc[1, 1] /confusion_matrix.loc[1,'All']
    f1_score = 2 * (precision * recall) / (precision + recall)
    print('threshold: %s, precision: %.2f, recall:%.2f ,Specificity:%.2f , f1_score:%.2f'%(i, precision, recall, Specificity,f1_score))


fpr_test, tpr_test, th_test = metrics.roc_curve(test.churn, test.proba)
fpr_train, tpr_train, th_train = metrics.roc_curve(train.churn, train.proba)

plt.figure(figsize=[3, 3])
plt.plot(fpr_test, tpr_test, 'b--')
plt.plot(fpr_train, tpr_train, 'r-')
plt.title('ROC curve')
plt.show()


print('AUC = %.4f' %metrics.auc(fpr_test, tpr_test))


#最优阈值（约登指数）
th_test[(tpr_test - fpr_test).argmax()]


# # 多元逻辑回归


# ## 特征选择


# ### 连续变量选择


# 前向回归、后向回归、逐步回归：
# - 前向回归：Y和每个X做回归，选择解释力度最高的（R方、p_value、AIC、BIC），第一个变量进入回归方程，进行F检验和t检验，同时计算残差平方和s1，通过检验则保留；引入第二个变量，重新构建方程与检验，计算残差平方和s2，比较s1与s2，s1-s2（偏回归平方和）
# - 后向回归：与前向回归相反，所有变量一次进入，进行检验，根据偏回归平方和逐个剔除
# - 逐步回归：结合两者，变量一个个进入，引入新变量要进行检验，通过才加入，引入新变量后要对原变量重新进行检验，一旦不显著则剔除


# model = smf.glm(
#         formula=formula, data=data, 
#         family=sm.families.Binomial(sm.families.links.logit)
#     ).fit()


#向前法
def forward_select(data, response):
    remaining = set(data.columns)
    remaining.remove(response)
    selected = []
    current_score, best_new_score = float('inf'), float('inf')
    while remaining:
        aic_with_candidates=[]
        for candidate in remaining:
            formula = "{} ~ {}".format(
                response,' + '.join(selected + [candidate]))
            aic = smf.logit(
                formula=formula, data=data).fit().aic
            aic_with_candidates.append((aic, candidate))
        aic_with_candidates.sort(reverse=True)
        best_new_score, best_candidate=aic_with_candidates.pop()
        if current_score > best_new_score: 
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
            print ('aic is {},continuing!'.format(current_score))
        else:        
            print ('forward selection over!')
            break
            
    formula = "{} ~ {} ".format(response,' + '.join(selected))
    print('final formula is {}'.format(formula))
    model = smf.logit(formula=formula, data=data).fit()
    return(model)


#只有连续变量可以通过逐步回归进行筛选
candidates = ['churn','duration','AGE','incomeCode','nrProm','peakMinAv','peakMinDiff','call_10086']
data_for_select = train[candidates]


lg_m1 = forward_select(data=data_for_select, response='churn')
lg_m1.summary()


print(f'原来有 {len(candidates)-1} 个变量')
print(f'筛选剩下 {len(lg_m1.params.index.tolist())} 个(包含 intercept 截距项)。')


# ### 分类变量选择


# 解决方案：   
# - 逐一根据显著性测试   
# - 使用sklearn中的决策树等方法筛选变量，但是多分类变量需要事先进行变量概化   
# - 使用WOE转换，多分类变量也需要事先进行概化，使用scorecardpy包中的woe算法可以自动进行概化


class_col = ['posTrend','prom','edu_class','feton','curPlan','avgplan','gender','negTrend','planChange','posPlanChange','negPlanChange']
for i in class_col:
    tab = pd.crosstab(churn[i], churn.churn)
    print(i,''' p-value = %6.4f'''  %stats.chi2_contingency(tab)[1])


# ## 模型建立


formula = '''churn ~ duration + AGE +  incomeCode + peakMinDiff + call_10086 +C(edu_class) +C(feton)+ C(posTrend) + C(negTrend) + C(curPlan) + C(avgplan) + C(gender)'''
lg_m = smf.logit(formula=formula, data=train).fit()
lg_m.summary()


# ## 模型预测


train['proba'] = lg_m.predict(train)
test['proba'] = lg_m.predict(test)


test[['churn','proba']].head(10)


# ## 模型评估


#混淆矩阵（阈值）
test['prediction'] = (test['proba'] > 0.5).astype('int')
pd.crosstab(test.churn, test.prediction, margins=True)


#准确率
acc_m = sum(test['prediction'] == test['churn']) /len(test)
print('The accurancy is %.2f' %acc_m)


#ROC曲线
for i in np.arange(0.1, 0.9, 0.1):
    prediction = (test['proba'] > i).astype('int')
    confusion_matrix = pd.crosstab(prediction,test.churn,
                                   margins = True)
    precision = confusion_matrix.loc[0, 0] /confusion_matrix.loc['All', 0]
    recall = confusion_matrix.loc[0, 0] / confusion_matrix.loc[0, 'All']
    Specificity = confusion_matrix.loc[1, 1] /confusion_matrix.loc[1,'All']
    f1_score = 2 * (precision * recall) / (precision + recall)
    print('threshold: %s, precision: %.2f, recall:%.2f ,Specificity:%.2f , f1_score:%.2f'%(i, precision, recall, Specificity,f1_score))


fpr_test, tpr_test, th_test = metrics.roc_curve(test.churn, test.proba)
fpr_train, tpr_train, th_train = metrics.roc_curve(train.churn, train.proba)

plt.figure(figsize=[3, 3])
plt.plot(fpr_test, tpr_test, 'b--')
plt.plot(fpr_train, tpr_train, 'r-')
plt.title('ROC curve')
plt.show()


print('AUC = %.4f' %metrics.auc(fpr_test, tpr_test))


#最优阈值
th_test[(tpr_test - fpr_test).argmax()]


test['prediction'] = (test['proba'] > 0.456).astype('int')
pd.crosstab(test.churn, test.prediction, margins=True)


# ## 模型优化


# 方差膨胀因子检测
def vif(df, col_i):
    from statsmodels.formula.api import ols
    
    cols = list(df.columns)
    cols.remove(col_i)
    cols_noti = cols
    formula = col_i + '~' + '+'.join(cols_noti)
    r2 = ols(formula, df).fit().rsquared
    return 1. / (1. - r2)


exog = train[candidates].drop(['churn'], axis=1)
for i in exog.columns:
    print(i, '\t', vif(df=exog, col_i=i))


#分类变量的相关性检验
#最终模型的显著性检验

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第8章 逻辑回归（电信客户流失预测）
# ===================================
# 项目内涵：预测电信客户是否流失(churn, 0/1)，从一元逻辑回归到多元逻辑回归，含特征筛选、
#          模型评估(ROC/AUC/约登指数最优阈值)与共线性诊断，是典型的二分类评分卡场景。
# 技术方法：pd.crosstab 卡方检验、smf.logit、train/test 划分、predict 概率、
#          metrics.roc_curve/auc、约登指数(tpr-fpr)选阈值、前向选择 forward_select、VIF。
# 数据源：telecom_churn.csv（电信客户流失及行为变量）。
# 关键步骤：1)交叉表+卡方看 posTrend 与 churn 相关 → 2)一元 logit(churn~duration)
#          → 3)ROC/AUC/最优阈值 → 4)前向选择筛连续变量 → 5)卡方筛分类变量
#          → 6)多元 logit 建模 → 7)评估 → 8)VIF 共线性诊断。
#
#    subscriberID  churn  gender  ...  posPlanChange  negPlanChange  call_10086
# 0    19164958.0    1.0     0.0  ...            0.0            0.0         0.0
# 1    39244924.0    1.0     1.0  ...            1.0            0.0         1.0
# 2    39578413.0    1.0     0.0  ...            0.0            0.0         1.0
# 3    40992265.0    1.0     0.0  ...            0.0            0.0         1.0
# 4    43061957.0    1.0     1.0  ...            0.0            0.0         0.0
#
# [5 rows x 20 columns]
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3463 entries, 0 to 3462
# Data columns (total 20 columns):
#  #   Column         Non-Null Count  Dtype  
# ---  ------         --------------  -----  
#  0   subscriberID   3463 non-null   float64
#  1   churn          3463 non-null   float64
#  2   gender         3463 non-null   float64
#  3   AGE            3463 non-null   float64
#  4   edu_class      3463 non-null   float64
#  5   incomeCode     3463 non-null   float64
#  6   duration       3463 non-null   float64
#  7   feton          3463 non-null   float64
#  8   peakMinAv      3463 non-null   float64
#  9   peakMinDiff    3463 non-null   float64
#  10  posTrend       3463 non-null   float64
#  11  negTrend       3463 non-null   float64
#  12  nrProm         3463 non-null   float64
#  13  prom           3463 non-null   float64
#  14  curPlan        3463 non-null   float64
#  15  avgplan        3463 non-null   float64
#  16  planChange     3463 non-null   float64
#  17  posPlanChange  3463 non-null   float64
#  18  negPlanChange  3463 non-null   float64
#  19  call_10086     3463 non-null   float64
# dtypes: float64(20)
# memory usage: 541.2 KB
# None
# churn      0.0   1.0   All
# posTrend                  
# 0.0        829   990  1819
# 1.0       1100   544  1644
# All       1929  1534  3463
# churn          0.0       1.0  All
# posTrend                         
# 0.0       0.455745  0.544255  1.0
# 1.0       0.669100  0.330900  1.0
# All       0.557031  0.442969  1.0
# 0.3309002433090024
# chisq = 158.4433 
# p-value = 0.0000
# dof = 1 
# expected_freq = [[1013.24025411  805.75974589]
#  [ 915.75974589  728.24025411]]
#  训练集样本量: 2424 
#  测试集样本量: 1039
# Optimization terminated successfully.
#          Current function value: 0.434302
#          Iterations 8
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                  churn   No. Observations:                 2424
# Model:                          Logit   Df Residuals:                     2422
# Method:                           MLE   Df Model:                            1
# Date:                Mon, 12 Oct 2026   Pseudo R-squ.:                  0.3657
# Time:                        19:12:40   Log-Likelihood:                -1052.7
# converged:                       True   LL-Null:                       -1659.8
# Covariance Type:            nonrobust   LLR p-value:                5.281e-266
# ==============================================================================
#                  coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      2.5597      0.120     21.365      0.000       2.325       2.794
# duration      -0.2487      0.011    -22.035      0.000      -0.271      -0.227
# ==============================================================================
#     churn     proba
# 3     1.0  0.395387
# 4     1.0  0.284526
# 5     0.0  0.579658
# 9     1.0  0.158662
# 12    0.0  0.518160
#     churn  prediction
# 3     1.0           1
# 4     1.0           0
# 5     0.0           1
# 9     1.0           0
# 12    0.0           1
# 14    0.0           0
# 16    1.0           1
# 17    1.0           1
# 20    1.0           1
# 22    0.0           0
# prediction    0    1   All
# churn                     
# 0.0         340  220   560
# 1.0          42  437   479
# All         382  657  1039
# The accurancy is 0.75
# threshold: 0.1, precision: 0.45, recall:0.97 ,Specificity:0.61 , f1_score:0.62
# threshold: 0.2, precision: 0.56, recall:0.93 ,Specificity:0.65 , f1_score:0.69
# threshold: 0.30000000000000004, precision: 0.61, recall:0.89 ,Specificity:0.67 , f1_score:0.72
# threshold: 0.4, precision: 0.69, recall:0.83 ,Specificity:0.70 , f1_score:0.75
# threshold: 0.5, precision: 0.74, recall:0.79 ,Specificity:0.72 , f1_score:0.77
# threshold: 0.6, precision: 0.83, recall:0.74 ,Specificity:0.77 , f1_score:0.78
# threshold: 0.7000000000000001, precision: 0.94, recall:0.70 ,Specificity:0.89 , f1_score:0.80
# threshold: 0.8, precision: 1.00, recall:0.63 ,Specificity:1.00 , f1_score:0.78
# AUC = 0.8680
# 0.45610676187868604
# Optimization terminated successfully.
#          Current function value: 0.668183
#          Iterations 4
# Optimization terminated successfully.
#          Current function value: 0.684710
#          Iterations 4
# Optimization terminated successfully.
#          Current function value: 0.671157
#          Iterations 4
# Optimization terminated successfully.
#          Current function value: 0.684370
#          Iterations 4
# Optimization terminated successfully.
#          Current function value: 0.677466
#          Iterations 4
# Optimization terminated successfully.
#          Current function value: 0.434302
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.658732
#          Iterations 5
# aic is 2109.4961958557715,continuing!
# Optimization terminated successfully.
#          Current function value: 0.427515
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.434294
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.425883
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.434277
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.430781
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.419139
#          Iterations 8
# aic is 2037.9872517144947,continuing!
# Optimization terminated successfully.
#          Current function value: 0.412149
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.419115
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.411022
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.418736
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.416159
#          Iterations 8
# aic is 2000.633412463795,continuing!
# Optimization terminated successfully.
#          Current function value: 0.404355
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.411013
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.411019
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.408969
#          Iterations 8
# aic is 1970.3132429937205,continuing!
# Optimization terminated successfully.
#          Current function value: 0.404317
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.404355
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.402241
#          Iterations 8
# aic is 1962.0625746095795,continuing!
# Optimization terminated successfully.
#          Current function value: 0.402195
#          Iterations 8
# Optimization terminated successfully.
#          Current function value: 0.402237
#          Iterations 8
# forward selection over!
# final formula is churn ~ duration + peakMinDiff + AGE + call_10086 + incomeCode 
# Optimization terminated successfully.
#          Current function value: 0.402241
#          Iterations 8
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                  churn   No. Observations:                 2424
# Model:                          Logit   Df Residuals:                     2418
# Method:                           MLE   Df Model:                            5
# Date:                Mon, 12 Oct 2026   Pseudo R-squ.:                  0.4126
# Time:                        19:12:40   Log-Likelihood:                -975.03
# converged:                       True   LL-Null:                       -1659.8
# Covariance Type:            nonrobust   LLR p-value:                5.520e-294
# ===============================================================================
#                   coef    std err          z      P>|z|      [0.025      0.975]
# -------------------------------------------------------------------------------
# Intercept       3.2780      0.218     15.066      0.000       2.852       3.704
# duration       -0.2464      0.012    -20.972      0.000      -0.269      -0.223
# peakMinDiff    -0.0028      0.000     -7.873      0.000      -0.004      -0.002
# AGE            -0.0233      0.004     -5.706      0.000      -0.031      -0.015
# call_10086     -0.6405      0.113     -5.671      0.000      -0.862      -0.419
# incomeCode      0.0108      0.003      3.191      0.001       0.004       0.017
# ===============================================================================
# 原来有 7 个变量
# 筛选剩下 6 个(包含 intercept 截距项)。
# posTrend  p-value = 0.0000
# prom  p-value = 0.2680
# edu_class  p-value = 0.0000
# feton  p-value = 0.0000
# curPlan  p-value = 0.0000
# avgplan  p-value = 0.0000
# gender  p-value = 0.0000
# negTrend  p-value = 0.0000
# planChange  p-value = 0.3037
# posPlanChange  p-value = 1.0000
# negPlanChange  p-value = 1.0000
# Warning: Maximum number of iterations has been exceeded.
#          Current function value: 0.315366
#          Iterations: 35
#                            Logit Regression Results                           
# ==============================================================================
# Dep. Variable:                  churn   No. Observations:                 2424
# Model:                          Logit   Df Residuals:                     2405
# Method:                           MLE   Df Model:                           18
# Date:                Mon, 12 Oct 2026   Pseudo R-squ.:                  0.5394
# Time:                        19:12:41   Log-Likelihood:                -764.45
# converged:                      False   LL-Null:                       -1659.8
# Covariance Type:            nonrobust   LLR p-value:                     0.000
# =======================================================================================
#                           coef    std err          z      P>|z|      [0.025      0.975]
# ---------------------------------------------------------------------------------------
# Intercept               5.0680      0.544      9.316      0.000       4.002       6.134
# C(edu_class)[T.1.0]     0.7367      0.152      4.863      0.000       0.440       1.034
# C(edu_class)[T.2.0]     1.0947      0.184      5.956      0.000       0.734       1.455
# C(edu_class)[T.3.0]     0.7519      0.373      2.014      0.044       0.020       1.484
# C(feton)[T.1.0]        -1.3024      0.133     -9.824      0.000      -1.562      -1.043
# C(posTrend)[T.1.0]     -1.5366      0.442     -3.473      0.001      -2.404      -0.669
# C(negTrend)[T.1.0]     -1.3148      0.444     -2.960      0.003      -2.185      -0.444
# C(curPlan)[T.2.0]     -34.2269   5358.008     -0.006      0.995   -1.05e+04    1.05e+04
# C(curPlan)[T.3.0]     -14.1381   3094.091     -0.005      0.996   -6078.444    6050.168
# C(curPlan)[T.4.0]     -11.0265   3094.091     -0.004      0.997   -6075.334    6053.280
# C(avgplan)[T.2.0]      30.2882   5358.008      0.006      0.995   -1.05e+04    1.05e+04
# C(avgplan)[T.3.0]      14.0555   3094.091      0.005      0.996   -6050.251    6078.362
# C(avgplan)[T.4.0]      10.1621   3094.091      0.003      0.997   -6054.145    6074.469
# C(gender)[T.1.0]        1.2543      0.134      9.371      0.000       0.992       1.517
# duration               -0.2898      0.015    -19.087      0.000      -0.320      -0.260
# AGE                    -0.0268      0.005     -5.635      0.000      -0.036      -0.018
# incomeCode              0.0122      0.004      3.116      0.002       0.005       0.020
# peakMinDiff            -0.0024      0.001     -4.653      0.000      -0.003      -0.001
# call_10086             -0.7867      0.131     -6.020      0.000      -1.043      -0.531
# =======================================================================================
#     churn     proba
# 3     1.0  0.179935
# 4     1.0  0.542096
# 5     0.0  0.006720
# 9     1.0  0.435664
# 12    0.0  0.428403
# 14    0.0  0.015822
# 16    1.0  0.960080
# 17    1.0  0.947527
# 20    1.0  0.895866
# 22    0.0  0.001686
# prediction    0    1   All
# churn                     
# 0.0         464   96   560
# 1.0          78  401   479
# All         542  497  1039
# The accurancy is 0.83
# threshold: 0.1, precision: 0.57, recall:0.98 ,Specificity:0.66 , f1_score:0.72
# threshold: 0.2, precision: 0.66, recall:0.95 ,Specificity:0.71 , f1_score:0.78
# threshold: 0.30000000000000004, precision: 0.74, recall:0.93 ,Specificity:0.75 , f1_score:0.82
# threshold: 0.4, precision: 0.79, recall:0.89 ,Specificity:0.78 , f1_score:0.84
# threshold: 0.5, precision: 0.83, recall:0.86 ,Specificity:0.81 , f1_score:0.84
# threshold: 0.6, precision: 0.88, recall:0.83 ,Specificity:0.85 , f1_score:0.85
# threshold: 0.7000000000000001, precision: 0.92, recall:0.79 ,Specificity:0.89 , f1_score:0.85
# threshold: 0.8, precision: 0.96, recall:0.74 ,Specificity:0.93 , f1_score:0.84
# AUC = 0.9297
# 0.3562514967736567
# prediction    0    1   All
# churn                     
# 0.0         456  104   560
# 1.0          68  411   479
# All         524  515  1039
# duration 	 1.0436502311937923
# AGE 	 1.061106306219031
# incomeCode 	 1.01525593193185
# nrProm 	 1.001884084219539
# peakMinAv 	 1.0461668630867544
# peakMinDiff 	 1.0187447997918486
# call_10086 	 1.0213331858803003
# [stderr] <string>:16: FutureWarning: Series.__getitem__ treating keys as positions is deprecated. In a future version, integer keys will always be treated as labels (consistent with DataFrame behavior). To access a value by position, use `ser.iloc[pos]`
# [stderr] <string>:27: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame.
# [stderr] Try using .loc[row_indexer,col_indexer] = value instead
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] <string>:30: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame.
# [stderr] Try using .loc[row_indexer,col_indexer] = value instead
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] <string>:49: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] C:\Users\chendan\AppData\Local\Programs\Python\Python310\lib\site-packages\statsmodels\discrete\discrete_model.py:268: ConvergenceWarning: Maximum Likelihood optimization failed to converge. Check mle_retvals
# [stderr]   mlefit = super().fit(
# [stderr] <string>:92: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame.
# [stderr] Try using .loc[row_indexer,col_indexer] = value instead
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] <string>:94: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame.
# [stderr] Try using .loc[row_indexer,col_indexer] = value instead
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# [stderr] <string>:112: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
# [stderr] <string>:115: SettingWithCopyWarning: 
# [stderr] A value is trying to be set on a copy of a slice from a DataFrame.
# [stderr] Try using .loc[row_indexer,col_indexer] = value instead
# [stderr] 
# [stderr] See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy


# ================================================================
# 12. 第9章 用户分群 —— K-means 用户细分（银行客户）
# 源文件: 第9章-用户分群\k-means聚类\Kmeans 的应用 - 用户细分.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第9章-用户分群\k-means聚类
# ================================================================

# -*- coding: utf-8 -*-
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

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
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
# 0  41360       34        3        3        9       49        2
# 1  52094       44       17        5       18       84        2
# 2  57340      122       26       32       36      216        2
# 3  76885       42        3        6        1       52        1
# 4  89150       20       15        2        2       39        1
# clustor
# 1    35942
# 2    34240
# 0    29818
# Name: count, dtype: int64
# DecisionTreeClassifier(max_depth=3, min_samples_leaf=100, min_samples_split=100,
#                        random_state=12345)
# 决策树图形渲染跳过(需安装 GraphViz): GraphViz's executables not found
# 决策树 dot 文本已保存为 kmeans_decision_tree.dot


# ================================================================
# 13. 第9章 用户分群 —— 层次聚类（城市经济指标）
# 源文件: 第9章-用户分群\层次聚类\hc_city10.py
# 数据目录: D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第9章-用户分群\层次聚类
# ================================================================

# -*- coding: utf-8 -*-
"""
第9章 用户分群 —— 层次聚类（城市经济指标）
============================================
项目内涵：对 10 个城市按 9 项经济指标聚类。先用 PCA 确定主成分个数，再用 fa_kit 做因子
         分析降为 2 个公共因子(Gross 总量/Avg 人均)，计算因子得分后用 scipy 层次聚类
         (ward 法)画出树状图，肉眼判定类别。
技术方法：StandardScaler、PCA、fa_kit 因子分析(varimax 旋转)、
         scipy.cluster.hierarchy: pdist(欧式距离)/linkage(ward)/dendrogram(树状图)。
数据源：cities_10.csv（10 城市 9 项经济指标 X1~X9），输出 fa_cities_10.csv、plot_dendrogram.png。
关键步骤：1)标准化 → 2)PCA 看 2 主成分解释 92% → 3)fa_kit 因子分析(varimax)得 Gross/Avg
         → 4)因子得分拼回原数据 → 5)散点图肉眼分类 → 6)层次聚类 ward 法 → 7)树状图。
依赖：fa_kit。
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# 读取city10.csv该数据代码
#你的代码
df=pd.read_csv("cities_10.csv",encoding="gbk")
df


#选取要用的特征
#你的代码
model_data=df.loc[:,"X1":]
model_data


# # 使用主成分分析 手动确定几个主成分 来压缩信息


#查看相关系数 判断使用主成分分析 变量降维的必要性
#你的代码
corr_matrix=model_data.corr()
corr_matrix


#在使用主成分和聚类之前 应该？？？from sklearn.preprocessing import StandardScaler
#你的代码
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
scaler_model_data=scaler.fit_transform(model_data)
scaler_model_data


#使用sklearn框架做主成分，判断主成分数量
#from sklearn.decomposition import PCA
#你的代码
from sklearn.decomposition import PCA


#实例化
pca=PCA(n_components=3)
model_data_scale=pca.fit(scaler_model_data)
model_data_scale


np.set_printoptions(suppress=True)#阻止数字以科学计算输出 眼睛不好观察>0<
#输出主成分方差和占比 pca.explained_variance_
#你的代码
print("主成分可解释的变异：\n",pca.explained_variance_)
print("主成分可解释的变异的比例:\n",pca.explained_variance_ratio_)


0.8+0.12


#根据结果 可见 选2个主成分可解释大部分数据


# - 根据主成分个数来确定因子个数，为下面因子分析做准备


# # 因子分析


#导入因子分析的包提取主成分，fa_kit是一个第三方的包 需要下载
#pip install fa_kit 我这里已经下载安装好了。。。


from fa_kit import FactorAnalysis
from fa_kit import plotting as fa_plotting#绘制因子载荷矩阵


#对输入的数据进行主成分提取
fa=FactorAnalysis.load_data_samples(
scaler_model_data,
preproc_demean=True,
preproc_scale=True)
fa.extract_components()


#设定提取主出发的方式，默认是broken_stick，建议使用top_n方法 fa.find
#你的代码
fa.find_comps_to_retain(method="top_n",num_keep=2)


#通过最大方差法对因子进行旋转
#你的代码
fa.rotate_components(method="varimax")


#可以绘制因子载荷矩阵图
fa_plotting.graph_summary(fa)
#第一张图解释了数据变异比例，第一个主成分解释了数据80%的变异，前两个主主成分已经大概能够解释原始数据了
#第二张图是在未旋转之前，各变量在因子中权重（载荷）每条折线表示一个因子，x轴个原始变量，y轴不同因子在各个变量上的权重
#第三张图方差最大化旋转后各个因子在各变量上的权重（载荷），观察此图，权重越高，代表性越强
#如果眼睛不喜欢看 emmm 那就看数，即打印因子载荷


#打印旋转后的因子权重
#你的代码
fa.comps["rot"]


# - 输出因子得分 拼接到原数据，对该数据进行层次聚类分析


#输出因子得分，为了方便拼接 转换成数据框
#你的代码n
fa_scores=fa.get_component_scores(scaler_model_data)
fa_scores=pd.DataFrame(fa_scores,columns=["Gross","Avg"])
fa_scores


#拼接原始数据
#你的代码
cities_fa_scores=df.join(fa_scores)
cities_fa_scores


cities_fa_scores.to_csv("fa_cities_10.csv",index=False)#不是必须


# # 层次聚类分析


#现在，对新的这份数据进行层次聚类分析
#你的代码
new_model_data=pd.read_csv("fa_cities_10.csv")
new_model_data


#画图，肉眼先看看分成几类，这些城市，
plt.rcParams['font.family'] = 'SimHei'
from pylab import mpl
mpl.rcParams['axes.unicode_minus'] = False 

def scatter(x, y, labels, **kw):
    
    plt.figure(figsize=(6, 4))
    plt.yticks(size=12)
    plt.xticks(size=12)
    plt.scatter(x, y)
    for xx, yy, label in zip(x, y, labels):
        plt.text(xx, yy, '%s.' % label, 
                 ha='center', va='bottom', **kw)
plt.show()


# 画图，x,y，标签
#你的代码
x=new_model_data["Gross"]
y=new_model_data["Avg"]
labels=new_model_data["AREA"]
scatter(x,y,labels)


# - 因子分析后 开始对拼接后的数据进行层次聚类分析


#层次聚类 导入包
import scipy.cluster.hierarchy as sch


#计算距离 生成点与点欧式距离矩阵
#你的代码
dis_mat=sch.distance.pdist(new_model_data[["Gross","Avg"]],metric='euclidean')


#搭建层次聚类模型,类与类链接
#你的代码
Z=sch.linkage(dis_mat,method="ward")
Z


#将层次聚类结果用层次聚类图展示出来，plt.savefig('plot_dendrogram.png')
#你的代码
P=sch.dendrogram(Z,labels=new_model_data["AREA"].tolist())
plt.savefig("plot_dendrogram.png")

# ------------------------------------------------------------
# 【运行结果】成功
# ------------------------------------------------------------
#
# 第9章 用户分群 —— 层次聚类（城市经济指标）
# ============================================
# 项目内涵：对 10 个城市按 9 项经济指标聚类。先用 PCA 确定主成分个数，再用 fa_kit 做因子
#          分析降为 2 个公共因子(Gross 总量/Avg 人均)，计算因子得分后用 scipy 层次聚类
#          (ward 法)画出树状图，肉眼判定类别。
# 技术方法：StandardScaler、PCA、fa_kit 因子分析(varimax 旋转)、
#          scipy.cluster.hierarchy: pdist(欧式距离)/linkage(ward)/dendrogram(树状图)。
# 数据源：cities_10.csv（10 城市 9 项经济指标 X1~X9），输出 fa_cities_10.csv、plot_dendrogram.png。
# 关键步骤：1)标准化 → 2)PCA 看 2 主成分解释 92% → 3)fa_kit 因子分析(varimax)得 Gross/Avg
#          → 4)因子得分拼回原数据 → 5)散点图肉眼分类 → 6)层次聚类 ward 法 → 7)树状图。
# 依赖：fa_kit。
#
# None
#   AREA       X1     X2      X3      X4      X5      X6      X7      X8      X9
# 0   辽宁   5458.2  13000  1376.2  2258.4  1315.9   529.0  2258.4   123.7   399.7
# 1   山东  10550.0  11643  3502.5  3851.0  2288.7  1070.7  3181.9   211.1   610.2
# 2   河北   6076.6   9047  1406.7  2092.6  1161.6   597.1  1968.3    45.9   302.3
# 3   天津   2022.6  22068   822.8   960.0   703.7   361.9   941.4   115.7   171.8
# 4   江苏  10636.3  14397  3536.3  3967.2  2320.0  1141.3  3215.8   384.7   643.7
# 5   上海   5408.8  40627  2196.2  2755.8  1970.2   779.3  2035.2   320.5   709.0
# 6   浙江   7670.0  16570  2356.5  3065.0  2296.6  1180.6  2877.5   294.2   566.9
# 7   福建   4682.0  13510  1047.1  1859.0   964.5   397.9  1663.3   173.7   272.9
# 8   广东  11769.7  15030  4224.6  4793.6  3022.9  1275.5  5013.6  1843.7  1201.6
# 9   广西   2455.4   5062   367.0   995.7   542.2   352.7  1025.5    15.1   186.7
#         X1     X2      X3      X4      X5      X6      X7      X8      X9
# 0   5458.2  13000  1376.2  2258.4  1315.9   529.0  2258.4   123.7   399.7
# 1  10550.0  11643  3502.5  3851.0  2288.7  1070.7  3181.9   211.1   610.2
# 2   6076.6   9047  1406.7  2092.6  1161.6   597.1  1968.3    45.9   302.3
# 3   2022.6  22068   822.8   960.0   703.7   361.9   941.4   115.7   171.8
# 4  10636.3  14397  3536.3  3967.2  2320.0  1141.3  3215.8   384.7   643.7
# 5   5408.8  40627  2196.2  2755.8  1970.2   779.3  2035.2   320.5   709.0
# 6   7670.0  16570  2356.5  3065.0  2296.6  1180.6  2877.5   294.2   566.9
# 7   4682.0  13510  1047.1  1859.0   964.5   397.9  1663.3   173.7   272.9
# 8  11769.7  15030  4224.6  4793.6  3022.9  1275.5  5013.6  1843.7  1201.6
# 9   2455.4   5062   367.0   995.7   542.2   352.7  1025.5    15.1   186.7
#           X1        X2        X3  ...        X7        X8        X9
# X1  1.000000 -0.094292  0.966506  ...  0.941148  0.637458  0.825568
# X2 -0.094292  1.000000  0.112726  ... -0.042776  0.081195  0.273145
# X3  0.966506  0.112726  1.000000  ...  0.935196  0.704714  0.898016
# X4  0.979238  0.074167  0.985373  ...  0.962267  0.713890  0.913364
# X5  0.922984  0.214052  0.963159  ...  0.937109  0.716722  0.934549
# X6  0.921680  0.093483  0.939194  ...  0.897127  0.624294  0.848004
# X7  0.941148 -0.042776  0.935196  ...  1.000000  0.836272  0.928692
# X8  0.637458  0.081195  0.704714  ...  0.836272  1.000000  0.881528
# X9  0.825568  0.273145  0.898016  ...  0.928692  0.881528  1.000000
#
# [9 rows x 9 columns]
# [[-0.37574772 -0.33589708 -0.57070001 -0.33180084 -0.4351153  -0.68608742
#   -0.13882664 -0.44958874 -0.36008526]
#  [ 1.19924012 -0.48315182  1.14473196  0.98455823  0.79990984  0.8650543
#    0.66401891 -0.27809633  0.34976628]
#  [-0.18446517 -0.76485655 -0.54609356 -0.46884237 -0.63100796 -0.49108511
#   -0.39102534 -0.60224445 -0.68853914]
#  [-1.43844228  0.6481162  -1.01716572 -1.40498973 -1.21233816 -1.16457327
#   -1.28376177 -0.46528598 -1.12861338]
#  [ 1.2259343  -0.18430174  1.17200074  1.08060301  0.83964698  1.06721529
#    0.6934899   0.0625339   0.46273553]
#  [-0.39102805  2.66204455  0.09085021  0.07932373  0.3955559   0.03063913
#   -0.33286576 -0.06343649  0.68294126]
#  [ 0.3084029   0.05150118  0.22017521  0.33489213  0.80993934  1.17974966
#    0.39938849 -0.11504119  0.20374931]
#  [-0.61584072 -0.28055447 -0.83620754 -0.66192379 -0.88123767 -1.06148835
#   -0.65617736 -0.35148095 -0.7876823 ]
#  [ 1.57651587 -0.11561179  1.72729954  1.76366162  1.73201866  1.45149297
#    2.25640894  2.92531908  2.34409505]
#  [-1.30456925 -1.19728849 -1.38489083 -1.37548199 -1.41737163 -1.19091719
#   -1.21064936 -0.66267885 -1.07836735]]
# PCA(n_components=3)
# None
# 主成分可解释的变异：
#  [8.01129553 1.22149318 0.60792399]
# 主成分可解释的变异的比例:
#  [0.80112955 0.12214932 0.0607924 ]
# 0.92
# None
# [0 1]
# None
# Figure(800x1200)
# [[ 0.36287997 -0.19604704]
#  [-0.00194704  0.94364822]
#  [ 0.36422208  0.00656524]
#  [ 0.36925509 -0.02877546]
#  [ 0.36125764  0.11159649]
#  [ 0.35279873 -0.00714436]
#  [ 0.37014035 -0.11869071]
#  [ 0.29509869  0.06139991]
#  [ 0.34676526  0.19965023]]
#       Gross       Avg
# 0 -1.174241 -0.364178
# 1  2.095775 -0.654819
# 2 -1.399899 -0.870629
# 3 -3.265185  0.698849
# 4  2.386557 -0.337666
# 5  0.163901  2.802894
# 6  1.209012  0.048116
# 7 -2.084500 -0.322173
# 8  5.501759  0.105138
# 9 -3.433179 -1.105531
#   AREA       X1     X2      X3  ...      X8      X9     Gross       Avg
# 0   辽宁   5458.2  13000  1376.2  ...   123.7   399.7 -1.174241 -0.364178
# 1   山东  10550.0  11643  3502.5  ...   211.1   610.2  2.095775 -0.654819
# 2   河北   6076.6   9047  1406.7  ...    45.9   302.3 -1.399899 -0.870629
# 3   天津   2022.6  22068   822.8  ...   115.7   171.8 -3.265185  0.698849
# 4   江苏  10636.3  14397  3536.3  ...   384.7   643.7  2.386557 -0.337666
# 5   上海   5408.8  40627  2196.2  ...   320.5   709.0  0.163901  2.802894
# 6   浙江   7670.0  16570  2356.5  ...   294.2   566.9  1.209012  0.048116
# 7   福建   4682.0  13510  1047.1  ...   173.7   272.9 -2.084500 -0.322173
# 8   广东  11769.7  15030  4224.6  ...  1843.7  1201.6  5.501759  0.105138
# 9   广西   2455.4   5062   367.0  ...    15.1   186.7 -3.433179 -1.105531
#
# [10 rows x 12 columns]
# None
#   AREA       X1     X2      X3  ...      X8      X9     Gross       Avg
# 0   辽宁   5458.2  13000  1376.2  ...   123.7   399.7 -1.174241 -0.364178
# 1   山东  10550.0  11643  3502.5  ...   211.1   610.2  2.095775 -0.654819
# 2   河北   6076.6   9047  1406.7  ...    45.9   302.3 -1.399899 -0.870629
# 3   天津   2022.6  22068   822.8  ...   115.7   171.8 -3.265185  0.698849
# 4   江苏  10636.3  14397  3536.3  ...   384.7   643.7  2.386557 -0.337666
# 5   上海   5408.8  40627  2196.2  ...   320.5   709.0  0.163901  2.802894
# 6   浙江   7670.0  16570  2356.5  ...   294.2   566.9  1.209012  0.048116
# 7   福建   4682.0  13510  1047.1  ...   173.7   272.9 -2.084500 -0.322173
# 8   广东  11769.7  15030  4224.6  ...  1843.7  1201.6  5.501759  0.105138
# 9   广西   2455.4   5062   367.0  ...    15.1   186.7 -3.433179 -1.105531
#
# [10 rows x 12 columns]
# None
# [[ 1.          4.          0.43027829  2.        ]
#  [ 0.          2.          0.55445008  2.        ]
#  [ 7.         11.          0.98187246  3.        ]
#  [ 6.         10.          1.34742622  3.        ]
#  [ 3.          9.          1.81218392  2.        ]
#  [12.         14.          2.82545755  5.        ]
#  [ 5.         13.          4.36874882  4.        ]
#  [ 8.         16.          5.127847    5.        ]
#  [15.         17.         10.30873462 10.        ]]



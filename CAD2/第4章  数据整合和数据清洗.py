# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第4章- 数据处理(pandas)")
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



# ============================================================
# 【运行结果】成功
# ============================================================
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

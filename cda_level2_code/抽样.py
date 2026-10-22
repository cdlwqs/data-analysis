# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第6章-市场调研与数据预处理\1数据采集与处理 1 数据采集方法")
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



# ============================================================
# 【运行结果】成功
# ============================================================
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

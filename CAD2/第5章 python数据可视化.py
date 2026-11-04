# -*- coding: utf-8 -*-
import os as _os; _os.chdir(r"D:\CDA\CDA 教材资料2025\2《CDA 二级认证教材：量化策略分析》\第5章-数据可视化")
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



# ============================================================
# 【运行结果】成功
# ============================================================
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
# <seaborn.axisgrid.FacetGrid object at 0x0000024310AC5AB0>
# None
#           x         y
# 0 -1.727793 -0.327636
# 1 -1.968059  1.272835
# 2 -1.128714 -1.105992
# 3 -0.747122  0.101521
# 4 -0.115909  1.294689
# <seaborn.axisgrid.JointGrid object at 0x0000024310AC56F0>
# <seaborn.axisgrid.FacetGrid object at 0x0000024335089180>
# <seaborn.axisgrid.JointGrid object at 0x0000024335089180>
# <seaborn.axisgrid.FacetGrid object at 0x0000024335089180>
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

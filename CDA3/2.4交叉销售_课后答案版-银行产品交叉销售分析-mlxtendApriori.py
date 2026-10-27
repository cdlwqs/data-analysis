"""课后答案版-银行产品交叉销售分析-mlxtendApriori
原素材: 2.4交叉销售（关联规则与序列模式）\关联规则-使用现成的python包\课后答案版-银行产品交叉销售分析-mlxtendApriori.ipynb
"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
file_path = '/Users/xavierxiong/Desktop/银行B端项目资料/常农项目材料-20240804/第三周/代码和数据/2关联规则/bank_prod_order(1).csv'
data = pd.read_csv(file_path, encoding='gbk')
data.head()
grouped = data.groupby('CSR_ID')['PROD'].apply(list)
grouped
te = TransactionEncoder()
te_ary = te.fit(grouped).transform(grouped)
df = pd.DataFrame(te_ary, columns=te.columns_)
df
#函数
def encode_units(x):
    if x ==True:
        return 1
    else:
        return 0
df=df.applymap(encode_units)
df.head()
frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
frequent_itemsets
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules
#可以根据需要进行后续处理，如按照confidence和lift过滤后，按support排序
conf = rules[(rules.confidence > 0.1) & (rules.lift > 1)]
conf.sort_values(by='support', ascending=False).head()
#如果有必要，也可以通过图形看一下规则在支持度，置信度和提升度上的分布情况
import matplotlib.pyplot as plt
%matplotlib inline

ax = plt.subplot()
ax.set_xlabel('lift')
conf.plot.scatter(x="lift", y="support",c="confidence",cmap='binary',
                  figsize=(6,4), ax=ax)

plt.show()

rules
# 确保 antecedents 和 consequents 是字符串类型
rules['antecedents'] = rules['antecedents'].astype(str)
rules['consequents'] = rules['consequents'].astype(str)

# 筛选 antecedents 和 consequents 包含 "财务通" 的规则
caiwutong_rules = rules[rules['antecedents'].str.contains('财务通') | rules['consequents'].str.contains('财务通')]

# 输出相关规则
print("与'财务通'相关的规则:")
print(caiwutong_rules)
caiwutong_rules#筛选规则中lift>1且confidence高的规则
# 筛选 antecedents 和 consequents 包含 "好享贷" 的规则
haoxiangdai_rules = rules[rules['consequents'].str.contains('好享贷')]

# 输出相关规则
print("与'好享贷'相关的规则:")
haoxiangdai_rules

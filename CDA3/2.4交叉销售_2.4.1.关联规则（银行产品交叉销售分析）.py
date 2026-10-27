"""2.4.1.关联规则（银行产品交叉销售分析）
原素材: 2.4交叉销售（关联规则与序列模式）\2.4.1.关联规则（银行产品交叉销售分析）.ipynb
"""

import pandas as pd

data = pd.read_csv('bank_prod_order.csv',encoding='gbk')
data.head()
baskets = data['PROD'].groupby(data['CSR_ID']).apply(list)
baskets.head()
import sys
sys.path.append('./myscript')
from apriori import arules

rules = arules(baskets, min_support=0.02)
rules.head()
conf = rules[(rules.confidence > 0.1) & (rules.lift > 1)]
conf.sort_values(by='support', ascending=False).head()
import matplotlib.pyplot as plt
%matplotlib inline

ax = plt.subplot()
ax.set_xlabel('lift')
conf.plot.scatter(x="lift", y="support",c="confidence",cmap='binary',
                  figsize=(6,4), ax=ax)

plt.show()
mapping = data['PROD'].drop_duplicates().to_dict()  # 生成{编号:产品}映射
inverse_mapping = {v:k for k, v in mapping.items()}     # 生成{产品:编号}映射

data['PROD'] = data['PROD'].replace(inverse_mapping)  # 将产品用编号替代
baskets = data['PROD'].groupby(data['CSR_ID']).apply(list)  
baskets.head()
from orangecontrib.associate.fpgrowth import *  

# 计算关联规则
n_examples=len(data)
itemsets = dict(frequent_itemsets(baskets.tolist(), 0.02))
rules = association_rules(itemsets, min_confidence=0.1)
stats = rules_stats(rules, itemsets, n_examples)

result = pd.DataFrame(stats, columns=['atecedent', 'consequent', 'support', 
                                      'confidence', 'coverage', 'strength', 
                                      'lift', 'leverage'])

# 将整型的项转换为原始产品名称
pid_to_product = lambda fsets: tuple(mapping[fset] for fset in fsets)
result['atecedent'] = result['atecedent'].map(pid_to_product)
result['consequent'] = result['consequent'].map(pid_to_product)
result.head()


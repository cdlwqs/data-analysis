"""2.4.2.序列模式（银行产品交叉销售分析）
原素材: 2.4交叉销售（关联规则与序列模式）\2.4.2.序列模式（银行产品交叉销售分析）.ipynb
"""

import pandas as pd

data = pd.read_csv('bank_prod_order.csv', encoding='gbk')

# 按照订单编号与用户编号分组汇总
baskets = data.groupby(['OrderNumber', 'CSR_ID'])['PROD'].apply(list)
baskets.head()
# 按照用户编号分组汇总
baskets = baskets.groupby(level=1).apply(list)
baskets.head()
import sys
sys.path.append('./myscript')  # aprioriAll.py放在'./myscript'文件夹下
from aprioriAll import aprioriAll

patterns = aprioriAll(baskets, min_support=0.1)
patterns.head()
import sys

sys.path.append('./myscript')  # prefixspan.py放在'./myscript'下

from prefixspan import SquencePattern, prefixSpan

patterns = prefixSpan(SquencePattern([], 1e4), baskets, threshold=100)
for pattern in patterns:
    print(pattern.squence, "-> support:", pattern.support)




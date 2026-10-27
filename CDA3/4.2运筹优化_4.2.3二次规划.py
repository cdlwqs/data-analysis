"""4.2.3二次规划
原素材: 4.2运筹优化\4.2.3二次规划.ipynb
"""

import cplex

op = cplex.Cplex()
op.read("qp1.lp")
op.solve()
# 输出结果
print(op.solution.get_objective_value())
print(op.solution.get_values())




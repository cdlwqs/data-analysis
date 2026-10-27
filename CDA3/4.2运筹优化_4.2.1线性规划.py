"""4.2.1线性规划
原素材: 4.2运筹优化\4.2.1线性规划.ipynb
"""

import cplex
op = cplex.Cplex()
op.read("productivity.lp")
op.solve()
print("Max objective value is %s" %op.solution.get_objective_value())
print("Best Productivety is %s" %op.solution.get_values())


"""4.2.2整数规划
原素材: 4.2运筹优化\4.2.2整数规划.ipynb
"""

import cplex
import numpy as np
op = cplex.Cplex()
op.read("campaign.lp")
op.solve()
print("Max objective value is %s" %op.solution.get_objective_value())
print("Best allocation :")
print(np.array(op.solution.get_values()).reshape([3,-1]).T)



"""流程挖掘pm4py
原素材: 4.3流程挖掘\流程挖掘pm4py.ipynb
"""

##导入IEEE XES格式数据
#IEEE XES是一种存储日志数据的标准格式。
from pm4py.objects.log.importer.xes import importer as xes_importer

log = xes_importer.apply('./running-example.xes')
print(log)
print('The first trace in the log: \n', log[0])
print('-' * 80)
print('The first event of the first trace: \n', log[0][0])
log[0:2:2][:3]
print(type(log))
print(type(log[0]))
print(type(log[0][0]))
print('Length of the log is %d' %(len(log)))
print('Length of the first trace is %d' %(len(log[0])))
print('Length of the first event is %d' %(len(log[0][0])))
# 导出XES文件
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
xes_exporter.apply(log, "./exportedLog.xes")
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

dfg = dfg_discovery.apply(log)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
dfg_visualization.view(gviz)
#添加流程转换耗时信息
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
dfg_visualization.view(gviz)



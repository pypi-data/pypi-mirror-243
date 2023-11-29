
#%%
import numpy as np
import networkx as nx
import pandas as pd 
exec(open("../sevenbridges/graphcreator.py").read())

latitude_longitude_data = np.array([
    [40.09068,116.17355],
     [40.00395,116.20531],
     [39.91441,116.18424],
     [39.81513,116.17115],
     [39.742767,116.13605],
     [39.987312,116.28745],
     [39.98205,116.3974],
     [39.95405,116.34899],
])

df = pd.DataFrame(latitude_longitude_data,columns=['lat','lon'])
df.insert(0,'node_name',['node1','node2','node3','node4','node5','node6','node7','node8'])
display(df)
generator = graph_generator()




generator.minmax(df)
generator.summary_statistics()

for i in generator.G.nodes(data=True):
    print(i)


generator.plot()
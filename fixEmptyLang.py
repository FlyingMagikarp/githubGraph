import networkx as nx

g = nx.read_gpickle("data/small.gpickle.1")
change = 0
for n in g.nodes:
    o = g.nodes[n]
    if o['type'] == 'repo' and o['lang'] is None:
        o['lang'] = 'NONE'
        change += 1

print("changed ",change," nodes")
print("-----")
print(nx.info(g))

nx.write_gml(g,"data/small.gml")
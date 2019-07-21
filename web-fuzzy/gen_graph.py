import json
import secrets
from random import randint, choices


N = 500

graph = {}

nodes = [secrets.token_hex(8) for _ in range(N)]

for node in nodes:
    graph[node] = {"children":[],'parent':None}

graph['root'] = nodes[0]

for i in range(1, N):
    cur_node = nodes[i]
    parent = nodes[randint(0, i-1)]
    graph[parent]['children'].append(cur_node)
    graph[cur_node]['parent'] = parent

graph[nodes[-1]] = True

json.dump(graph, open("graph.json", "w"))

print(len(graph))


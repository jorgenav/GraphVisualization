import networkx as nx
from networkx.readwrite import json_graph
import json


if __name__ == "__main__":
    g = nx.Graph(name='Twitter graph')
    with open("../data/data_twitter.json", "r") as f:
        lst = []
        for l in f:
            friend = json.loads(l, encoding='utf-8')
            if '_normal' in friend['img']:
                friend['img'] = friend['img'].replace('_normal', '')
            g.add_node(friend['id'], attr_dict=friend)

            lst.append(friend)

    for user in lst:
        for following in user['following']:
            if following in g:
                g.add_edge(user['id'], following)

    articulaciones = []

    for art in nx.articulation_points(g):
        articulaciones.append(art)

    for node in g.nodes():
        g.node[node]['degree'] = nx.degree(g, node)
        g.node[node]['closeness'] = nx.closeness_centrality(g, node)

        if node in articulaciones:
            g.node[node]['articulacion'] = 1
        else:
            g.node[node]['articulacion'] = 0

        if nx.clustering(g, node) < 0.33:
            g.node[node]['cluster'] = 0
        elif (nx.clustering(g, node) > 0.33) and (nx.clustering(g, node) < 0.66):
            g.node[node]['cluster'] = 1
        else:
            g.node[node]['cluster'] = 2

    with open("../data/json-graph.json", "w") as f:
        f.write(json.dumps(json_graph.node_link_data(g)))

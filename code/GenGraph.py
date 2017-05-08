# -*- coding: utf-8 -*-

import networkx as nx
from networkx.readwrite import json_graph
import json


if __name__ == "__main__":
    # g = nx.DiGraph(name='Twitter graph')
    g = nx.Graph(name='Twitter graph')
    # with open("../data/data_twitter_C.json", "r") as f:
    # with open("../data/data_twitter_M.json", "r") as f:
    # with open("../data/data_twitter_M_test_SIN_M.json", "r") as f:
    # with open("../data/data_twitter_M_test.json", "r") as f:
    with open("../data/data_twitter_MARVEL.json", "r") as f:
        lst = []
        for l in f:
            friend = json.loads(l, encoding='utf-8')
            if '_normal' in friend['img']:
                friend['img'] = friend['img'].replace('_normal','')
            # print(friend)
            g.add_node(friend['id'], attr_dict=friend)


            lst.append(friend)

    for user in lst:
        for following in user['following']:
            # if following in g.nodes():
            if following in g:
                g.add_edge(user['id'], following)
        # for follower in user['followers']:
        #     if follower in g:
        #         g.add_edge(follower,user['id'])


    # Metricas de grafos

    # print 'Clustering', nx.average_clustering(g)

    articulaciones = []

    for art in nx.articulation_points(g):
        articulaciones.append(art)
    print(articulaciones)

    for node in g.nodes():
        g.node[node]['degree'] = nx.degree(g, node)
        if node in articulaciones:
            g.node[node]['articulacion'] = 1
        else:
            g.node[node]['articulacion'] = 0

        if nx.clustering(g, node) < 0.25:
            g.node[node]['cluster'] = 0
        elif (nx.clustering(g, node) > 0.25) and (nx.clustering(g, node) < 0.50):
            g.node[node]['cluster'] = 1
        elif (nx.clustering(g, node) > 0.50) and (nx.clustering(g, node) < 0.75):
            g.node[node]['cluster'] = 2
        else:
            g.node[node]['cluster'] = 3
        # g.node[node]['articulation'] = nx.degree(g, node)
        # print('Clustering', nx.triangles(g, nodes=node))
        # print('Clustering', nx.square_clustering(g, nodes=node))





    with open("../data/json-graph.json","w") as f:
        f.write(json.dumps(json_graph.node_link_data(g)))
    # K_5 = nx.complete_graph(5)



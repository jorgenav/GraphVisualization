# -*- coding: utf-8 -*-

import networkx as nx
from networkx.readwrite import json_graph
from networkx_viewer import Viewer
import json


if __name__ == "__main__":
    g = nx.DiGraph(name='Twitter graph')
    # with open("../data/data_twitter_M.json", "r") as f:
    with open("../data/data_twitter_M_test.json", "r") as f:
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
        for follower in user['followers']:
            if follower in g:
                g.add_edge(follower,user['id'])


    # Metricas de grafos

    # print 'Clustering', nx.average_clustering(g)

    for node in g.nodes():
        # print(node)
        # print(nx.get_node_attributes(g,node))
        # print(g.node[node])
        g.node[node]['degree'] = nx.degree(g, node)


    # for conn_comp in nx.connected_components(g):
    #     print conn_comp
    #     print(len(conn_comp))

        # if len(conn_comp) > 1:
        #     print 'Degree: ', nx.degree_centrality(conn_comp)
        #     print 'Closeness: ', nx.closeness_centrality(conn_comp)
        #     print 'Betweenness: ', nx.betweenness_centrality(conn_comp)
        #     print 'PageRank: ', nx.pagerank(conn_comp)
        #     if (max_conn_comp is None) or (len(max_conn_comp) < len(conn_comp)):
        #         max_conn_comp = conn_comp


    # print(nx.clustering(g))

    # print(g.number_of_nodes())
    # print(json_graph.node_link_data(g))

    with open("../data/json-graph.json","w") as f:
        f.write(json.dumps(json_graph.node_link_data(g)))
    # K_5 = nx.complete_graph(5)


    # app = Viewer(K_5)
    # app = Viewer(g)
    # app.mainloop()
import networkx as nx
import pandas as pd
from itertools import chain

def cBMG_not_cograph():
    df= pd.read_csv('../examples/cBMG_not_cograph.txt', sep= '\t')
    nodes= set( chain.from_iterable( df.values ) )
    IDXs= {x:i for i,x in enumerate(nodes)}

    G= nx.DiGraph()
    F= lambda x: x[:-1]
    for x in nodes:
        G.add_node(IDXs[x], gene= x, species= F(x))
    G.add_edges_from(map(lambda X: list(map(lambda x: IDXs[x], X)) , df.values))
    return G

def BMG_2colored():
    """
    Two colores best match graph
    """
    G= nx.DiGraph()
    blue_nodes= ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
    red_nodes= ['b1', 'b2', 'b3', 'b4']
    nodes= blue_nodes + red_nodes
    nLabel= {x:i for i,x in enumerate(nodes)}
    #node_attrs= [(x, {'color': 'red'}) for x in blue_nodes] + [(x, {'color': 'blue'}) for x in red_nodes]
    node_attrs=  [(nLabel[x], {'gene': x, 'species': 'red'}) for x in blue_nodes]
    node_attrs+= [(nLabel[x], {'gene': x, 'species': 'blue'}) for x in red_nodes]

    G.add_nodes_from(node_attrs)

    edges= [('a1', 'b1'),
            ('a1', 'b2'),
            ('a1', 'b3'),
            ('a1', 'b4'),
            ('a2', 'b2'),
            ('a3', 'b3'),
            ('a4', 'b4'),
            ('a5', 'b2'),
            ('a5', 'b3'),
            ('a5', 'b4'),
            ('a6', 'b3'),
            ('a6', 'b4'),
            ('b1', 'a1'),
            ('b1', 'a2'),
            ('b1', 'a3'),
            ('b1', 'a4'),
            ('b1', 'a5'),
            ('b1', 'a6'),
            ('b2', 'a2'),
            ('b3', 'a3'),
            ('b4', 'a4'),
           ]

    edges= [(nLabel[ed[0]], nLabel[ed[1]]) for ed in edges]

    G.add_edges_from(edges)
    return G

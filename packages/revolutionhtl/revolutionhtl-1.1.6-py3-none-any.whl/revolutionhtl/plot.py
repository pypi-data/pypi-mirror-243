import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np
import pydot
import networkx as nx
from .nxTree import is_leaf

def plot_tree(tree, label_attr= None, ax= None):
    if label_attr!=None:
        labels= {x: tree.nodes[x][label_attr] for x in tree}
    else:
        labels= None
    pos = graphviz_layout(tree, prog="dot", root= tree.root)
    nx.draw(tree,
            pos,
            with_labels= True,
            node_color= [tree.nodes[x]['color'] for x in tree],
            labels= labels,
            ax= ax,
           )
    return plt.gcf()

rgbColor= np.array([[102, 102, 255, 1], [255, 0, 102, 1], [102, 255, 153, 1]])/255
rgbColor[:,-1]= 1
colors_plot= {'red': rgbColor[0,:],
              'blue': rgbColor[1,:]
             }

def plot_digraph(G):
    pos= nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color= [colors_plot[G.nodes[x]['color']] for x in G])
    nx.draw_networkx_edges(G, pos,
                           connectionstyle="arc3,rad=0.15", edge_color= rgbColor[-1,:],
                           width= 3
                          )
    nx.draw_networkx_labels(G, pos)
    fig= plt.gcf()
    fig.set_size_inches(8,8)
    return fig


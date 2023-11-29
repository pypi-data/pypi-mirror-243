import networkx as nx
from itertools import permutations
#from build_st_n import BUILDst_N
from . import nxTree as nxt
from .error import TreeDontExplainGraph

def LRT_from_cBMG(G, speciesAttr, geneAttr):
    triplets= _get_informative_triplets(G, geneAttr, speciesAttr)
    T= BUILDst_N( triplets, geneAttr, speciesAttr)
    G1= get_cBMG_of_T(T, speciesAttr, geneAttr)
    if not _are_equal_graphs(G, G1, geneAttr):
        raise TreeDontExplainGraph('The graph is not a cBMG')
    return T

def get_cBMG_of_T(T, color_attr, geneAttr):
    G1= nx.DiGraph()
    G1.add_edges_from( from_tree_2_cBMs(T, color_attr, geneAttr) )
    return G1

def from_tree_2_cBMs(T, color_attr, geneAttr):
    best_matches= []
    color_2_leafs= nxt.get_color2leafs(T, color_attr)
    for color0,color1 in permutations(color_2_leafs, 2):
        for x in color_2_leafs[color0]:
            best_matches+= [[x,y] for y in _get_best_matches_of_x(x, color_2_leafs[color1], T)]
    F= lambda x: T.nodes[x][geneAttr]
    return [list(map(F, X)) for X in best_matches]

def _are_equal_graphs(G, G1, geneAttr):
    are_equal= True
    for x in G:
        #are_equal= set(G[x]) == set(G1[x])
        x1= G.nodes[x][geneAttr]
        are_equal= {G.nodes[y][geneAttr] for y in G[x]} == set(G1[x1])
        if not are_equal:
            break
    return are_equal

def _get_informative_triplets(G, geneAttr, speciesAttr):
    """
    ...
    """
    DD= _get_color_2_nodes(G, speciesAttr)
    ret= []
    for color0, color1 in permutations(DD, 2):
        others= set(DD[color1])
        for node in DD[color0]:
            ret+= _get_node_inf_triplets(G, node, others, [color0, color1], geneAttr, speciesAttr)
    return ret

def _get_node_inf_triplets(G, node, others, colors, geneAttr, speciesAttr):
    """
    Se harán todas las tripletas de tipo 'node x | y'
    Donde el color de 'x' y 'y' son el mismo, pero diferente del color de 'node'.
    Además 'node -> x' en el grafo, pero no pasa que 'node -> y'

    Input:
    - G
    - node
    - others: Todos los nodos de un mismo color
    """
    neighbors= set(G[node])
    no_neighbors= others - neighbors
    return [_create_triplet(node, x, y, G, geneAttr, speciesAttr)
            for x in neighbors for y in no_neighbors]

def _create_triplet(node, x, y, G, geneAttr, speciesAttr):############ Revisar bien lo que debería hacer esta función y normalizar
    """
    The triplet is 'node x | y'
    """
    T= nx.DiGraph()
    T.root= 0
    T.add_nodes_from([0,1], species= None, gene= None)
    T.add_node(2, gene= G.nodes[y][geneAttr],
               species= G.nodes[y][speciesAttr])
    T.add_node(3, gene= G.nodes[node][geneAttr],
               species= G.nodes[node][speciesAttr])
    T.add_node(4, gene= G.nodes[x][geneAttr],
               species= G.nodes[x][speciesAttr])
    T.add_edges_from(((0,1),(0,2),(1,3),(1,4)))
    return T

def _get_color_2_nodes(G, colorAttr):
    DD= {}
    for node in G:
        color= G.nodes[node][colorAttr]
        DD[ color ]= DD.get(color, list()) + [node]
    return DD

def _compute_lca_hash(x, nodes, T):
    Y_x_t= {}
    for y in nodes:
        v= nxt.LCA(T, [x,y])
        Y_x_t[v]= Y_x_t.get(v, []) + [y]
    return Y_x_t

def _get_best_matches_of_x(x, nodes, T):
    Y_x_t= _compute_lca_hash(x, nodes, T)
    Y= list(Y_x_t)
    best= Y[0]
    for y in Y[1:]:
        if nxt.LCA(T, [best, y]) == best :
            best= y
    return Y_x_t[ best ]

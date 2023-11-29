import networkx as nx
from itertools import chain
from . import nxTree as nxt
from networkx.drawing.nx_pydot import graphviz_layout
from .error import InconsistentTrees

def BUILDst_N(profile, color_attr= None, *copyAttrs):
    """
    Input:
    NX trees con atributo color en los nodos
    Las hojas deben tener un label único dentro de cada árbol,
    pero deben de repetirse entre árboles.

    Para especificar el label, se define el kwordarg 'color_attr'. Por
    default el valor de este argumento es None.
    """
    # Init display graph
    H_p= _create_display_graph(profile, color_attr, copyAttrs)
    position= _get_initial_position(H_p)

    # Init output tree
    T= nx.DiGraph() # Create new tree
    T.add_node(0)
    T.root= 0
    nIdx= 1 # ID of the next inner node

    # Check if display graph is conected
    CC= list(nx.weakly_connected_components( _induced_sub_display(H_p, position) ))
    if len(CC) == 1:
        Q= [(position, T.root)]
    else:
        T.add_node(nIdx)
        T.add_edge(T.root, nIdx)
        Q= [(cc.intersection(position), nIdx) for cc in CC]
        nIdx+= 1

    while len(Q) > 0:
        position, pred= Q.pop(0)
        ind_leafs= _get_pseudoleafs(H_p, position, color_attr)
        len_ind_l= len(ind_leafs)
        if len_ind_l==1:
            leaf= ind_leafs.pop()
            attrs= H_p.nodes[leaf]
            T.add_node(nIdx, **attrs)
            T.add_edge(pred, nIdx)
            nIdx+= 1
        elif len_ind_l==2:
            leaf1, leaf2= ind_leafs
            XX= nIdx
            #
            T.add_node(XX)
            T.add_edge(pred, XX)
            nIdx+= 1
            #
            attrs= H_p.nodes[leaf1]
            T.add_node(nIdx, **attrs)
            T.add_edge(XX, nIdx)
            nIdx+= 1
            #
            attrs= H_p.nodes[leaf2]
            T.add_node(nIdx, **attrs)
            T.add_edge(XX, nIdx)
            nIdx+= 1
        else:
            T.add_node(nIdx)
            T.add_edge(pred, nIdx)
            position= _compute_successor(position, H_p)
            CC= list(nx.weakly_connected_components( _induced_sub_display(H_p, position) ))
            dQ= [(cc.intersection(position), nIdx) for cc in CC]
            if len(CC)==1:
                raise InconsistentTrees('Inconsistent profile')
            # Actualizar cola
            Q+= dQ
            nIdx+= 1

    return T

def _create_display_graph(profile, color_attr, copyAttrs):
    """
    Constructs a directed display graph [REvolutionH-tl paper]
    It is a modification of [display_graph paper]
    """
    H_p= nx.DiGraph()
    H_p.roots= set()
    nodes_relation, idx= _create_display_nodes(profile, H_p, color_attr, copyAttrs)
    _create_display_edges(profile, nodes_relation, H_p)
    _add_display_colors(H_p, color_attr, idx, copyAttrs)
    return H_p


def _create_display_nodes(profile, H_p, color_attr, copyAttrs):
    """
    Combine all the trees of in profile to a single directed graph H_p.

    Input:
    - Profile: list of nxTrees
    - H_p: empti nx.DiGraph with the attribute '.roots' as an empty set.
    - color_attr: string specifying the attribute for leafs color.

    This function manipulates the H_p graph as follows:
    - Addition of nodes: For each node v in the trees, it is created a node
      u in H_p.
    - Identification of roots: The roots of the original trees are stored
      in the attribute H_p.roots
    - Each of the created nodes have the attributes:
      - inner_label: Keeps the node v
      - tree_idx: Keeps the index in the profile where is stored de tree containing v
      - color: This attribute is copied from v

    Output:
    - nodes_relation (dict): A bijective mapping; for each tuple
      (T_i, v) there is a node u, where T_i is a tree in the profile,
      v is a vertex in T_i, and u is the corresponding vertex created
      in H_p.
    - idx (int): The total number of nodes in the original trees.
    """
    idx= 0
    nodes_relation= {}
    tree_idx= 0
    for X in profile:
        H_p.roots.add(idx)
        for x in nxt.BFS_graph(X, X.root):
            nodes_relation[(X,x)]= idx
            x_attrs= {'inner_label': x,
                      'tree_idx': tree_idx,
                     }

            if nxt.is_leaf(X, x):
                x_attrs.update({color_attr: X.nodes[x][color_attr]})
                x_attrs.update({atr: X.nodes[x][atr] for atr in copyAttrs})

            H_p.add_node(idx, **x_attrs)
            idx+= 1
        tree_idx+= 1
    return nodes_relation, idx

def _create_display_edges(profile, nodes_relation, H_p):
    """
    Add the edges in H_p that are equivalent to those in
    the profile using the map nodes_relation.
    """
    for X in profile:
        for x in X:
            idxx= nodes_relation[(X,x)]
            for y in X[x]:
                idxy= nodes_relation[(X,y)]
                H_p.add_edge(idxx, idxy)

def _add_display_colors(H_p, color_attr, idx, copyAttrs):
    """
    Create the a unique node for each of the colors present
    in the leafs of the profile, and creates an arc from such nodes
    to the leafs of the corresponding color.
    """
    colors= {}
    edges= []
    for x in H_p.roots:
        for y in nxt.induced_leafs(H_p, x):
            node_color= H_p.nodes[y][color_attr]
            if node_color in colors:
                ID= colors[node_color]
            else:
                colors[node_color]= ID= idx
                attrs= {color_attr: node_color}
                attrs.update({atr: H_p.nodes[y][atr] for atr in copyAttrs})
                H_p.add_node(ID, **attrs)
                idx+= 1
            H_p.add_edge(ID, y)
            H_p.nodes[y]['color_node']= ID
            

def _get_initial_position(H_p):
    return H_p.roots

def _get_pseudoleafs(H_p, position, color_attr):
    position_leafs= set(chain.from_iterable(nxt.induced_leafs(H_p, x) for x in position))
    #return {H_p.nodes[x][color_attr] for x in position_leafs}
    return {H_p.nodes[x]['color_node'] for x in position_leafs}

def _get_semiuniversal(position, H_p):
    tree_to_subPos= {}
    for x in position:
        tree_idx= H_p.nodes[x]['tree_idx']
        # Agregar el nodo a la lista de nodos del árbol
        # Si no existe dicha lista, la crea
        tree_to_subPos[ tree_idx ]= tree_to_subPos.get(tree_idx, []) + [x]
    return {L[0] for tree_idx,L in tree_to_subPos.items() if len(L)==1}

def _compute_successor(position, H_p):
    semiuniversal= _get_semiuniversal(position, H_p)
    semihijos= set(chain.from_iterable([set(H_p[x]) for x in semiuniversal]))
    return (position - semiuniversal).union(semihijos)

def _induced_sub_display(H_p, position):
    nbunch= {y for x in position for y in nxt.BFS_graph(H_p, x)}
    nbunch.update({H_p.nodes[x]['color_node'] for x in nbunch if nxt.is_leaf(H_p, x)})
    return nx.induced_subgraph(H_p, nbunch)


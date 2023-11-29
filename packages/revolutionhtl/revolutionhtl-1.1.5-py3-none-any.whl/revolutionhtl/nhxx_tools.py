import networkx as nx
from itertools import chain, product
from .nxTree import set_sparce_matrix

_name_attr= 'label'

def tralda_to_nxTree(tralda_tree, name_attr= 'accession'):
    newick= tralda_tree.to_newick()
    nxT= read_nhxx(newick, name_attr= name_attr)
    return nxT

def _add_node(T, node, dad):
    T.add_node(node)
    T.add_edge(dad, node)

def _add_node_info(T,
                   node,
                   cache_label,
                   cache_weigth,
                   cahce_dict,
                   name_attr= _name_attr,
                   branch_length_attr= 'length',
                  ):
    if cache_label != None:
        T.nodes[node][name_attr]= cache_label
    else:
        T.nodes[node][name_attr]= node

    if cache_weigth != None:
        T.nodes[node][branch_length_attr]= float(cache_weigth)

    T.nodes[node].update(cahce_dict)

def _update_cache_dict(cache_key, cache_value, cahce_dict, attrs_type, use_nhx_flag, add_attrs):
    if add_attrs:
        typer= attrs_type.get(cache_key, lambda x: x)
        cahce_dict[cache_key]= typer(cache_value)

def ask_attrs(add_attrs, use_nhx_flag, cache_key):
    if use_nhx_flag:
        if cache_key=='&&NHX':
            add_attrs= True
    else:
        add_attrs= True
    return add_attrs

def read_nhxx(nhx,
              name_attr= _name_attr,
              attr_sep= ';',
              attrs_type= {},
              use_nhx_flag= False,
              fill_missed_attrs= True,
             ):
    # Init tree
    T= nx.DiGraph()
    T.add_node(0, **{name_attr: 0})
    T.root= 0

    # Auxiliar variables
    current= 0    # Current node
    idx= 1        # Index for new nodes
    S= [0]        # Stack of visited inner nodes
    last_controller= None

    reading_label= False
    cache_label= None
    reading_weight= False
    cache_weigth= None
    reading_comment= False
    cache_key= None
    cache_value= None
    cahce_dict= {}
    clasp_count= 0 # Cuenta si hay caracteres '[' en el comentario, todos deben ser cerrados.
    is_key= False
    is_value= False
    add_attrs= False
    end_comment= None

    for x in nhx:
        if reading_comment:
            if x=='[':
                clasp_count+= 1
            elif x==']':
                if clasp_count==0:
                    add_attrs= ask_attrs(add_attrs, use_nhx_flag, cache_key)
                    _update_cache_dict(cache_key, cache_value, cahce_dict, attrs_type, use_nhx_flag, add_attrs)
                    reading_comment= False
                    is_key= is_value= False
                    cache_key= cache_value= None
                    add_attrs= False
                    end_comment= True
                else:
                    clasp_count-= 1
            if x=='=':
                is_key= False
                is_value= True
                cache_value= ''
            elif x==attr_sep:
                add_attrs= ask_attrs(add_attrs, use_nhx_flag, cache_key)
                _update_cache_dict(cache_key, cache_value, cahce_dict, attrs_type, use_nhx_flag, add_attrs)
                is_key= is_value= False
                cache_key= cache_value= None
            elif is_key:
                cache_key+= x
            elif is_value:
                cache_value+= x
            elif not end_comment:
                is_key= True
                is_value= False
                cache_key= x
        elif x=='(':
            last_controller= '('
            # Create node
            _add_node(T, idx, current)
            S+= [idx]
            current= idx
            idx+= 1
        elif x==',':
            last_controller= ','
            # End of node
            _add_node_info(T, current, cache_label, cache_weigth, cahce_dict, name_attr= name_attr)
            cache_label= cache_weigth= None
            cahce_dict= {}
            reading_label= reading_weight= reading_comment= False
            current= S[-1]
        elif x==')':
            last_controller= ')'
            # End of node
            _add_node_info(T, current, cache_label, cache_weigth, cahce_dict, name_attr= name_attr)
            cache_label= cache_weigth= None
            cahce_dict= {}
            reading_label= reading_weight= reading_comment= False
            # Exit node
            current= S.pop()
        elif x=='[':
            last_controller= '['
            reading_comment= True
            end_comment= False
        elif x==':':
            last_controller= ':'
            reading_weight= True
            reading_label= False
            cache_weigth= ''
        elif x==';':
            last_controller= ';'
            # End of node
            _add_node_info(T, current, cache_label, cache_weigth, cahce_dict, name_attr= name_attr)
            # Pop last element of stack
            S.pop()
            break
        else:
            # Reading node name or weight
            if reading_label:
                cache_label+= x
            elif reading_weight:
                cache_weigth+= x
            else:
                reading_label= True
                cache_label= x
                if last_controller!=')':
                    _add_node(T, idx, current)
                    current= idx
                    idx+= 1
    if len(S)>0:
        msg= f'";" found before closing all the parenthesis: {S}'
        raise ValueError(msg)

    if fill_missed_attrs:
        all_attrs= set(chain.from_iterable( dict(T.nodes(data= True)).values() ))
        for x,attr in product(T, all_attrs):
            if attr not in T.nodes[x]:
                T.nodes[x][attr]= None

    # Add attributes for rmq-lca
    set_sparce_matrix(T)

    return T

def get_nhx(T,
            root= None,
            name_attr= None,
            attr_sep= ';',
            ignore_attrs= [],
            ignore_inner_name= False,
            include_none= False,
            use_nhx_flag=False,
           ):
    if not root:
        root= T.root

    newick= {}
    for node in nx.dfs_postorder_nodes(T, source= root):
        if len(T[node])==0 :
            nwk_n= str(T.nodes[node].get(name_attr, ''))
        else:
            nwk_n= '(' + ','.join([ newick[son] for son in T[node] ]) + ')'
            if not ignore_inner_name:
                nwk_n+= str(T.nodes[node].get(name_attr, ''))

        c_attrs= set((at for at in T.nodes[node] if (include_none or T.nodes[node][at]!=None)))
        c_attrs-= set(ignore_attrs+[name_attr])
        if len(c_attrs) > 0:
            nwk_n+= '[' + attr_sep.join((f'{x}={T.nodes[node][x]}' for x in c_attrs)) +']'

        newick[ node ]= nwk_n
    return newick[root]+';'

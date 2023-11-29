import pandas as pd
import os
import numpy as np
import networkx as nx
from itertools import chain
from tqdm import tqdm
tqdm.pandas()
from Bio.SeqIO.FastaIO import SimpleFastaParser

from .common_tools import norm_path
from .in_out import create_cBMG, tl_digraph_from_pandas
from .reduce_giant import reduce_graph

####################
#                  #
# Some parameters  #
#                  #
####################

from .constants import _diamond_tl_headers, _default_f, _df_matches_cols

####################
#                  #
# Parse functions  #
#                  #
####################

normalization_modes= ['query', 
                      'target', 
                      'alignment', 
                      'smallest',
                      'raw', 
                     ]
normalization_smallest=['smallest_bidirectional', 'smallest_directed']

colRelation= {'query' : 'Query_length',
              'target' : 'Target_length',
              'alignment' : 'Alignment_ength',
              'smallest' : None,
             }

def _parse(path, f_value, singletons, fastaspath, mode= 'normal', N_max= 2000):
    if mode in normalization_modes:
        df_hits= parse_prt_files(path, mode)
    else:
        raise ValueError(f'Mode for parsing only can be one of: {", ".join(normalization_modes)}')
    # select best hits
    df= select_best_hits(df_hits, f_value)
    # Identify orthogroups
    df, OGs_table= identify_orthogroups(df, N_max= N_max)
    if singletons:
        singletons= identify_singletons(OGs_table, fastaspath)
    return df, OGs_table, singletons

def simple_species_parser(file):
    species= file.split('/')[-1].split('.')
    return species[0], species[2]

def prt_species_parser(file):
    species= file.split('/')[-1].split('.')
    return species[0], species[3]

def select_best_hits(df_hits, f_value, a= 'Query_accession', b= 'Target_accession'):
    """
    Input:
    - path: A directory containing reciprocal blast-like analisis between pairs of species.
            The files contained there should be named as follows: <species_a>.fa.vs<species_b.fa>.blast
    - f_value: used for the dinamic threshold.
    """
    # Identify best hit scores w.r.t. query_gene and target_species
    w_x_B= max_hit_scores(df_hits)
    # Apply dynamic threshold for best hit selection
    print('Selecting best hits by dynamic threshold...')
    is_best_hit= lambda row: row.Normalized_bit_score >= f_value * w_x_B[ row.Query_accession, row.Target_species ]
    mask= df_hits.progress_apply(is_best_hit, axis= 1)
    df_best_hits= df_hits.loc[mask]
    return df_best_hits

def identify_orthogroups(df_best_hits,
                         Query_accession= 'Query_accession',
                         Target_accession= 'Target_accession',
                         Query_species= 'Query_species',
                         Target_species= 'Target_species',
                         N_max= 2000):
    # Create graph
    G= nx.DiGraph()
    G.add_edges_from( df_best_hits[[Query_accession,Target_accession]].values )
    # Identify connected components
    CCs= pd.Series(list(nx.weakly_connected_components(G)))
    # Reduce giant connected components
    mask_giant= CCs.apply(lambda X: len(X)>N_max)
    reduced_CCs= CCs[ mask_giant ].apply(lambda X: reduce_graph(nx.induced_subgraph(G, X), N_max= N_max))
    # Obtain singletons list
    singletons= reduced_CCs.str[1]
    singletons= set(chain.from_iterable(singletons.values))
    # Obtain graph partitions
    reduced_CCs= reduced_CCs.str[0]
    reduced_CCs= pd.Series(list(chain.from_iterable(reduced_CCs.values)), dtype='object')
    # Make final CCs list
    CCs= pd.concat((CCs[ ~mask_giant ], reduced_CCs), ignore_index= True)
    # Sort connected components by size and gene names
    CCs= pd.DataFrame(dict(CCs= CCs,
                           N= CCs.str.len(),
                           name= CCs.apply(lambda X: ''.join(sorted(''.join(X)))),
                          ))
    CCs= CCs.sort_values(by= ['N', 'name']).CCs
    # Asign a number for each connected component
    idx_2_og= dict(enumerate(CCs.values))
    D= {x: i for i,X in idx_2_og.items() for x in X}
    # Quit singletons w.r.t partition
    F= lambda x: x not in singletons
    df_best_hits= df_best_hits[ df_best_hits[Query_accession].apply(F) & df_best_hits[Target_accession].apply(F) ]
    # Keep only intra-hits w.r.t partition
    df_best_hits= df_best_hits[ df_best_hits.apply(lambda X: D[X[Query_accession]]==D[X[Target_accession]], axis= 1) ]
    # Asign a connected component to each row of dataframe
    cols= list(df_best_hits.columns)
    df_best_hits['OG']= df_best_hits[Query_accession].apply(lambda x: D[x])
    # Sort rows by OG
    df_best_hits= df_best_hits[['OG']+cols].sort_values('OG')

    # Create OGs table
    OGs_table= create_og_table(df_best_hits, idx_2_og,
                               Query_accession,
                               Target_accession,
                               Query_species,
                               Target_species)

    return df_best_hits, OGs_table

def identify_singletons(df, fastaspath):
    """
    df: dataframe for orthogroups
    fastaspath: list of fasta files
    """
    # Identify genes in orthogroups
    species_columns= list(df.columns)[3:]
    F= lambda X: X.split(',')
    genes_og= df[species_columns].apply(lambda row: chain.from_iterable(F(X) for X in row.dropna()) , axis= 1)
    genes_og= set(chain.from_iterable(genes_og.values))

    # Identify genes in fasta files
    genes_fa= set()
    DD= dict()
    for file in fastaspath:
        with open(file) as F:
            fgenes= [title.split()[0] for title, _ in SimpleFastaParser(F)]
        genes_fa.update(fgenes)
        DD.update({x:file.split('/')[-1] for x in fgenes})
    singletons= genes_fa - genes_og
    singletons= [[x, DD[x]] for x in singletons]
    singletons= pd.DataFrame(singletons, columns= ['gene', 'file'])
    return singletons.sort_values('file')

def get_species_columns(genes, species, gene2species, idx):
    ret= {}
    for gene in genes:
        spec= gene2species[gene]
        ret[spec]= ret.get(spec, []) + [gene]

    nGenes= len(genes)
    nSpecies= len(ret)

    return [idx, nGenes, nSpecies] + [','.join(ret.get(spec, []))
                                      for spec in species]

def create_og_table(df_BHs, idx_2_og,
                    Query_accession,
                    Target_accession,
                    Query_species,
                    Target_species):
    # Create genesdict
    gene2species= pd.DataFrame(
        list(df_BHs[[Query_accession,
                     Query_species]].values) + list(df_BHs[[Target_accession,
                                                            Target_species]].values
                                                   ),
        columns= ['gene', 'species']
    ).drop_duplicates().set_index('gene').species

    # Create species set
    species_list= sorted(set(gene2species))

    # Create map OG->species->gene
    OGs_table= pd.DataFrame([get_species_columns(genes, species_list, gene2species, idx)
                             for idx, genes in idx_2_og.items()],
                            columns= ['OG', 'n_genes', 'n_sepecies'] + species_list
                           )
    return OGs_table

def parse_prt_files(path,
                    normalization_method,
                        Query_accession= 'Query_accession',
                        Target_accession= 'Target_accession',
                        Query_species= 'Query_species',
                        Target_species= 'Target_species',
                        pd_params= dict(names= _diamond_tl_headers, sep= '\t'),
                    species_parser= simple_species_parser,
                       ):
    print('Reading .proteinortho.tsv file and hits directory...')
    # Load prt hits
    df_hits= parse_prt_hits(norm_path(path),
                            pd_params= pd_params,
                            species_parser= species_parser,
                           )
    # Normalize
    if normalization_method == 'smallest':
        df_hits['SMALLEST']= df_hits[['Query_length', 'Target_length']].min(axis=1)
        df_hits= normalize_scores(df_hits,
                                  Query_accession,
                                  Target_accession,
                                  'Bit_score',
                                  'SMALLEST',
                                  Query_species,
                                  Target_species)

    elif normalization_method != 'raw':
        df_hits= normalize_scores(df_hits,
                                  Query_accession,
                                  Target_accession,
                                  'Bit_score',
                                  colRelation[normalization_method],
                                  Query_species,
                                  Target_species)
    DD= {'Bit_score':'Normalized_bit_score'}
    df_hits.columns= [DD.get(x,x) for x in df_hits.columns]
    return df_hits

def normalize_scores(df, a, b, score, norm_factor, a_s, b_s):
    normalized_score= pd.DataFrame({a_s : df[a_s],
                                    b_s : df[b_s],
                                    a : df[a],
                                    b : df[b],
                                    score : df[score]/df[norm_factor]})

    DD= {(Q,T):S for Q,T,S in normalized_score[[a,b,score]].values}
    SS= dict(normalized_score[[a,a_s]].values)
    SS.update(dict(normalized_score[[b,b_s]].values))
    hits= {frozenset(X) for X in DD}

    def normalize(T,Q):
        N=0
        S= 0
        edges= [(Q,T), (T,Q)]
        for edge in edges:
            if edge in DD:
                S+= DD[edge]
                N+= 1
        return S/N

    D1= {(Q,T) : normalize(Q,T)
         for Q,T in hits}

    permutate= lambda X: (X, X[::-1])
    normalized_score= [(SS[Q],SS[T],Q,T,D1[X])
                       for X in D1 for Q,T in permutate(X)]
    normalized_score= pd.DataFrame(normalized_score,
                                   columns= [a_s,b_s,a,b,score]
                                  )

    return normalized_score    

def parse_prt_orthogroups(orthogroups_file, clear_singletons= True):
    df_prt= pd.read_csv(orthogroups_file, sep= '\t')
    species_cols= list(map(lambda x: x.split('.')[0], df_prt.columns[3:]))
    df_prt.columns= ['Species', 'Genes', 'Alg.-Conn.']+species_cols
    df_prt[species_cols]= df_prt[species_cols].apply(lambda X: X.apply(lambda x: set(x.split(','))))
    df_prt.index.name= 'OG'
    if clear_singletons:
        df_prt= _clean_prt(df_prt)
    return df_prt

def parse_prt_hits(hits_dir,
                   hit_file_ext= '.alignment_hits',
                   Query_accession= 'Query_accession',
                   pd_params= dict(names= _diamond_tl_headers, sep= '\t'),
                   species_parser= simple_species_parser
                  ):
    """
    Returns a DataFrame of hits obtained from proteinortho files
    """

    df= pd.concat((_read_bh_table(f'{hits_dir}/{file}',
                                 pd_params,
                                 Query_accession= Query_accession,
                                 species_parser= species_parser,
                                 )
                   for file in os.listdir(hits_dir) if file.endswith(hit_file_ext)
                  ))
    return df

def _read_bh_table(file, pd_params, Query_accession, species_parser= simple_species_parser):
    """
    Para que funcione, el archivo debe ser llamado algo así como: 
    H0.vs.H10.diamond
    """
    species= species_parser(file)
    df= pd.read_csv(file, **pd_params)
    columns= list(df.columns)
    df['Query_species']= species[0]
    df['Target_species']= species[1]
    return df[ ['Query_species', 'Target_species']+columns ]

def max_hit_scores(df_hits,
                   Query_accession= 'Query_accession',
                   Target_species= 'Target_species',
                   Score= 'Normalized_bit_score',
                  ):
    return df_hits.groupby([Query_accession, Target_species])[Score].max()


def _get_orthogroup_hits(row, df_hits):
    """
    Input:
    - row: A row from an orthogroups table (.proteinortho.tsv)
    - df_hits: table of best hits (Query_gene -> Target_gene)
    """
    genes= set(chain.from_iterable(row))
    mask= (df_hits.Query_accession.isin(genes)) & (df_hits.Target_accession.isin(genes))
    og_hits= df_hits[ mask ]
    og_hits['OG']= row.name
    return og_hits

def _clean_prt(df_prt):
    mask= df_prt.Species > 1
    species= list(df_prt.columns[3:])
    return df_prt.loc[mask, species]

def read_symBets(prt_graph_path, prt_path):
    # Loads symBets (proteinortho-graph)
    symBets= pd.read_csv(prt_graph_path, sep='\t', comment= '#', names= ['a',
                                                                         'b',
                                                                         'evalue_ab',
                                                                         'bitscore_ab',
                                                                         'evalue_ba',
                                                                         'bitscore_ba',
                                                                        ])

    # Loads proteiortho table containng orthogroups
    df_prt= parse_prt_orthogroups(prt_path)

    # For each ortogroup obtain the orthology relations of all the genes in such orthogroup
    F= lambda x: _get_orthos(x, symBets)
    df_edges= pd.concat( list(df_prt.apply(F, axis= 1)) )

    return df_edges

def _get_orthos(row, symBets):
    orths= pd.concat((_search_orths(row, X, symBets) for X in row.index))
    orths['OG']= row.name
    return orths.set_index('OG').sort_index()

def _search_orths(row, species, symBets):
    mask= lambda x: symBets[ (symBets.a==x) | (symBets.b==x) ]
    return pd.concat(map(mask, row[species]))

####################
#                  #
# General functions#
#                  #
####################

def _check_files(path):
    prt_path= [x for x in os.listdir(path) if x.endswith('.proteinortho.tsv')]
    if len(prt_path)==1:
        prt_path= path + prt_path[0]
    else:
        raise ValueError(f'There is more than one ".proteinortho.tsv" file at {path}')
    return prt_path

def _get_prt_projectname(prt_file):
    return prt_file.split('/')[-1].split('.')[0]


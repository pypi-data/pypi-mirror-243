
desc_def= """ | Steps :
1. Alignment hits computation
2. Best hit selection
3. Gene tree reconstruction and orthology inference
4. Species tree reconstruction
5. Gene and species trees reconciliation | 
More details at: https://pypi.org/project/revolutionhtl/
"""




if __name__ == "__main__":
    from .reconciliation import reconciliate_many, recon_table_to_str
    from .error import InconsistentTrees, MissedData, ParameterError
    from .orthology import orthologs_from_trees_df
    from .supertree import from_gene_forest
    from .constants import _df_matches_cols, _default_f
    from .hug_free import build_graph_series
    from .parse_prt import _parse, normalization_modes, normalization_smallest
    from .common_tools import norm_path
    from .cBMG_tools import analyze_digraphs_list
    from .nhxx_tools import read_nhxx, get_nhx
    from .in_out import read_tl_digraph, tl_digraph_from_pandas
    from .diamond import diamond_all_vs_all
    from .blast import blast_all_vs_all
    from .tree_correction import correct_tree_df

    from tqdm import tqdm
    from numpy import argsort
    import pandas as pd
    import os
    from datetime import datetime
    from importlib.metadata import version
    from networkx import DiGraph

    import argparse

    V_tl= version('revolutionhtl')
    V_tl

    txt= f'REvolutionH-tl: Reconstruction of Evolutionaty Histories TooL (V{V_tl})'

    parser = argparse.ArgumentParser(prog= 'revolutionhtl',
                                     description=f'{txt}{desc_def}',
                                     usage='python -m revolutionhtl <arguments>',
                                     formatter_class=argparse.MetavarTypeHelpFormatter,
                                    )

    # Arguments
    ###########

    # Input data
    # ..........
    parser.add_argument('-steps',
                        help= 'List of steps to run (default: 1 2 3 4).',
                        type= int,
                        nargs= '*',
                        default= [1, 2, 3, 4, 5]
                       )

    parser.add_argument('-F', '--fastas',
                        help= '[str | Input for step 1] Directory containing fasta files.',
                        type= str,
                        default= None
                       )

    parser.add_argument('-alignment_h', '--alignment_hits',
                        help= '[str | Input for step 2] Directory containing alignment hits.',
                        type= str,
                        default= None
                       )

    parser.add_argument('-best_h', '--best_hits',
                        help= '[str | Input for step 3] .tsv file containing best hits.',
                        type= str,
                        default= None,
                       )

    parser.add_argument('-T', '--gene_trees',
                        help= '[str | Input for steps 4 and 5] .tsv file containing gene trees in nhx format.',
                        type= str,
                       )

    parser.add_argument('-S', '--species_tree',
                        help= '[str | Input for step 5] .nhx file containing a species tree.',
                        type= str,
                        default= None,
                       )

    # Parameters
    # ..........
    al_default= 'diamond'
    parser.add_argument('-aligner', '--aligner',
                        help= f'[str | Parameter for step 1 | Default: {al_default}] Command or path to the program for computation of aligment hits. Supported: diamond, blastn, blastp',
                        type= str,
                        default= al_default)
    parser.add_argument('-v', '--verbose_diamond', action='store_true',
                        help= '[flag | Parameter for step 1 ] Use to display diamond messages.')
    e_default= 0.00001
    parser.add_argument('-e', '--evalue', default= e_default, type= float,
                        help= f'[float | Parameter for step 1 | Default: {e_default}] Maximum evalue required to consider significant an aligment hit.'
                       )
    mk_def= 'makeblastdb'
    parser.add_argument('-m_command', '--makeblastdb', default= mk_def, type= str,
                        help= f'[str | Parameter for step 1 | Default: {mk_def}] BLAST command or path to the BLAST program for database creation.')
    id_def= 25
    parser.add_argument('-id', '--identity', default= id_def, type= int,
                        help= f'[float | Parameter for step 1 | Default: {id_def}] Minimum percentage of identity required to report an alignment hit.')
    cov_def= 50
    parser.add_argument('-cov', '--coverture', default= cov_def, type= int,
                        help= f'[float | Parameter for step 1 | Default: {cov_def}] Minimum percentage of query coverture required to report an alignment hit.')
    kh_def= 100
    parser.add_argument('-k_hits', '--max_target_seqs', default= kh_def, type= int,
                        help= f'[int | Parameter for step 1 | Default: {kh_def}] Maximum number of alignment hits per gene againist a fixed species.')

    bhh_def= 'target'
    parser.add_argument('-bh_heuristic', '--besthit_heuristic',
                        help= f'[str | Parameter for step 2 | Default: {bhh_def}] Indicates how to normalize bit-score. Normalize by sequence lenght: query, target, alignment, smallest. No normalization: raw.',
                        type= str,
                        choices= ['query', 'target', 'alignment', 'smallest', 'raw'],
                        default= bhh_def,
                       )

    parser.add_argument('-f', '--f_value',
                        help= f'[float | Parameter for step 2 | Defualt: {_default_f}] Number between 0 and 1. Defines the adaptative threshhold for best-hit selection as: f*max_bit_score.',
                        type= float,
                        default= _default_f,
                       )

    com_def= 'Louvain'
    com_opt= ['Mincut', 'BPMF', 'Karger', 'Greedy', 'Gradient_Walk', 'Louvain', 'Louvain_Obj']
    parser.add_argument('-bmg_h', '--bmg_heuristic',
                        help= f'[str | Parameter for step 3 | Defult: {com_def}] Comunity detection method for MaxConsistentTriples heuristic. Options: {", ".join(com_opt)}.',
                        type= str,
                        default= com_def,
                        choices= com_opt,
                       )

    parser.add_argument('-no_binary_R', '--no_binary_triples',
                        help= '[flag | Parameter for step 3 ] Use to avoid the usage of binary triples from best-hit graph.',
                        action= 'store_false',
                       )


    parser.add_argument('-f_bT', '--force_binary_gene_tree',
                        help= '[flag | Parameter for step 3 ] Use to force gene trees to be binary.',
                        action= 'store_true',
                       )

    parser.add_argument('-T_no_db', '--gene_tree_no_double_build',
                        help= '[flag | Parameter for step 3 ] Use to avoid running build twice in the MaxConsistentTriples heuristic.',
                        action= 'store_false',
                       )

    com_def= 'louvain_weight'
    com_opt= ['naive', 'louvain', 'mincut', 'louvain_weight']
    parser.add_argument('-stree_h', '--species_tree_heuristic',
                        help= f'[str | Parameter for step 4 | Default: {com_def}] Comunity detection method for MaxConsistentTriples heuristic. Options: {", ".join(com_opt)}.',
                        type= str,
                        default= com_def,
                        choices= com_opt
                       )

    sr_def= 3
    parser.add_argument('-streeh_repeats', '--stree_heuristic_repeats',
                        help= f'[int | Parameter for step 4 | Default: {sr_def}] Specifies how many times run the MaxConsistentTriples heuristic.',
                        type= int,
                        default= sr_def
                       )

    parser.add_argument('-streeh_b', '--streeh_binary',
                        help= '[flag | Parameter for step 4] Use to force specis tree to be binary.',
                        action= 'store_true',
                       )

    parser.add_argument('-streeh_ndb', '--streeh_no_doble_build',
                        help= '[flag | Parameter for step 4] Use to avoid running build twice in the MaxConsistentTriples heuristic.',
                        action= 'store_false',
                       )

    parser.add_argument('-n_edit_T', '--do_not_edit_inconsistent_trees',
                        help= '[flag | Prameter for step 5] Use to avoid editing of inconsistent gene trees.',
                        action= 'store_true',
                       )   
    # Format parameters
    # .................

    pr_def= 'tl_project'
    parser.add_argument('-o', '--output_prefix',
                        help= f'[str | Default: {pr_def}] Prefix for output files.',
                        type= str,
                        default= pr_def,
                       )

    fa_def= '.fa'
    parser.add_argument('-fext', '--fasta_ext',
                        help= f'[str | Default: {fa_def}] Extesion for fasta files.',
                        type= str,
                        default= fa_def,
                       )

    parser.add_argument('-singletons',
                        help= "[flag | Prameter for step 2] Use to print singletons, i.e. genes that weren't assigned to an orthogroup.",
                        action= 'store_true',
                       )

    og_def= 'OG'
    parser.add_argument('-og', '--orthogroup_column',
                        help= f'[str | Default: {og_def}] Column specifying orthogroup ID in input and output .tsv files.',
                        type= str,
                        default= og_def,
                       )

    nm_def= 2000
    parser.add_argument('-Nm', '--N_max',
                        help= f'[int | Default: {nm_def}] Maximum number of genes in a orthogroup, bigger orthogroups are splitted. If 0, no orthogroup is splitted.',
                        type= int,
                        default= nm_def,
                       )

    ks_def= 100
    parser.add_argument('-k', '--k_size_partition',
                        help= f'[int | Default: {ks_def}] Range in the numer of genes of orthogroups procesed in batch: first those with <k genes, then <2k. then <3k, and so on.',
                        type= int,
                        default= ks_def,
                       )

    sep_def= ';'
    parser.add_argument('-S_attr', '--S_attr_sep',
                        help= f'[str | Default: {sep_def}] Attribute delimiter in the input .nhx file (Input of step 5).',
                        type= str,
                        default= sep_def,
                       )

    args= parser.parse_args()

    ################
    # Process data #
    ################

    from .hello import hello5
    print(f'{hello5}V{V_tl}\n')

    allowed_steps= {1, 2, 3, 4, 5}
    bad_steps= set(args.steps) - allowed_steps
    if len(bad_steps) > 0:
        raise ParameterError(f'Only steps 1, 2, 3, 4, and 5 are allowed to be used in the parameter -steps. ')
    else:
        args.steps= sorted(set(args.steps))

    print(f'Running steps {", ".join(map(str, args.steps))}')

    logfile= f'{args.output_prefix}_log.txt'
    with open(logfile, 'a') as F:
        DD= vars(args)
        keys= sorted(DD)
        log= (f'{k}={DD[k]}' for k in keys)
        log= '\n'.join(log)+'\n'
        log= f'> {datetime.now()}\n> REvolutionH-tl V{V_tl}\n{log}'
        log= f'----------------------------------------------\n{log}'
        F.write(log)

    # 1. Alignment hits computation
    ###########################

    if 1 in args.steps:
        if type(args.fastas)!=str:
            raise MissedData('Step 1 needs a value for the parameter --fastas.')
        print('\nStep 1: Alignment hits computation')
        print('----------------------------------')
        alignment_hits= f'{args.output_prefix}_alignment_all_vs_all/'
        if 'diamond' in args.aligner:
            diamond_all_vs_all(args.fastas,
                               out_dir= alignment_hits,
                               fasta_ext= args.fasta_ext,
                               diamond= args.aligner,
                               quiet= not args.verbose_diamond,
                               evalue= args.evalue,
                               identity= args.identity,
                               cov= args.coverture,
                               max_target_seqs= args.max_target_seqs)
        elif 'blast' in args.aligner:
            blast_all_vs_all(args.fastas,
                             out_dir= alignment_hits,
                             fasta_ext= args.fasta_ext,
                             blast_command= args.aligner,
                             makeblastdb= args.makeblastdb,
                             evalue= args.evalue,
                             identity= args.identity,
                             cov= args.coverture,
                             max_target_seqs= args.max_target_seqs,
                    )
        else:
            ValueError(f'Unrecognized aligner "{args.aligner}"')
        with open(logfile, 'a') as F:
            F.write('> Step 1 completed\n')
        print(f'Alignment hits successfully written to {alignment_hits}')
        if (2 in args.steps) and (type(args.alignment_hits)!=str):
            print('This data will be used as input of step 2')
    else:
        alignment_hits= None

    # 2. Best hit selection
    #####################

    if 2 in args.steps:
        print("\nStep 2: Best hit selection")
        print("--------------------------")
        generated_hits= type(alignment_hits)==str
        inputed_hits= type(args.alignment_hits)==str
        if (not generated_hits) and (not inputed_hits):
            raise MissedData('Step 2 needs a value for the parameter --alignment_hits. You can create it running step 1')
        elif inputed_hits:
            alignment_hits= norm_path(args.alignment_hits)
        else:
            alignment_hits= norm_path(alignment_hits)
        if args.singletons:
            if type(args.fastas)==str:
                fasta_path= norm_path(args.fastas)
                text= f'\nInput fasta files: {fasta_path}'
                fasta_files= {f'{fasta_path}{x}' for x in os.listdir(fasta_path) if x.endswith(args.fasta_ext)}
            else:
                raise MissedData('Step 2 needs a value for the parameter --fastas whenerver you use the -singletons flag.')
        else:
            fasta_files= None
            text= ''

        print(f'Input hits: {alignment_hits}{text}')

        df_hits, OGs_table, singletons= _parse(alignment_hits, args.f_value, args.singletons, fasta_files, args.besthit_heuristic, N_max= args.N_max)

        opath= args.output_prefix+'.best_hits.tsv'
        df_hits.reset_index(drop=True).to_csv(opath, sep='\t', index= False)
        print(f'Best hits successfully written to {opath}')
        if (3 in args.steps) and (type(args.best_hits)!=str):
            print('This file will be used as input for step 3')

        opath= args.output_prefix+'.orthogroups.tsv'
        OGs_table.to_csv(opath, sep='\t', index= False)
        print(f'Orthogroups successfully written to {opath}')

        if args.singletons:
            opath= args.output_prefix+'.singletons.tsv'
            singletons.to_csv(opath, sep='\t', index= False)
            print(f'singletons successfully written to {opath}')

        with open(logfile, 'a') as F:
            F.write('> Step 2 completed\n')
    else:
        df_hits= None

    # 3. Gene tree reconstruction and orthology inference
    ###############################################
    if 3 in args.steps:
        print("\nStep 3: Gene tree reconstruction and orthology inference")
        print("--------------------------------------------------------")
        computedHs= type(df_hits)==pd.DataFrame
        inputedHs= type(args.best_hits)==str
        if (not computedHs) and (not inputedHs):
            raise MissedData('Step 3 needs a value for the parameter -best_hits. You can create it by running step 2.')
        if inputedHs:
            print(f'Processing best hit graphs at {args.best_hits}...')
            G= read_tl_digraph(args.best_hits, og_col= args.orthogroup_column)
        else:
            print('Processing best hit graphs of step 2...')
            G= tl_digraph_from_pandas(df_hits, og_col= args.orthogroup_column)

        F= lambda x,y,G0: (G0.nodes[x]['accession'], G0.nodes[y]['accession'])
        DD= {F(x,y,G0): G0[x][y]['weight'] for G0 in G for (x,y) in G0.edges}
        missed= [(y,x) for (x,y) in DD if (y,x) not in DD]
        DD.update({(y,x): DD[(x,y)] for (y,x) in missed})

        print('Reconstructing gene trees...')
        Tg= build_graph_series(G, args)
        if (4 in args.steps) and (type(args.gene_trees)!=str):
            print('These gene trees will be used as input for step 4')
        if (5 in args.steps) and (type(args.gene_trees)!=str):
            print('These gene trees will be used as input for step 5')

        # Compute orthologs
        TTg= Tg.reset_index()
        df_orthologs= orthologs_from_trees_df(TTg, forbidden_leaf_name= 'X', tree_col= 'tree')
        # Add bit-score
        df_orthologs['Normalized_bit_score']= df_orthologs.apply(lambda row: DD.get((row.a, row.b),'*') , axis=1 )

        # Print orthologs
        opath= f'{args.output_prefix}.orthologs.tsv'
        df_orthologs.to_csv(opath, sep= '\t', index= False)
        print(f'Orthologs successfully written to {opath}')

        with open(logfile, 'a') as F:
            F.write('> Step 3 completed\n')

    else:
        Tg= None

    # 4. Reconstruct species tree
    #############################
    if 4 in args.steps:
        print("\nStep 4: Species tree reconstruction")
        print("-----------------------------------")
        computedTg= type(Tg)==pd.Series
        inputedTg= type(args.gene_trees)==str

        if (not computedTg) and (not inputedTg):
            raise MissedData('Step 4 needs a value for the parameter -gene_trees. You can create it by running step 3.')
        if inputedTg:
            print(f'Reading gene trees from {args.gene_trees}...')
            gTrees= pd.read_csv(args.gene_trees, sep= '\t').set_index(
                args.orthogroup_column).tree.apply(
                lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            print(f'Using gene trees generated at step 3...')
            gTrees= Tg

        print("Reconstructing species tree...")
        species_tree= from_gene_forest(gTrees,
                                       method= args.species_tree_heuristic,
                                       numb_repeats= args.stree_heuristic_repeats,
                                       doble_build= args.streeh_no_doble_build,
                                       binary= args.streeh_binary,
                                      )

        s_newick= get_nhx(species_tree, root= 1, name_attr= 'species', ignore_inner_name= True)
        opath= f'{args.output_prefix}.species_tree.tsv'
        with open(opath, 'w') as F:
            F.write(s_newick)
        print(f'Species tree successfully written to {opath}')
        if (5 in args.steps) and (type(args.species_tree)!=str):
            print('This species tree will be used as input for step 5')

        with open(logfile, 'a') as F:
            F.write('> Step 4 completed\n')
    else:
        species_tree= None

    # 5. Reconciliate gene trees and species tree
    ##############################################
    if 5 in args.steps:
        print("\nStep 5: Gene and species trees reconciliation")
        print("---------------------------------------------")
        computedTg= type(Tg)==pd.Series
        inputedTg= type(args.gene_trees)==str
        if (not computedTg) and (not inputedTg):
            raise MissedData('Step 5 needs a value for the parameter -gene_trees. You can create it by running step 3.')
        if inputedTg:
            print(f'Reading gene trees from {args.gene_trees}...')
            gTrees= pd.read_csv(args.gene_trees, sep= '\t').set_index(
                args.orthogroup_column).tree.apply(
                lambda x: read_nhxx(x, name_attr= 'accession'))
        else:
            print(f'Using gene trees generated at step 3...')
            gTrees= Tg


        computedTs= type(species_tree)==DiGraph
        inputedTs= type(args.species_tree)==str
        if (not computedTs) and (not inputedTs):
            raise MissedData('Step 5 needs a value for the parameter -species_tree. You can create it by running step 4.')
        if inputedTs:
            print(f'Reading species tree from {args.species_tree}...')
            with open(args.species_tree) as F:
                sTree= read_nhxx(''.join( F.read().strip().split('\n') ),
                                 name_attr= 'species', attr_sep= args.S_attr_sep)
        else:
            print(f'Using species tree generated at step 4...')
            sTree= species_tree

        if not args.do_not_edit_inconsistent_trees:
            gTrees= gTrees.reset_index().set_index(args.orthogroup_column)
            print('Editing inconsistent gene trees...')
            gTrees= correct_tree_df(gTrees, sTree, tree_col= 'tree', root= 1,
                                    label_attr= 'accession',
                                    species_attr= 'species',
                                    event_attr= 'accession',
                                    inplace= False
                                   )
            F= lambda T: get_nhx(T, root= T.root, name_attr= 'accession')
            for_file= gTrees.reset_index()
            for_file.tree= for_file.tree.apply(F)

            opath= f'{args.output_prefix}.corrected_trees.tsv'
            for_file.to_csv(opath, sep= '\t', index= False)
            print(f'Corrected gene trees successfully written to {opath}')
            gTrees= gTrees.tree
            root= None
        else:
            root= 1

        print('Reconciling trees...')
        df_recs= reconciliate_many(gTrees, sTree, root= root)

        # Write resolved trees
        df_r= recon_table_to_str(sTree, df_recs, args.orthogroup_column)
        opath= f'{args.output_prefix}.reconciliation.tsv'
        df_r.to_csv(opath, sep= '\t', index= False)
        print(f'Reconciliation successfully written to {opath}')

        # Write labeled species tree
        nhx_s= get_nhx(sTree, name_attr= 'species', root= 1, ignore_inner_name= True)
        opath= f'{args.output_prefix}.labeled_species_tree.nhxx'
        with open(opath, 'w') as F:
            F.write(nhx_s)
        print(f'Indexed species tree successfully written to {opath}')

        with open(logfile, 'a') as F:
            F.write('> Step 5 completed\n')
    print("\nREvolutionH-tl finished all the tasks without any problem")
    print("---------------------------------------------------------")

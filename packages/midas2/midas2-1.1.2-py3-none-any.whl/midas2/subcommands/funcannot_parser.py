#!/usr/bin/env python3
import os
import sys
from itertools import chain
import pandas as pd
from pybedtools import BedTool

from midas2.common.argparser import add_subcommand
from midas2.common.utils import tsprint, retry, command, multithreading_map, drop_lz4, find_files, upload, pythonpath, upload_star, num_physical_cores
from midas2.common.utilities import decode_species_arg, decode_genomes_arg
from midas2.models.midasdb import MIDAS_DB
from midas2.params.inputs import MIDASDB_NAMES



def localpath(midas_db, species_id, filename):
    return midas_db.get_target_layout("pangenome_file", False, species_id, "", filename)

def localtemp(midas_db, species_id, method, filename):
    return midas_db.get_target_layout("funcannot_tempfile", False, species_id, method, filename)


def parse_genomad_plasmid_genes(file_path):
    """ Parse Genomad plasmid genes TSV into DataFrame """
    df = pd.read_csv(file_path, delimiter="\t")

    if df.empty:
        return pd.DataFrame()

    df = df[['gene', 'start', 'end', 'annotation_conjscan', 'annotation_amr', 'annotation_accessions', 'annotation_description']]
    df[['contig_external', 'gene_num']] = df['gene'].str.rsplit('_', n=1, expand=True)

    assert ~df[['contig_external', 'start', 'end']].duplicated().any(), f"Duplicated plasmid results for {file_path}"

    df = df[['contig_external', 'start', 'end', 'gene', 'annotation_conjscan', 'annotation_amr', 'annotation_accessions', 'annotation_description']]
    df = df.rename(columns={'start': 'start_genomad', 'end': 'end_genomad'})

    return df


def parse_genomad_virus_genes(file_path):
    """ Parse Genomad virus genes TSV into DataFrame """
    df = pd.read_csv(file_path, delimiter="\t")

    if df.empty:
        return pd.DataFrame()

    df = df[['gene', 'start', 'end', 'annotation_conjscan', 'annotation_amr', 'annotation_accessions', 'annotation_description']]
    df[['contig_plus', 'gene_num']] = df['gene'].str.rsplit('_', n=1, expand=True)

    # For the provisus case, we only keep the contig_id
    if df['contig_plus'].str.contains(r'\|p').any():
        df[['contig_external', 'part2']] = df['contig_plus'].str.rsplit(r'\|p', expand=True, n = 1)
    else:
        df['contig_external'] = df['contig_plus']

    assert ~df[['contig_id', 'start', 'end']].duplicated().any(), f"Duplicated virus results for {file_path}"

    df = df[['method', 'contig_id', 'start', 'end', 'gene',  'annotation_conjscan', 'annotation_amr', 'annotation_accessions', 'annotation_description']]
    df = df.rename(columns={'start': 'start_genomad', 'end': 'end_genomad'})

    return df


def parse_mefinder(file_path):
    """ Parse MEFINDER into DataFrame """
    df = pd.read_csv(file_path, delimiter=",", skiprows=5)

    if df.empty:
        return pd.DataFrame()

    df['contig_id'] = df['contig'].str.split(' ').str[0]
    df = df[['contig_id', 'start', 'end', 'mge_no', 'prediction', 'name', 'type', 'synonyms']]
    df = df.rename(columns={'contig_id': 'contig_external', 'start': 'start_mefinder', 'end': 'end_mefinder'})

    return df


def parse_resfinder(file_path):
    # rename the columns without spaces
    new_columns = ['resistance_gene', 'identity', 'align_ratio', 'coverage', 'within_reference_position', 'contig', 'within_contig_position', 'phenotype', 'accession_no']
    df = pd.read_csv(file_path, sep='\t', header=0, names=new_columns)

    if df.empty:
        return pd.DataFrame()

    df['contig'] = df['contig'].str.split(' ').str[0]
    df[['start', 'end']]  = df['within_contig_position'].str.split('\\.\\.', expand=True)
    # Notes there can be duplicated annotaitons for the same gene range (contig-start-end)
    df = df[['contig', 'start', 'end', 'resistance_gene', 'phenotype', 'accession_no']]
    df = df.rename(columns={'contig': 'contig_external', 'start': 'start_resfinder', 'end': 'end_resfinder'})
    return df


def merge_annot_with_genes(df, genes_99):
    bed1 = BedTool.from_dataframe(genes_99)
    bed2 = BedTool.from_dataframe(df)
    overlaps = bed1.intersect(bed2, wa=True, wb=True)
    overlapping_df = pd.read_table(overlaps.fn, header=None)
    overlapping_df.columns = list(genes_99.columns) + list(df.columns)
    # Drop duplicated column aka contig_id
    overlapping_df = overlapping_df.drop(columns=['contig_external'])
    # Reorder the column names
    overlapping_df = overlapping_df[['centroid_99'] + [col for col in overlapping_df if col != 'centroid_99']]
    return overlapping_df


def funannot_parser(args):
    if args.zzz_worker_mode:
        funannot_parser_worker(args)
    else:
        funannot_parser_master(args)


def funannot_parser_master(args):

    midas_db = MIDAS_DB(os.path.abspath(args.midasdb_dir), args.midasdb_name)
    species_for_genome = midas_db.uhgg.genomes

    def genome_work(genome_id):
        """
        For each genome, we sequentially read in three functional annotation tables,
        overlap with the list_of_centroids99, write to TEMP files.
        """

        assert genome_id in species_for_genome, f"Genome {genome_id} is not in the database."
        species_id = species_for_genome[genome_id]

        gene_feature_fp = midas_db.get_target_layout("annotation_genes", False, species_id, genome_id)
        cluster_info_fp = midas_db.get_target_layout("pangenome_cluster_info", False, species_id)

        msg = f"Annotating genome {genome_id} from species {species_id}."

        if not args.upload and os.path.exists(local_file):
            if not args.force:
                tsprint(f"Destination {local_file} for genome {genome_id} annotations already exists.  Specify --force to overwrite.")
                return
            msg = msg.replace("Importing", "Reimporting")
        tsprint(msg)

        last_dest = midas_db.get_target_layout("annotation_log", True, species_id, genome_id)
        local_dest = midas_db.get_target_layout("annotation_log", False, species_id, genome_id)
        local_dir = os.path.dirname(os.path.dirname(local_dest))
        command(f"mkdir -p {local_dir}")

        worker_log = os.path.basename(local_dest)
        worker_subdir = os.path.dirname(local_dest) if args.scratch_dir == "." else f"{args.scratch_dir}/functional/{genome_id}"
        worker_log = f"{worker_subdir}/{worker_log}"

        if not args.debug:
            command(f"rm -rf {worker_subdir}")
        if not os.path.isdir(worker_subdir):
            command(f"mkdir -p {worker_subdir}")

        # Recurisve call via subcommand.  Use subdir, redirect logs.
        # Output files are generated inside worker_subdir
        subcmd_str = f"--zzz_worker_mode --midasdb_name {args.midasdb_name} --midasdb_dir {os.path.abspath(args.midasdb_dir)} {'--debug' if args.debug else ''} {'--upload' if args.upload else ''}"
        worker_cmd = f"cd {worker_subdir}; PYTHONPATH={pythonpath()} {sys.executable} -m midas2 funannot_parser --genome {genome_id} {subcmd_str} &>> {worker_log}"
        with open(f"{worker_log}", "w") as slog:
            slog.write(msg + "\n")
            slog.write(worker_cmd + "\n")

        try:
            command(worker_cmd)
        finally:
            # Cleanup should not raise exceptions of its own, so as not to interfere with any
            # prior exceptions that may be more informative.  Hence check=False.
            if args.upload:
                upload(f"{worker_log}", last_dest, check=False)
            if args.scratch_dir != ".":
                command(f"cp -r {worker_subdir} {local_dir}")
            if not args.debug:
                command(f"rm -rf {worker_subdir}", check=False)

    if args.genomes:
        genome_id_list = decode_genomes_arg(args, species_for_genome)

    if args.species:
        species = midas_db.uhgg.species
        species_id_list = decode_species_arg(args, species)
        genome_id_list = list(chain.from_iterable([list(species[spid].keys()) for spid in species_id_list]))

    CONCURRENT_PROKKA_RUNS = int(args.num_threads / 8)
    multithreading_map(genome_work, genome_id_list, num_threads=CONCURRENT_PROKKA_RUNS)


def funannot_parser_worker(args):
    """
    Input:
        - pangenomes/cluster_info.txt
        - gene_annotations/
        - genomad, mefinder and resfinder results
    Output:
        - Three functional annotations tables only for centroids.99
    """

    violation = "Please do not call funannot_parser_worker directly.  Violation"
    assert args.zzz_worker_mode, f"{violation}:  Missing --zzz_worker_mode arg."

    midas_db = MIDAS_DB(args.midasdb_dir, args.midasdb_name)
    species_for_genome = midas_db.uhgg.genomes

    genome_id = args.genomes
    species_id = species_for_genome[genome_id]

    # Assume MIDASDB2 is available locally
    cluster_info_fp = midas_db.get_target_layout("pangenome_cluster_info", False, species_id)
    contig_len_fp = midas_db.get_target_layout("pangenome_contigs_len", False, species_id)
    gene_feature_fp = midas_db.get_target_layout("annotation_genes", False, species_id, genome_id)

    # Read in centroids_info.txt and only keep the first column
    centroids_99 = pd.read_csv(cluster_info_fp, sep='\t', usecols=[0])
    contig_len = pd.read_csv(contig_len_fp, sep='\t')
    gene_features = pd.read_csv(gene_feature_fp, sep='\t')

    # Only keep cenroids_99 from given genome
    genes_99 = pd.merge(centroids_99, gene_features, left_on='centroid_99', right_on='gene_id', how='inner')
    genes_99 = pd.merge(genes_99, contig_len[['contig_id', 'contig_length']], left_on='contig_id', right_on='contig_id', how='inner')
    genes_99 = genes_99[['contig_id', 'start', 'end', 'centroid_99', 'strand', 'gene_type', 'contig_length']]

    # Read in Genomad results
    df = parse_genomad_virus_genes(midas_db.get_target_layout("genomad_virus_genes", False, species_id, genome_id))
    if df.empty:
        command("touch file")
    else:
        df = merge_annot_with_genes(df, genes_99)
        df.to_csv(midas_db.get_target_layout("pangenome_genomad_virus", False, species_id), sep='\t', index=False)


def register_args(main_func):
    subparser = add_subcommand('funannot_parser', main_func, help='Genome annotation for specified genomes using Prokka with all cores')
    subparser.add_argument('--genomes',
                           dest='genomes',
                           required=False,
                           help="genome[,genome...] to import;  alternatively, slice in format idx:modulus, e.g. 1:30, meaning annotate genomes whose ids are 1 mod 30; or, the special keyword 'all' meaning all genomes")
    subparser.add_argument('--species',
                           dest='species',
                           required=False,
                           help="species[,species...] whose pangenome(s) to build;  alternatively, species slice in format idx:modulus, e.g. 1:30, meaning build species whose ids are 1 mod 30; or, the special keyword 'all' meaning all species")
    subparser.add_argument('--midasdb_name',
                           dest='midasdb_name',
                           type=str,
                           default="uhgg",
                           choices=MIDASDB_NAMES,
                           help="MIDAS Database name.")
    subparser.add_argument('--midasdb_dir',
                           dest='midasdb_dir',
                           type=str,
                           default=".",
                           help="Path to local MIDAS Database.")
    subparser.add_argument('-t',
                           '--num_threads',
                           dest='num_threads',
                           type=int,
                           default=num_physical_cores,
                           help="Number of threads")
    subparser.add_argument('--upload',
                           action='store_true',
                           default=False,
                           help='Upload built files to AWS S3')
    subparser.add_argument('--scratch_dir',
                           dest='scratch_dir',
                           type=str,
                           default=".",
                           help="Absolute path to scratch directory for fast I/O.")
    return main_func


@register_args
def main(args):
    tsprint(f"Executing midas2 subcommand {args.subcommand}.") # with args {vars(args)}.")
    funannot_parser(args)

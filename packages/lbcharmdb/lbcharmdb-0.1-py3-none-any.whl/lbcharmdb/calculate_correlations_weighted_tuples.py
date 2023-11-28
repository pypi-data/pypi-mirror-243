import logging
import math
from typing import Optional

import numpy as np
import ROOT
from tqdm import tqdm

from . import utilities
from .units import MeV

DEBUG_MODE = False
RDF = ROOT.ROOT.RDataFrame
PT_TOLERANCE = 0.001 * MeV

def compute_integral_of_expression_in_tree ( input_tree: ROOT.TTree, 
                                tformula_expression: str, cuts: str="(1)" ) -> float:
    """
    Quickly computes the integral of an expression in a ROOT.TTree by 
    exploiting the mean of the histogram (which is always exact and
    not influenced by the binning), together with the quick access to the
    number of entries. This is tested to be equal to a loop over entries and
    an explicit sum per entry. 
    """
    histogram_name = utilities.id_generator()
    
    input_tree.Draw(("{}>>" + histogram_name).format(tformula_expression), cuts, "GOFF")
    histogram = ROOT.gDirectory.Get(histogram_name)
    
    return histogram.GetMean()*histogram.GetEntries()

def normalise_weights( input_tree, weight_variable ):
    normalisation_factor = compute_integral_of_expression_in_tree( input_tree, weight_variable)
    weightsq = compute_integral_of_expression_in_tree( input_tree, f"({weight_variable}**2)")
    
    if normalisation_factor > 0 and weightsq > 0:
        normalisation_factor /= weightsq
    else:
        return 1.0
    
    return normalisation_factor

def keys_by_run_number( run_numbers ):
    """ Creates an index based on the run number """

    unqiue_run_numbers, run_number_keys = np.unique( run_numbers, True )

    return {"run_numbers": unqiue_run_numbers, "keys": run_number_keys}

def seek_index( B_data, event_number: int, run_number: int, pt: float,
                run_number_index: dict ):
    """ Looks for the (event_number, run_number, K_PT) combination in
    another dataset, and returns that index. If multiple indices were found,
    the first match is returned. """
    keys = [ ]
    if not np.isin( run_number, run_number_index["run_numbers"], assume_unique=True ):
        return (False, "run")

    #idx, = np.where(run_number_index["run_numbers"] == run_number )[0] # should be unique!
    idx = np.searchsorted( run_number_index["run_numbers"], run_number )
    if idx < len(run_number_index["run_numbers"]) -1:
        keys = range( run_number_index["keys"][idx], run_number_index["keys"][idx+1] )
    else:
        keys = range( run_number_index["keys"][idx], len(B_data["runNumber"]) )

    subset = B_data["eventNumber"][keys[0]:keys[-1]+1]
    key_a = np.searchsorted( subset, event_number   ) + keys[0]
    key_b = np.searchsorted( subset, event_number+1 ) + keys[0]

    event_number_match = range( key_a, key_b )

    if not len(event_number_match):
        print ("Could not match based on event.")
        return (False, "event")
    
    kinematics_match = [ k for k in event_number_match if abs(B_data["TO_MATCH_PT"][k] - pt) < PT_TOLERANCE ]

    if not len(kinematics_match):
        print ("Could not match based on kinematics.")
        return (False, "kinematics")
    
    if len(kinematics_match) > 1 and DEBUG_MODE:
        print (f"Multiple matches found for (run,event)={run_number},{event_number}: {len(kinematics_match)}")
        print (kinematics_match)
        print(pt)
        print ([B_data["TO_MATCH_PT"][k] for k in kinematics_match])
        print("---")

    return (True, kinematics_match[0])

def sort_by_run_number( data_set ):
    #indx = np.argsort( data_set["runNumber"] )
    indx = np.lexsort( (data_set["eventNumber"], data_set["runNumber"]) )

    return {"runNumber":    data_set["runNumber"][indx],
            "eventNumber":  data_set["eventNumber"][indx],
            "TOTAL_WEIGHT": data_set["TOTAL_WEIGHT"][indx],
            "TO_MATCH_PT":  data_set["TO_MATCH_PT"][indx]}

def match_by_event_run_number( reference_tree: ROOT.TTree, tree_B: ROOT.TTree, 
                                kinematic_branch_name_A: str,
                                kinematic_branch_name_B: str,
                                weight_tformula_A: str,
                                weight_tformula_B ):
    """ Tree_A is the reference tree """

    if kinematic_branch_name_A is None:
        kinematic_branch_name_A = "eventNumber"
    
    logging.info("Sorting datasets...")
    reference_data = RDF(reference_tree).Define("TO_MATCH_PT", kinematic_branch_name_A).Define("TOTAL_WEIGHT", weight_tformula_A)
    reference_data = reference_data.AsNumpy(columns=["eventNumber", "runNumber", "TOTAL_WEIGHT", "TO_MATCH_PT"])
    reference_data = sort_by_run_number( reference_data )

    B_data = RDF(tree_B)
    B_data = RDF(B_data).Define("TO_MATCH_PT", kinematic_branch_name_B).Define("TOTAL_WEIGHT", weight_tformula_B)
    B_data = B_data.AsNumpy(columns=["eventNumber", "runNumber", "TOTAL_WEIGHT", "TO_MATCH_PT"])
    B_data = sort_by_run_number( B_data )
    
    run_number_index = keys_by_run_number( B_data["runNumber"] )

    B_data_augmented = {
        "eventNumber": reference_data["eventNumber"][:],
        "runNumber": reference_data["runNumber"][:],
        "TOTAL_WEIGHT": np.zeros( len(reference_data["runNumber"])),
        "TO_MATCH_PT": reference_data["TO_MATCH_PT"][:]}

    n_found = 0
    missing_runs = []

    for event_key_ref, run_number in tqdm(enumerate(reference_data["runNumber"]), total=len(reference_data["runNumber"])):
        weight = 0.

        event_number = reference_data["eventNumber"][event_key_ref]
        pt           = reference_data["TO_MATCH_PT"][event_key_ref]

        found, key = seek_index( B_data, event_number, run_number, pt, run_number_index )
        
        if found:
            weight = B_data["TOTAL_WEIGHT"][key]
            n_found += 1
        else:
            if key == "run":
                missing_runs += [ run_number ]
            elif key == "event":
                missing_runs += [ event_number ]
        
        B_data_augmented["TOTAL_WEIGHT"][event_key_ref] = weight

    if n_found < len( B_data["TO_MATCH_PT"] ):
        n_missed = len(B_data["TO_MATCH_PT"]) - n_found

        print (f"There are more entries in the 'reduced' tree! Skipped {n_missed} entries.")
    
    return reference_data, B_data_augmented


def match_trees( *, tree_A: ROOT.TTree, tree_B: ROOT.TTree, 
                            weight_branch_name_A: str,
                            weight_branch_name_B: str,
                            matched_tree_persistence_path: str,
                            kinematic_branch_name: str ):
    matched_tree_A, matched_tree_B = match_by_event_run_number( reference_tree = tree_A, 
                                            tree_B = tree_B, 
                                            kinematic_branch_name_A = kinematic_branch_name,
                                            kinematic_branch_name_B = kinematic_branch_name,
                                            weight_tformula_A=weight_branch_name_A,
                                            weight_tformula_B=weight_branch_name_B )
    
    df_A = ROOT.RDF.FromNumpy(matched_tree_A)
    df_B = ROOT.RDF.FromNumpy(matched_tree_B)

    df_A.Snapshot( "datasetA", f"{matched_tree_persistence_path}/matched_trees_A.root" )
    df_B.Snapshot( "datasetB", f"{matched_tree_persistence_path}/matched_trees_B.root" )

    return  f"{matched_tree_persistence_path}/matched_trees_A.root", f"{matched_tree_persistence_path}/matched_trees_B.root"

def calculate_correlation( *, tree_A: ROOT.TTree, tree_B: ROOT.TTree, 
                            weight_branch_name_A: str,
                            weight_branch_name_B: str,
                            kinematic_branch_name: str,
                            matched_tree_persistence_path: Optional[str]=None, ):
    matched_tree_A, matched_tree_B = match_by_event_run_number( reference_tree = tree_A, 
                                            tree_B = tree_B, 
                                            kinematic_branch_name_A = kinematic_branch_name,
                                            kinematic_branch_name_B = kinematic_branch_name,
                                            weight_tformula_A=weight_branch_name_A,
                                            weight_tformula_B=weight_branch_name_B )
    weight_product = np.inner( matched_tree_A["TOTAL_WEIGHT"], matched_tree_B["TOTAL_WEIGHT"] )
    normsq = np.inner( matched_tree_A["TOTAL_WEIGHT"], 
                matched_tree_A["TOTAL_WEIGHT"] ) * np.inner( matched_tree_B["TOTAL_WEIGHT"], matched_tree_B["TOTAL_WEIGHT"] )
    norm = math.sqrt(normsq)
    
    return weight_product/norm

def calculate_correlation_identical_trees( tree_A: ROOT.TTree, tree_B: ROOT.TTree ):
    tree_B.SetName("tree_B")

    normalisation_A = normalise_weights(tree_A, "TOTAL_WEIGHT")
    normalisation_B = normalise_weights(tree_B, "TOTAL_WEIGHT")
    
    if (tree_A.GetEntries() != tree_B.GetEntries()):
        logging.fatal("Cannot compute correlation when the number of entries is different.")
        logging.fatal(f"{tree_A.GetEntries()!s} for treeA, {tree_B.GetEntries()!s} for tree B")
    
    tree_A.AddFriend(tree_B)

    weight_A_formula = f"({normalisation_A}*TOTAL_WEIGHT)"
    weight_B_formula = f"({normalisation_B}*tree_B.TOTAL_WEIGHT)"
    weight_product_formula = f"({weight_A_formula}*{weight_B_formula})"

    weight_inner_product = compute_integral_of_expression_in_tree( tree_A, weight_product_formula)
    norm_of_weight_A = compute_integral_of_expression_in_tree( tree_A, weight_A_formula)
    norm_of_weight_B = compute_integral_of_expression_in_tree( tree_A, weight_B_formula)
    
    return weight_inner_product/math.sqrt(norm_of_weight_B*norm_of_weight_A)

def get_application_options():
    import argparse

    parser = argparse.ArgumentParser(description = "Script to help out with computing the correlation between weighted nTuples")
    parser.add_argument('--treeA_file', help='Location of the .root file containing the first nTuple', required=True)
    parser.add_argument('--treeA_tree_path', help='Location *inside* the .root file of the first nTuple (eg. "DecayTree")', required=True)

    parser.add_argument('--friend_treeA_file', 
        help='Location of the .root file containing a friend tree for the first nTuple', nargs="*")
    parser.add_argument('--friend_treeA_tree_path', 
        help='Location *inside* the .root file of the first nTuple (eg. "DecayTree")', nargs="*")

    parser.add_argument('--friend_treeB_file', 
        help='Location of the .root file containing a friend tree for second nTuple', nargs="*")
    parser.add_argument('--friend_treeB_tree_path', 
        help='Location *inside* the .root file of the first nTuple (eg. "DecayTree")', nargs="*")

    parser.add_argument('--treeB_file', help='Location of the .root file containing the second nTuple', required=True)
    parser.add_argument('--treeB_tree_path', help='Location *inside* the .root file of the second nTuple (eg. "DecayTree")', required=True)
    parser.add_argument('--output_directory', help='Location to write the matched nTuples to, along with the results', required=True)
    parser.add_argument('--kinematic_branch_name', 
        help='Name of a branch that is used for the matching inside ' \
                            + 'multiple-candidates. For exampe: K_PT, or D_PT.', required=True)
    parser.add_argument('--weight_branch_name_A', 
        help='TFormula to compute the weight in tree A.', default="weight", 
        required=True)
    parser.add_argument('--weight_branch_name_B', 
        help='TFormula to compute the weight in tree B.', default="weight", 
        required=True)
    parser.add_argument('--skip_matching', 
        help='If set, the per-candidate tree matching is skipped.', 
        action="store_true")
    
    return parser

def main():
    logger = logging.getLogger( "main" )

    options = get_application_options().parse_args()
    
    logger.info( "Initialising correlation calculator." )
    
    utilities.check_output_directory( options.output_directory )

    ifile_A = ROOT.TFile.Open( options.treeA_file, "READONLY")
    itree_A = ifile_A.Get( options.treeA_tree_path )

    if not itree_A:
        logger.fatal(f"Could not find tree {options.treeA_tree_path} in {options.treeA_file}.")

    ROOT.TFile.Open( options.treeB_file, "READONLY")
    itree_B = ifile_A.Get( options.treeB_tree_path )

    if not itree_B:
        logger.fatal(f"Could not find tree {options.treeB_tree_path} in {options.treeB_file}.")

    #calculate_correlation(itree_A, itree_B, options.weight_branch_name,
    #                        options.output_directory, options.kinematic_branch_name)
    if not options.skip_matching:
        cached_file_A, cached_file_B = match_trees( tree_A = itree_A, tree_B = itree_B, 
                weight_branch_name_A = options.weight_branch_name_A,
                weight_branch_name_B = options.weight_branch_name_B,
                kinematic_branch_name = options.kinematic_branch_name, matched_tree_persistence_path=options.output_directory )
    else:
        cached_file_A, cached_file_B = f"{options.output_directory}/matched_trees_A.root", \
                                        f"{options.output_directory}/matched_trees_B.root"

    ifile_micro_A = ROOT.TFile.Open( cached_file_A, "READONLY" )
    itree_micro_A = ifile_micro_A.Get("datasetA")

    ifile_micro_B = ROOT.TFile.Open( cached_file_B, "READONLY" )
    itree_micro_B = ifile_micro_B.Get("datasetB")
    
    logger.info("Calculating correlation...")
    print( "Correlation coefficient", calculate_correlation_identical_trees( tree_A=itree_micro_A, tree_B=itree_micro_B ) )